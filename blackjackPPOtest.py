import blackjackenv.blackjack
from basicStrategyBlackJack import BasicStrategyChart
from torch import nn
from os.path import exists

from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
import gymnasium as gym
from sb3_contrib.common.wrappers import ActionMasker

MAX_TOTAL_ROUNDS = 1000000
MAX_LEARN_TIMESTEPS = 2000000


def mask_fn(env):
    return env.action_mask()


if __name__ == '__main__':

    env = gym.make('blackjack/BlackJack-v0.1.1')
    env = ActionMasker(env, mask_fn)

    if exists("ppo_blackjack_v5.zip"):
        model = MaskablePPO.load("ppo_blackjack_v5", env)
    else:
        policy_kwargs = dict(activation_fn=nn.ReLU, net_arch=dict(pi=[32, 32], vf=[32, 32]))
        model = MaskablePPO(MaskableActorCriticPolicy, env, verbose=1, tensorboard_log='./blackjack_tensorboard/',
                            stats_window_size=1000000, learning_rate=0.0006, policy_kwargs=policy_kwargs, clip_range=0.4
                            )
        model.learn(total_timesteps=MAX_LEARN_TIMESTEPS)
        model.save("ppo_blackjack_v5")

    rewards = 0
    wins = 0
    actions = 0
    correctactions = 0
    env.reset()

    for i in range(MAX_TOTAL_ROUNDS):
        print(i)
        obs, info = env.reset()
        terminated, truncated = False, False
        print(obs)
        while True:
            # action, _states = model.predict(obs, action_masks=info["action_mask"], deterministic=True)
            action = env.action_space.sample()
            actions += 1
            if obs[3] == 1:
                if obs[2] == 1:
                    actionopt = BasicStrategyChart.pair_hand[0][obs[1] - 2].value
                else:
                    actionopt = BasicStrategyChart.pair_hand[int(obs[0] / 2) - 1][obs[1] - 2].value
            elif obs[2] == 1:
                actionopt = BasicStrategyChart.soft_hand[obs[0] - 13][obs[1] - 2].value
            else:
                actionopt = BasicStrategyChart.hard_hand[obs[0] - 5][obs[1] - 2].value
            if actionopt == 4 and not info["action_mask"][4]:
                actionopt = 1
            if actionopt == 3 and not info["action_mask"][3]:
                actionopt = 1
            if actionopt == 2 and not info["action_mask"][2]:
                if obs[0] == 18:
                    actionopt = 0
                else:
                    actionopt = 1
            if action == actionopt:
                correctactions += 1
            print(action)
            obs, reward, terminated, truncated, info = env.step(action)
            print(obs, terminated, reward)
            env.render()
            if terminated or truncated:
                rewards += reward
                if float(reward) > 0.0:
                    wins += 1
                break

    env.close()

    avg_reward = rewards / MAX_TOTAL_ROUNDS
    winrate = wins / MAX_TOTAL_ROUNDS
    print("Average Reward:", avg_reward)
    print("Winrate:", winrate)
    print("Random Situations:", correctactions / actions)

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
