import blackjackenv.blackjack
from basicStrategyBlackJack import BasicStrategyChart
import gymnasium as gym

MAX_TOTAL_ROUNDS = 1000000
env = gym.make('blackjack/BlackJack-v0.1.1', natural=True, peek=True)
rewards = 0
for i in range(MAX_TOTAL_ROUNDS):
    print(i)
    turn = 0
    obs, info = env.reset()
    print(obs)
    while True:
        if obs[3] == 1:
            if obs[2] == 1:
                action = BasicStrategyChart.pair_hand[0][obs[1] - 2].value
            else:
                action = BasicStrategyChart.pair_hand[int(obs[0] / 2) - 1][obs[1] - 2].value
        elif obs[2] == 1:
            action = BasicStrategyChart.soft_hand[obs[0] - 13][obs[1] - 2].value
        else:
            action = BasicStrategyChart.hard_hand[obs[0] - 5][obs[1] - 2].value
        if action == 4 and not info["action_mask"][4]:
            action = 1
        if action == 3 and not info["action_mask"][3]:
            action = 1
        if action == 2 and not info["action_mask"][2]:
            if obs[0] == 18:
                action = 0
            else:
                action = 1
        obs, reward, terminated, truncated, info = env.step(action)
        turn += 1
        print(obs, terminated, reward)
        if terminated or truncated:
            rewards += reward
            break

env.close()
avg_reward = rewards / MAX_TOTAL_ROUNDS
print("Average Reward:", avg_reward)
