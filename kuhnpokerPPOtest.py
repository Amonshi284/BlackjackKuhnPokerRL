from torch import nn

import kuhnpokerenv.kuhnpoker
from os.path import exists
from stable_baselines3 import PPO, A2C, DQN
import gymnasium as gym
from stable_baselines3.common.env_util import make_vec_env

MAX_TOTAL_GAMES = 200000
MAX_LEARN_TIMESTEPS = 200000


def eval_kuhn(alpha, opponent, start, actiontable):
    rewards = 0
    env.reset(options={"alpha": alpha, "opponent": opponent, "start": start})
    for j in range(MAX_TOTAL_GAMES):
        # print(j)
        obs, info = env.reset()
        terminated, truncated = False, False
        # print(obs)
        while True:
            action, _states = model.predict(obs, deterministic=False)
            if start == "player":
                # as starting player
                if obs[1] == 0:
                    # starting action
                    if obs[0] == 0:
                        # first action with Jack
                        if action == 0:
                            actiontable[0][0][0][0] += 1  # check
                        else:
                            actiontable[0][0][0][1] += 1  # bet
                    elif obs[0] == 1:
                        # first action with queen
                        if action == 0:
                            actiontable[0][1][0][0] += 1  # check
                        else:
                            actiontable[0][1][0][1] += 1  # bet
                    else:
                        # first action with king
                        if action == 0:
                            actiontable[0][2][0][0] += 1  # check
                        else:
                            actiontable[0][2][0][1] += 1  # bet
                elif obs[1] == 2:
                    # reaction
                    if obs[0] == 0:
                        # reaction with jack
                        if action == 0:
                            actiontable[0][0][1][0] += 1  # check
                        else:
                            actiontable[0][0][1][1] += 1  # bet
                    elif obs[0] == 1:
                        # reaction with queen
                        if action == 0:
                            actiontable[0][1][1][0] += 1  # check
                        else:
                            actiontable[0][1][1][1] += 1  # bet
                    else:
                        # reaction with king
                        if action == 0:
                            actiontable[0][2][1][0] += 1  # check
                        else:
                            actiontable[0][2][1][1] += 1  # bet
            else:
                # as second player
                if obs[1] == 1:
                    # enemy checks
                    if obs[0] == 0:
                        # reaction to check with jack
                        if action == 0:
                            actiontable[1][0][0][0] += 1  # check
                        else:
                            actiontable[1][0][0][1] += 1  # bet
                    elif obs[0] == 1:
                        # reaction to check with queen
                        if action == 0:
                            actiontable[1][1][0][0] += 1  # check
                        else:
                            actiontable[1][1][0][1] += 1  # bet
                    else:
                        # reaction to check with king
                        if action == 0:
                            actiontable[1][2][0][0] += 1  # check
                        else:
                            actiontable[1][2][0][1] += 1  # bet
                else:
                    # enemy bets
                    if obs[0] == 0:
                        # reaction to bet with jack
                        if action == 0:
                            actiontable[1][0][1][0] += 1  # check
                        else:
                            actiontable[1][0][1][1] += 1  # bet
                    elif obs[0] == 1:
                        # reaction to bet with queen
                        if action == 0:
                            actiontable[1][1][1][0] += 1  # check
                        else:
                            actiontable[1][1][1][1] += 1  # bet
                    else:
                        # reaction to bet with king
                        if action == 0:
                            actiontable[1][2][1][0] += 1  # check
                        else:
                            actiontable[1][2][1][1] += 1  # bet
            obs, reward, terminated, truncated, info = env.step(action)
            # print(obs, terminated, reward)
            if terminated or truncated:
                rewards += reward
                break
    return rewards, actiontable


if __name__ == '__main__':
    env = gym.make("kuhnpoker/KuhnPoker-v0")
    env.reset(options={"start": "opponent"})
    actiontable = [[[[0 for n in range(2)] for m in range(2)] for l in range(3)] for k in range(2)]
    if exists("dqn_kuhn_v8.zip"):
        model = DQN.load("dqn_kuhn_v8", env)
    else:
        policy_kwargs = dict(activation_fn=nn.ReLU, net_arch=[32, 32])
        model = DQN("MlpPolicy", env, verbose=1, tensorboard_log="kuhn_tensorboard", stats_window_size=100000,
                    learning_rate=0.0006)
        print(model.policy)
        model.learn(total_timesteps=MAX_LEARN_TIMESTEPS)
        env.reset(options={"start": "player"})
        model.learn(total_timesteps=MAX_LEARN_TIMESTEPS)
        model.save("dqn_kuhn_v8")

    for i in range(10):
        env.reset(options={"alpha": 0.3, "opponent": "optimal", "start": "player"})
        reward1st, actiontable = eval_kuhn(0.3, "optimal", "player", actiontable)
        reward2nd, actiontable = eval_kuhn(0.3, "optimal", "opponent", actiontable)
        avg_1st_rewards = reward1st / MAX_TOTAL_GAMES
        avg_2nd_rewards = reward2nd / MAX_TOTAL_GAMES
        avg_reward = avg_1st_rewards + avg_2nd_rewards
        print("Average as 1st player:\t", avg_1st_rewards, "\nAverage as 2nd player:\t", avg_2nd_rewards,
              "\nAverage reward:\t", avg_reward)

    print("first player")
    try:
        print("jackstart:\tcheck:", actiontable[0][0][0][0], "\tbet:", actiontable[0][0][0][1], "\tcheckquote:",
              actiontable[0][0][0][0] / (actiontable[0][0][0][0] + actiontable[0][0][0][1]))
    except ZeroDivisionError:
        print("divisionerror!")
    try:
        print("jackreact:\tcheck:", actiontable[0][0][1][0], "\tbet:", actiontable[0][0][1][1], "\tcheckquote:",
              actiontable[0][0][1][0] / (actiontable[0][0][1][0] + actiontable[0][0][1][1]))
    except ZeroDivisionError:
        print("divisionerror!")
    try:
        print("queenstart:\tcheck:", actiontable[0][1][0][0], "\tbet:", actiontable[0][1][0][1], "\tcheckquote:",
              actiontable[0][1][0][0] / (actiontable[0][1][0][0] + actiontable[0][1][0][1]))
    except ZeroDivisionError:
        print("divisionerror!")
    try:
        print("queenreact:\tcheck:", actiontable[0][1][1][0], "\tbet:", actiontable[0][1][1][1], "\tcheckquote:",
              actiontable[0][1][1][0] / (actiontable[0][1][1][0] + actiontable[0][1][1][1]))
    except ZeroDivisionError:
        print("divisionerror!")
    try:
        print("kingstart:\tcheck:", actiontable[0][2][0][0], "\tbet:", actiontable[0][2][0][1], "\tcheckquote:",
              actiontable[0][2][0][0] / (actiontable[0][2][0][0] + actiontable[0][2][0][1]))
    except ZeroDivisionError:
        print("divisionerror!")
    try:
        print("kingreact:\tcheck:", actiontable[0][2][1][0], "\tbet:", actiontable[0][2][1][1], "\tcheckquote:",
              actiontable[0][2][1][0] / (actiontable[0][2][1][0] + actiontable[0][2][1][1]))
    except ZeroDivisionError:
        print("divisionerror!")
    print("second player")
    try:
        print("jackreactcheck:\tcheck:", actiontable[1][0][0][0], "\tbet:", actiontable[1][0][0][1], "\tcheckquote:",
              actiontable[1][0][0][0] / (actiontable[1][0][0][0] + actiontable[1][0][0][1]))
    except ZeroDivisionError:
        print("divisionerror!")
    try:
        print("jackreactbet:\tcheck:", actiontable[1][0][1][0], "\tbet:", actiontable[1][0][1][1], "\tcheckquote:",
              actiontable[1][0][1][0] / (actiontable[1][0][1][0] + actiontable[1][0][1][1]))
    except ZeroDivisionError:
        print("divisionerror!")
    try:
        print("queenreactcheck:\tcheck:", actiontable[1][1][0][0], "\tbet:", actiontable[1][1][0][1], "\tcheckquote:",
              actiontable[1][1][0][0] / (actiontable[1][1][0][0] + actiontable[1][1][0][1]))
    except ZeroDivisionError:
        print("divisionerror!")
    try:
        print("queenreactbet:\tcheck:", actiontable[1][1][1][0], "\tbet:", actiontable[1][1][1][1], "\tcheckquote:",
              actiontable[1][1][1][0] / (actiontable[1][1][1][0] + actiontable[1][1][1][1]))
    except ZeroDivisionError:
        print("divisionerror!")
    try:
        print("kingreactcheck:\tcheck:", actiontable[1][2][0][0], "\tbet:", actiontable[1][2][0][1], "\tcheckquote:",
              actiontable[1][2][0][0] / (actiontable[1][2][0][0] + actiontable[1][2][0][1]))
    except ZeroDivisionError:
        print("divisionerror!")
    try:
        print("kingreactbet:\tcheck:", actiontable[1][2][1][0], "\tbet:", actiontable[1][2][1][1], "\tcheckquote:",
              actiontable[1][2][1][0] / (actiontable[1][2][1][0] + actiontable[1][2][1][1]))
    except ZeroDivisionError:
        print("divisionerror!")
    env.close()
