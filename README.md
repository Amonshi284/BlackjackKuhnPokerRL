Overview

This repository contains two custom OpenAI Gymnasium environments for the card games Kuhn Poker and Blackjack. Additionally, it includes several exemplary evaluation functions to demonstrate how to interact with and evaluate policies within these environments.
Environments
Kuhn Poker

Kuhn Poker is a simplified poker game involving only three cards and two players. The rules are simplified as follows:

- Each player antes one chip.
- Each player is dealt one card from a deck of three cards.
- Players take turns to bet or fold.
- The game ends after one betting round, and the player betting against a fold or otherwise with the highest card wins the pot.

Features

- Simple rules for easy implementation and understanding.
- Perfect for testing basic reinforcement learning algorithms.
- Minimal state and action spaces, facilitating faster learning.

Blackjack

Blackjack is a classic card game where the goal is to beat the dealer by having a hand value as close to 21 as possible without exceeding it.
Features

- Standard rules of Blackjack with dealer playing according to fixed strategies.
- Includes options for varying the number of decks, reshuffling policies, and betting strategies.
- Supports multiple variations such as splitting, doubling down, and insurance.

Installation

To install the environments, clone the repository and install the dependencies using pip:

    git clone https://github.com/yourusername/game-gymnasium-envs.git
    cd game-gymnasium-envs
    pip install -r requirements.txt

To use the environments, import them and create instances as follows:

    import kuhnpokerenv.kuhnpoker
    import gymnasium as gym

    env = gym.make("kuhnpoker/KuhnPoker-v0")

A PPO Agent trained with parameters learning_rate=0.00015 and net_arch=dict(pi=[32, 32], vf=[32, 32]) in 2 million timesteps can reach an average reward of -0,01193 with deterministic set to True.
In Kuhn Poker for example different parametervariations of PPO can reach around the best possible average reward as the starting player against the optimal strategy as seen in the graph.
![grafik](https://github.com/Amonshi284/BlackjackKuhnPokerRL/assets/16608842/85244246-7dad-49c1-ad76-53e895765f0a)
