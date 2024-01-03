import gymnasium as gym
from BlackjackEnv import BlackjackEnv

env = BlackjackEnv()
observation, info = env.reset()
print(observation)

for _ in range(10):
    while True:
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)
        print(observation)
        if terminated or truncated:
            observation, info = env.reset()
            print(observation)
            break

env.close()