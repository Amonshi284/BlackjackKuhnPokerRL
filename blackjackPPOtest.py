import blackjackenv.blackjack
from os.path import exists

from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
import gymnasium as gym
from sb3_contrib.common.wrappers import ActionMasker

MAX_TOTAL_ROUNDS = 1000000
MAX_LEARN_TIMESTEPS = 1000000


def mask_fn(env):
    return env.action_mask()


if __name__ == '__main__':

    env = gym.make('blackjack/BlackJack-v0.1.1')
    env = ActionMasker(env, mask_fn)

    if exists("ppo_blackjack.zip"):
        model = MaskablePPO.load("ppo_blackjack", env)
    else:
        model = MaskablePPO(MaskableActorCriticPolicy, env, verbose=1, tensorboard_log='./blackjack_tensorboard/')
        model.learn(total_timesteps=MAX_LEARN_TIMESTEPS)
        model.save("ppo_blackjack")

    rewards = 0
    env.reset()
    model = MaskablePPO.load("ppo_blackjack", env)

    for i in range(MAX_TOTAL_ROUNDS):
        print(i)
        obs, info = env.reset()
        terminated, truncated = False, False
        print(obs)
        while True:
            action, _states = model.predict(obs)
            if action == 3 and not info["action_mask"][3]:
                action = 1
            elif action == 4 and not info["action_mask"][4]:
                action = 1
            obs, reward, terminated, truncated, info = env.step(action)
            print(obs, terminated, reward)
            env.render()
            if terminated or truncated:
                rewards += reward
                break


    env.close()


    avg_reward = rewards / MAX_TOTAL_ROUNDS
    print("Average Reward:", avg_reward)


    """for _ in range(10):
        observation, info = envs.reset()
        print(observation)
        while True:
            action = int(input("Enter your action:\n1) stick\n2) hit\n3) double down\n4) split\n5) surrender")) - 1
            observation, reward, terminated, truncated, info = envs.step(action)
            print(observation, terminated, reward)
            if terminated or truncated:
                break
    
    envs.close()"""
