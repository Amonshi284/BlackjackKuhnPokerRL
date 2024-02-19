from enum import Enum


class Moves(Enum):
    S = 0
    H = 1
    D = 2
    P = 3
    R = 4


class BasicStrategyChart:
    hard_hand = [
        [Moves.H.value, Moves.H.value, Moves.H.value, Moves.H.value, Moves.H.value, Moves.H.value, Moves.H.value,
         Moves.H.value, Moves.H.value, Moves.H.value],
        [Moves.H.value, Moves.H.value, Moves.H.value, Moves.H.value, Moves.H.value, Moves.H.value, Moves.H.value,
         Moves.H.value, Moves.H.value, Moves.H.value],
        [Moves.H.value, Moves.H.value, Moves.H.value, Moves.H.value, Moves.H.value, Moves.H.value, Moves.H.value,
         Moves.H.value, Moves.H.value, Moves.H.value],
        [Moves.H.value, Moves.H.value, Moves.H.value, Moves.H.value, Moves.H.value, Moves.H.value, Moves.H.value,
         Moves.H.value, Moves.H.value, Moves.H.value],
        [Moves.H.value, Moves.D.value, Moves.D.value, Moves.D.value, Moves.D.value, Moves.H.value, Moves.H.value,
         Moves.H.value, Moves.H.value, Moves.H.value],
        [Moves.D.value, Moves.D.value, Moves.D.value, Moves.D.value, Moves.D.value, Moves.D.value, Moves.D.value,
         Moves.D.value, Moves.H.value, Moves.H.value],
        [Moves.D.value, Moves.D.value, Moves.D.value, Moves.D.value, Moves.D.value, Moves.D.value, Moves.D.value,
         Moves.D.value, Moves.D.value, Moves.H.value],
        [Moves.H.value, Moves.H.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.H.value, Moves.H.value,
         Moves.H.value, Moves.H.value, Moves.H.value],
        [Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.H.value, Moves.H.value,
         Moves.H.value, Moves.H.value, Moves.H.value],
        [Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.H.value, Moves.H.value,
         Moves.H.value, Moves.H.value, Moves.H.value],
        [Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.H.value, Moves.H.value,
         Moves.H.value, Moves.R.value, Moves.H.value],
        [Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.H.value, Moves.H.value,
         Moves.R.value, Moves.R.value, Moves.R.value],
        [Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value,
         Moves.S.value, Moves.S.value, Moves.S.value],
        [Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value,
         Moves.S.value, Moves.S.value, Moves.S.value],
        [Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value,
         Moves.S.value, Moves.S.value, Moves.S.value],
        [Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value,
         Moves.S.value, Moves.S.value, Moves.S.value],
        [Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value,
         Moves.S.value, Moves.S.value, Moves.S.value],
    ]
    soft_hand = [
        [Moves.H.value, Moves.H.value, Moves.H.value, Moves.D.value, Moves.D.value, Moves.H.value, Moves.H.value,
         Moves.H.value, Moves.H.value, Moves.H.value],
        [Moves.H.value, Moves.H.value, Moves.H.value, Moves.D.value, Moves.D.value, Moves.H.value, Moves.H.value,
         Moves.H.value, Moves.H.value, Moves.H.value],
        [Moves.H.value, Moves.H.value, Moves.D.value, Moves.D.value, Moves.D.value, Moves.H.value, Moves.H.value,
         Moves.H.value, Moves.H.value, Moves.H.value],
        [Moves.H.value, Moves.H.value, Moves.D.value, Moves.D.value, Moves.D.value, Moves.H.value, Moves.H.value,
         Moves.H.value, Moves.H.value, Moves.H.value],
        [Moves.H.value, Moves.D.value, Moves.D.value, Moves.D.value, Moves.D.value, Moves.H.value, Moves.H.value,
         Moves.H.value, Moves.H.value, Moves.H.value],
        [Moves.S.value, Moves.D.value, Moves.D.value, Moves.D.value, Moves.D.value, Moves.S.value, Moves.S.value,
         Moves.H.value, Moves.H.value, Moves.H.value],
        [Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value,
         Moves.S.value, Moves.S.value, Moves.S.value],
        [Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value,
         Moves.S.value, Moves.S.value, Moves.S.value],
        [Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value,
         Moves.S.value, Moves.S.value, Moves.S.value],
    ]
    pair_hand = [
        [Moves.P.value, Moves.P.value, Moves.P.value, Moves.P.value, Moves.P.value, Moves.P.value, Moves.P.value,
         Moves.P.value, Moves.P.value, Moves.P.value],
        [Moves.P.value, Moves.P.value, Moves.P.value, Moves.P.value, Moves.P.value, Moves.P.value, Moves.H.value,
         Moves.H.value, Moves.H.value, Moves.H.value],
        [Moves.P.value, Moves.P.value, Moves.P.value, Moves.P.value, Moves.P.value, Moves.P.value, Moves.H.value,
         Moves.H.value, Moves.H.value, Moves.H.value],
        [Moves.H.value, Moves.H.value, Moves.H.value, Moves.P.value, Moves.P.value, Moves.H.value, Moves.H.value,
         Moves.H.value, Moves.H.value, Moves.H.value],
        [Moves.D.value, Moves.D.value, Moves.D.value, Moves.D.value, Moves.D.value, Moves.D.value, Moves.D.value,
         Moves.D.value, Moves.H.value, Moves.H.value],
        [Moves.P.value, Moves.P.value, Moves.P.value, Moves.P.value, Moves.P.value, Moves.H.value, Moves.H.value,
         Moves.H.value, Moves.H.value, Moves.H.value],
        [Moves.P.value, Moves.P.value, Moves.P.value, Moves.P.value, Moves.P.value, Moves.P.value, Moves.H.value,
         Moves.H.value, Moves.H.value, Moves.H.value],
        [Moves.P.value, Moves.P.value, Moves.P.value, Moves.P.value, Moves.P.value, Moves.P.value, Moves.P.value,
         Moves.P.value, Moves.P.value, Moves.P.value],
        [Moves.P.value, Moves.P.value, Moves.P.value, Moves.P.value, Moves.P.value, Moves.S.value, Moves.P.value,
         Moves.P.value, Moves.S.value, Moves.S.value],
        [Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value, Moves.S.value,
         Moves.S.value, Moves.S.value, Moves.S.value],

    ]
