import os
from typing import Optional
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from gymnasium.error import DependencyNotInstalled


def cmp(a, b):
    return float(a > b) - float(a < b)


deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]


def draw_card(np_random):
    return int(np_random.choice(deck))


def draw_hand(np_random):
    return [draw_card(np_random), draw_card(np_random)]


def usable_ace(hand):  # Does this hand have a usable ace?
    return int(1 in hand and sum(hand) + 10 <= 21)


def pair_in_hand(hand):
    return len(hand) == 2 and hand[0] == hand[1]


def sum_hand(hand):  # Return current hand total
    if usable_ace(hand):
        return sum(hand) + 10
    return sum(hand)


def is_bust(hand):  # Is this hand a bust?
    return sum_hand(hand) > 21


def score(hand):  # What is the score of this hand (0 if bust)
    return 0 if is_bust(hand) else sum_hand(hand)


def is_natural(hand):  # Is this hand a natural blackjack?
    return sorted(hand) == [1, 10]


def is_terminated(player, player2, player3, terminated2, terminated3):
    terminated = False
    if len(player2) > 0 and not terminated2:
        temp = player
        player = player2
        player2 = temp
        terminated2 = True
    elif len(player3) > 0 and not terminated3:
        temp = player
        player = player3
        player3 = temp
        terminated3 = True
    else:
        terminated = True
    return player, player2, player3, terminated, terminated2, terminated3


class BlackjackEnv(gym.Env):
    metadata = {
        "render_modes": ["human", "rgb_array"],
        "render_fps": 4,
    }

    def __init__(self, render_mode: Optional[str] = None, natural=False, sab=False):
        self.action_space = spaces.Discrete(5)
        # Player hand, dealer hand, soft ace in player hand, pair in player hand
        self.observation_space = spaces.MultiDiscrete(np.array([32, 32, 2, 2]))

        # Flag to payout 1.5 on a "natural" blackjack win, like casino rules
        # Ref: http://www.bicyclecards.com/how-to-play/blackjack/
        self.natural = natural

        # Flag for full agreement with the (Sutton and Barto, 2018) definition. Overrides self.natural
        self.sab = sab

        self.render_mode = render_mode

    def step(self, action):
        assert self.action_space.contains(action)
        terminated = False
        if action == 1:  # hit: add a card to players hand and return
            self.player.append(draw_card(self.np_random))
            if is_bust(self.player):
                self.player, self.player2, self.player3, terminated, self.terminated2, self.terminated3 = is_terminated(
                    self.player, self.player2, self.player3, self.terminated2, self.terminated3
                )
                self.reward += -1.0
        elif action == 0:  # stick: play out the dealers hand, and score
            self.player, self.player2, self.player3, terminated, self.terminated2, self.terminated3 = is_terminated(
                self.player, self.player2, self.player3, self.terminated2, self.terminated3
            )
            while sum_hand(self.dealer) < 17:
                self.dealer.append(draw_card(self.np_random))
            if self.sab and is_natural(self.player) and not is_natural(self.dealer):
                # Player automatically wins. Rules consistent with S&B
                self.reward += 1.0
            elif (
                    not self.sab
                    and self.natural
                    and is_natural(self.player)
            ):
                # Natural gives extra points, but doesn't autowin. Legacy implementation
                self.reward += 1.5
            else:
                self.reward += cmp(score(self.player), score(self.dealer))
        elif action == 2:  # double down: add a card to players hand, double bet, play out dealers hand and score
            self.player.append(draw_card(self.np_random))
            if is_bust(self.player):
                self.reward += -2.0
            else:
                while sum_hand(self.dealer) < 17:
                    self.dealer.append(draw_card(self.np_random))
                if self.sab and is_natural(self.player) and not is_natural(self.dealer):
                    # Player automatically wins. Rules consistent with S&B
                    self.reward += 2.0
                elif (
                        not self.sab
                        and self.natural
                        and is_natural(self.player)
                ):
                    # Natural gives extra points, but doesn't autowin. Legacy implementation
                    self.reward += 3.0
                else:
                    self.reward += cmp(score(self.player), score(self.dealer)) * 2.0
            self.player, self.player2, self.player3, terminated, self.terminated2, self.terminated3 = is_terminated(
                self.player, self.player2, self.player3, self.terminated2, self.terminated3
            )
        elif action == 3:  # split: only possible with two cards of same rank, split hand in two, place second bet for
            # second hand, play hands after another
            if len(self.player) == 2 and self.player[0] == self.player[1] and len(self.player2) == 0:
                self.player2.append(self.player.pop())
                self.player2.append(draw_card(self.np_random))
                self.player.append(draw_card(self.np_random))
            elif len(self.player) == 2 and self.player[0] == self.player[1] and len(self.player3) == 0:
                self.player3.append(self.player.pop())
                self.player3.append(draw_card(self.np_random))
                self.player.append(draw_card(self.np_random))
            # else:
                # print("Split is only possible with two cards of the same rank.")
        elif action == 4:  # surrender: only in first turn of hand, give up hand and get back half of bet
            if len(self.player) == 2 and len(self.player2) == 0:
                self.reward += -0.5
                terminated = True
            else:
                terminated = False
                # print("Surrender is only possible in the first turn of a hand.")

        if self.render_mode == "human":
            self.render()
        # truncation=False as the time limit is handled by the `TimeLimit` wrapper added during `make`
        return self._get_obs(terminated), self.reward, terminated, False, self._get_info()

    def _get_obs(self, terminated):
        if terminated:
            return np.array([sum_hand(self.player), sum_hand(self.dealer), usable_ace(self.player),
                             pair_in_hand(self.player)])
        else:
            return np.array([sum_hand(self.player), self.dealer[0], usable_ace(self.player), pair_in_hand(self.player)])

    def _get_info(self):
        return {"action_mask": [1, 1, 1, 1 if self._get_obs(False)[3] and len(self.player2) == 0 else 0,
                                1 if len(self.player) == 2 and len(self.player2) == 0 else 0]}

    def action_mask(self):
        return self._get_info()["action_mask"]

    def reset(
            self,
            seed: Optional[int] = None,
            options: Optional[dict] = None,
    ):
        super().reset(seed=seed)
        self.dealer = draw_hand(self.np_random)
        self.player = draw_hand(self.np_random)
        self.player2 = []
        self.player3 = []

        self.reward = 0
        self.terminated2 = False
        self.terminated3 = False

        _, dealer_card_value, _, _ = self._get_obs(False)

        suits = ["C", "D", "H", "S"]
        self.dealer_top_card_suit = self.np_random.choice(suits)

        if dealer_card_value == 1:
            self.dealer_top_card_value_str = "A"
        elif dealer_card_value == 10:
            self.dealer_top_card_value_str = self.np_random.choice(["J", "Q", "K"])
        else:
            self.dealer_top_card_value_str = str(dealer_card_value)

        if self.render_mode == "human":
            self.render()
        return self._get_obs(False), self._get_info()

    def render(self):
        if self.render_mode is None:
            assert self.spec is not None
            gym.logger.warn(
                "You are calling render method without specifying any render mode. "
                "You can specify the render_mode at initialization, "
                f'e.g. gym.make("{self.spec.id}", render_mode="rgb_array")'
            )
            return

        try:
            import pygame
        except ImportError as e:
            raise DependencyNotInstalled(
                "pygame is not installed, run `pip install gymnasium[toy-text]`"
            ) from e

        player_sum, dealer_card_value, usable_ace, player_pair = self._get_obs(terminated=False)
        screen_width, screen_height = 600, 500
        card_img_height = screen_height // 3
        card_img_width = int(card_img_height * 142 / 197)
        spacing = screen_height // 20

        bg_color = (7, 99, 36)
        white = (255, 255, 255)

        if not hasattr(self, "screen"):
            pygame.init()
            if self.render_mode == "human":
                pygame.display.init()
                self.screen = pygame.display.set_mode((screen_width, screen_height))
            else:
                pygame.font.init()
                self.screen = pygame.Surface((screen_width, screen_height))

        if not hasattr(self, "clock"):
            self.clock = pygame.time.Clock()

        self.screen.fill(bg_color)

        def get_image(path):
            cwd = os.path.dirname(__file__)
            image = pygame.image.load(os.path.join(cwd, path))
            return image

        def get_font(path, size):
            cwd = os.path.dirname(__file__)
            font = pygame.font.Font(os.path.join(cwd, path), size)
            return font

        small_font = get_font(
            os.path.join("font", "Minecraft.ttf"), screen_height // 15
        )
        dealer_text = small_font.render(
            "Dealer: " + str(dealer_card_value), True, white
        )
        dealer_text_rect = self.screen.blit(dealer_text, (spacing, spacing))

        def scale_card_img(card_img):
            return pygame.transform.scale(card_img, (card_img_width, card_img_height))

        dealer_card_img = scale_card_img(
            get_image(
                os.path.join(
                    "img",
                    f"{self.dealer_top_card_suit}{self.dealer_top_card_value_str}.png",
                )
            )
        )
        dealer_card_rect = self.screen.blit(
            dealer_card_img,
            (
                screen_width // 2 - card_img_width - spacing // 2,
                dealer_text_rect.bottom + spacing,
            ),
        )

        hidden_card_img = scale_card_img(get_image(os.path.join("img", "Card.png")))
        self.screen.blit(
            hidden_card_img,
            (
                screen_width // 2 + spacing // 2,
                dealer_text_rect.bottom + spacing,
            ),
        )

        player_text = small_font.render("Player", True, white)
        player_text_rect = self.screen.blit(
            player_text, (spacing, dealer_card_rect.bottom + 1.5 * spacing)
        )

        large_font = get_font(os.path.join("font", "Minecraft.ttf"), screen_height // 6)
        player_sum_text = large_font.render(str(player_sum), True, white)
        player_sum_text_rect = self.screen.blit(
            player_sum_text,
            (
                screen_width // 2 - player_sum_text.get_width() // 2,
                player_text_rect.bottom + spacing,
            ),
        )

        if usable_ace:
            usable_ace_text = small_font.render("usable ace", True, white)
            self.screen.blit(
                usable_ace_text,
                (
                    screen_width // 2 - usable_ace_text.get_width() // 2,
                    player_sum_text_rect.bottom + spacing // 2,
                ),
            )
        if player_pair:
            player_pair_text = small_font.render("pair in hand", True, white)
            self.screen.blit(
                player_pair_text,
                (
                    screen_width // 2 - player_pair_text.get_width() // 2,
                    player_sum_text_rect.bottom + spacing // 2,
                ),
            )
        if self.render_mode == "human":
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        else:
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
            )

    def close(self):
        if hasattr(self, "screen"):
            import pygame

            pygame.display.quit()
            pygame.quit()
