# Overview
This is a project that implements an Alpha-Beta Pruning-based game agent for 5x5 Tic-Tac-Toe game requiring 4-in-a-line to win.

The game logic is implemented as a class called `Game` in the `game.py` file, and the `AlphaBetaAgent` as well as 3 other agents, `RandomAgent`, a `NoisyHeuristicAgent` and `HumanAgent` is implemented in `agents.py`.

Running `main.py` will start 40 games, 10 games each of the following configurations (match-ups):
- `AlphaBetaAgent` as `X` vs `RandomAgent` as `O`
- `RandomAgent` as `X` vs `AlphaBetaAgent` as `O`
- `AlphaBetaAgent` as `X` vs `NoisyHeuristicAgent` as `O`
- `NoisyHeuristicAgent` as `X` vs `AlphaBetaAgent` as `O`

The state of each game is printed in the terminal as the game progresses and saved in a `log file` with the format of `Game_{game_number}_{playerX_agent}_vs_{playerO_agent}.txt`, e.g. `Game_3_AlphaBeta_vs_Random.txt`. These files are stored in a directory whose default is `./logs/`.

At the end of all 40 games, a summary with the following metrics is printed to the terminal and saved in a `summary.txt` and `summary.csv` file within the `./logs/` directory:
- Outcome for each game: `Win`/`Loss`/`Draw` for the `AlphaBetaAgent`.
- Node Expansions: Total number of nodes expanded by the `AlphaBetaAgent` during 1 game.
- Computational Time: Wall-clock time (in seconds) for the `AlphaBetaAgent` total thinking time per game.
- Game Length: Number of moves until termination of the game.

# Setup and Dependencies
This project does not utilise any additional libraries outside of the Python Standard Library.

The project has been tested using `Python version 3.12.3`

`pip install -r requirements.txt` is not required to run.

Simply unzip the folder containing `main.py`, `game.py`, and `agents.py` and ensure these 3 files
are in the same directory.

# How To Run
To run the 40 games, use the command:
```
python main.py
```
Upon execution, the game progress will be printed on the terminal. Once all 40 games have completed, a summary of the 4 metrics will be displayed on the terminal. Summary and detailed logs of each game can also be found under the default directory `./logs/`.

Additional testing can be done by executing `game.py` and `agents.py`.

Running the command:
```
python game.py
```
will play a game with the moves as defined in `sequence[]` inside the function `main()`. This is used for manually testing the heuristic function and observing how the each grid cell values change under different states.

Running the command:
```
python agents.py
```
will play a game with the agents as defined as `playerX` and `playerO` inside the function `main()`. You can play against any of the agents by setting either `playerX` or `playerO` as a `HumanAgent` object.

# Documentation
Detailed documentation of the code such as class attributes and methods, their parameters and returns etc. can be found within each python file.