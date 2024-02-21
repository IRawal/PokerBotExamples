# Poker Bot Workshop

Welcome to the Poker Bot Workshop! This repository contains the codebase for creating your own poker bot.

## Getting Started

This project is designed to help you understand the basics of creating a poker bot. You'll learn about game theory, decision trees, and more.

### Prerequisites

To get started, you'll need:

- Python 3.7 or later
- pip for package installation

You can install Python from [here](https://www.python.org/downloads/) and pip is included in Python 3.4 and later versions.

### Installation

Clone this repository to your local machine:

`git clone https://github.com/your_username/poker_bot_workshop.git`

`cd poker_bot_workshop`

`pip install -r requirements.txt`

`python engine.py`

# PokerBot Engine

           This is the engine code for a poker bot game. It manages the game procedure, logging, and communication with the poker bots.

## Usage

           To run the game, execute the `Game().run()` function in the `__main__` block.

## Features

           - Runs one round of poker at a time.
           - Manages logging of game events.
           - Communicates with the poker bots over a socket connection.
           - Handles actions such as folding, calling, checking, and raising.
           - Incorporates round state, player messages, and game log into the game procedure.

## Dependencies

           - `eval7`: A library for evaluating poker hands.

## Configuration

           - `PLAYER_1_NAME` and `PLAYER_2_NAME`: Names of the poker bots.
           - `PLAYER_1_PATH` and `PLAYER_2_PATH`: Paths to the poker bot scripts.
           - `NUM_ROUNDS`: Number of rounds to play.
           - `SMALL_BLIND` and `BIG_BLIND`: Blind amounts.
           - `STARTING_STACK`: Starting stack size.
           - `GAME_LOG_FILENAME`: Filename for the game log.

## License

           This code is licensed under the MIT License.
