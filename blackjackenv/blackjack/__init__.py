from gymnasium.envs.registration import register

register(
    id="blackjack/BlackJack-v0.1.1",
    entry_point="blackjackenv.blackjack.envs:BlackjackEnv",
    nondeterministic=True
)
