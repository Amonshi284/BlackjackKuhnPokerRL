import kuhnpokerenv.kuhnpoker
from os.path import exists
from stable_baselines3 import PPO
import gymnasium as gym
from stable_baselines3.common.env_util import make_vec_env

MAX_TOTAL_GAMES = 10000

if __name__ == '__main__':
    env = gym.make("kuhnpoker/KuhnPoker-v0")
    if exists("ppo_kuhn.zip"):
        model = PPO.load("ppo_kuhn", env)
    else:
        model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="kuhn_tensorboard")

    model.learn(total_timesteps=100000)
    model.save("ppo_kuhn")

    rewards = 0
    env.reset(options={"alpha": 0.3, "opponent": "optimal", "start": "player"})
    for i in range(MAX_TOTAL_GAMES):
        print(i)
        obs, info = env.reset(options={"alpha": 0.3, "opponent": "optimal", "start": "player"})
        terminated, truncated = False, False
        print(obs)
        while True:
            action, _states = model.predict(obs)
            obs, reward, terminated, truncated, info = env.step(action)
            print(obs, terminated, reward)
            if terminated or truncated:
                rewards += reward
                break

    env.close()

    avg_reward = rewards / MAX_TOTAL_GAMES
    print("Average: ", avg_reward)
