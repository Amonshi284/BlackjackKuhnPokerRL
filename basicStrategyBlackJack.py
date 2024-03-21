from enum import Enum


class Moves(Enum):
    S = 0
    H = 1
    D = 2
    P = 3
    R = 4


class BasicStrategyChart:
    hard_hand = [
        # Dealers open card
        #   2        3        4        5        6        7        8        9       10        A
        [Moves.H, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H],
        [Moves.H, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H],
        [Moves.H, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H],
        [Moves.H, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H],
        [Moves.H, Moves.D, Moves.D, Moves.D, Moves.D, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H],
        [Moves.D, Moves.D, Moves.D, Moves.D, Moves.D, Moves.D, Moves.D, Moves.D, Moves.H, Moves.H],
        [Moves.D, Moves.D, Moves.D, Moves.D, Moves.D, Moves.D, Moves.D, Moves.D, Moves.D, Moves.H],
        [Moves.H, Moves.H, Moves.S, Moves.S, Moves.S, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H],
        [Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H],
        [Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H],
        [Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.H, Moves.H, Moves.H, Moves.R, Moves.H],
        [Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.H, Moves.H, Moves.R, Moves.R, Moves.R],
        [Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S],
        [Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S],
        [Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S],
        [Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S],
        [Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S],
    ]
    soft_hand = [
        # Dealers open card
        #   2        3        4        5        6        7        8        9       10        A
        [Moves.H, Moves.H, Moves.H, Moves.D, Moves.D, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H],  # 13
        [Moves.H, Moves.H, Moves.H, Moves.D, Moves.D, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H],  # 14
        [Moves.H, Moves.H, Moves.D, Moves.D, Moves.D, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H],  # 15
        [Moves.H, Moves.H, Moves.D, Moves.D, Moves.D, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H],  # 16
        [Moves.H, Moves.D, Moves.D, Moves.D, Moves.D, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H],  # 17
        [Moves.S, Moves.D, Moves.D, Moves.D, Moves.D, Moves.S, Moves.S, Moves.H, Moves.H, Moves.H],  # 18
        [Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S],  # 19
        [Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S],  # 20
        [Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S],  # 21
    ]
    pair_hand = [
        # Dealers open card
        #   2        3        4        5        6        7        8        9       10        A
        [Moves.P, Moves.P, Moves.P, Moves.P, Moves.P, Moves.P, Moves.P, Moves.P, Moves.P, Moves.P],  # A
        [Moves.P, Moves.P, Moves.P, Moves.P, Moves.P, Moves.P, Moves.H, Moves.H, Moves.H, Moves.H],  # 2
        [Moves.P, Moves.P, Moves.P, Moves.P, Moves.P, Moves.P, Moves.H, Moves.H, Moves.H, Moves.H],  # 3
        [Moves.H, Moves.H, Moves.H, Moves.P, Moves.P, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H],  # 4
        [Moves.D, Moves.D, Moves.D, Moves.D, Moves.D, Moves.D, Moves.D, Moves.D, Moves.H, Moves.H],  # 5
        [Moves.P, Moves.P, Moves.P, Moves.P, Moves.P, Moves.H, Moves.H, Moves.H, Moves.H, Moves.H],  # 6
        [Moves.P, Moves.P, Moves.P, Moves.P, Moves.P, Moves.P, Moves.H, Moves.H, Moves.H, Moves.H],  # 7
        [Moves.P, Moves.P, Moves.P, Moves.P, Moves.P, Moves.P, Moves.P, Moves.P, Moves.P, Moves.P],  # 8
        [Moves.P, Moves.P, Moves.P, Moves.P, Moves.P, Moves.S, Moves.P, Moves.P, Moves.S, Moves.S],  # 9
        [Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S, Moves.S],  # 10

    ]
