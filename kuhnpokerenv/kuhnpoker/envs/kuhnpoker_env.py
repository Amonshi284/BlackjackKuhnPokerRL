import gymnasium as gym
import numpy
from gymnasium import spaces
import kuhnpokerenv.kuhnpoker.envs.optimal_agent_kuhn


class KuhnPokerEnv(gym.Env):
    def __init__(self):
        self.timestep = None
        self.done = None
        self.player = None
        self.player_act = None
        self.opponent = None
        self.alpha = 0.3
        self.opp_type = "optimal"
        self.opp_act = None
        self.start = "player"
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.MultiDiscrete([3, 3])

    def _get_obs(self):
        return numpy.array([self.player, self.opp_act])

    def _get_opp_act(self):
        if self.opp_type == "random":
            return self.np_random.integers(1, 3)
        else:
            return kuhnpokerenv.kuhnpoker.envs.optimal_agent_kuhn.get_optimal_action(obs=[self.opponent,
                                                                                          self.player_act],
                                                                                     start=self.start, alpha=self.alpha,
                                                                                     random=self.np_random)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        # 0 = Jack, 1 = Queen, 2 = King
        cards = [0, 1, 2]
        self.alpha = options["alpha"] if (options is not None and options.__contains__("alpha") and
                                          0 <= options["alpha"] <= 1 / 3) else self.alpha
        self.opp_type = options["opponent"] if options is not None and options.__contains__("opponent") else (
            self.opp_type)
        self.start = options["start"] if (options is not None and options.__contains__("start") and
                                          options["start"] in ("player", "opponent")) else self.start
        self.timestep = 0
        self.player_act = 0
        self.opp_act = 0
        self.done = False
        self.player = self.np_random.choice(cards)
        cards.remove(self.player)
        self.opponent = self.np_random.choice(cards)

        if self.start == "opponent":
            self.opp_act = self._get_opp_act()
            self.timestep += 1
        observation = self._get_obs()
        return observation, {}

    def step(self, action):
        reward = 0
        self.timestep += 1
        self.player_act = action + 1
        if self.start == "player" and self.timestep == 1:
            self.timestep += 1
            self.opp_act = self._get_opp_act()
        if self.player_act == self.opp_act == 1:
            self.done = True
            if self.opponent < self.player:
                reward = 1
            else:
                reward = -1
        elif self.player_act == self.opp_act == 2:
            self.done = True
            if self.opponent < self.player:
                reward = 2
            else:
                reward = -2
        elif self.player_act == 2 and self.opp_act == 1:
            if self.start == "player":
                self.done = True
                reward = 1
            else:
                self.opp_act = self._get_opp_act()
                self.done = True
                if self.opp_act == 2:
                    if self.opponent < self.player:
                        reward = 2
                    else:
                        reward = -2
                else:
                    reward = 1
        elif self.player_act == 1 and self.opp_act == 2:
            if self.start == "opponent" or self.timestep == 3:
                self.done = True
                reward = -1

        return self._get_obs(), reward, self.done, False, {}
