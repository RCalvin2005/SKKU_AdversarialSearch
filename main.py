import random
import os
import game
import agents

def main(): 
    """
    Plays and records the results of 40 games.
    10 games where AlphaBeta Agent plays as X (first player) against RandomAgent.
    10 games where AlphaBeta Agent plays as O (second player) against RandomAgent.
    10 games where AlphaBeta Agent plays as X (first player) against NoisyHeuristicAgent.
    10 games where AlphaBeta Agent plays as O (second player) against NoisyHeuristicAgent.
    """
    GAMES_PER_ROUND = 10

    DEPTH_LIMIT = 4
    ENFORCE_TIME_LIMIT = True

    summary_file = "summary" # Name of the file containing the summary of all games
    log_folder = "./logs/"
    os.makedirs(log_folder, exist_ok=True)

    # Game metrics
    metrics = {
        "AB_outcome" : [], # Game outcome for AlphaBetaAgent
        "node_expansions" : [], # Total number of nodes expanded by AlphaBetaAgent
        "comp_time" : [], # Total computational time by AlphaBetaAgent
        "game_length" : [], # Total number of turns until game ends
    }

    # Play 10 games where AlphaBeta Agent plays as X (first player) against RandomAgent
    for i in range(GAMES_PER_ROUND):
        log_file = f"{log_folder}Game_{i}_AlphaBeta_vs_Random.txt"
        file_headline = f"Game {i+1}: AlphaBetaAgent (X) vs RandomAgent (O)"

        random.seed(i)
        game_obj = game.Game()
        
        playerX = agents.AlphaBetaAgent(game_obj, "X", DEPTH_LIMIT, ENFORCE_TIME_LIMIT)
        playerO = agents.RandomAgent(game_obj, "O")

        play_game(game_obj, playerX, playerO, log_file)

        save_metrics(game_obj, playerX, metrics, log_file, file_headline)

    # Play 10 games where AlphaBeta Agent plays as O (second player) against RandomAgent
    for i in range(GAMES_PER_ROUND):
        log_file = f"{log_folder}Game_{i + GAMES_PER_ROUND*1}_Random_vs_AlphaBeta.txt"
        file_headline = f"Game {i+1}: RandomAgent (X) vs AlphaBetaAgent (O)"

        random.seed(i)
        game_obj = game.Game()
        
        playerX = agents.RandomAgent(game_obj, "X")
        playerO = agents.AlphaBetaAgent(game_obj, "O", DEPTH_LIMIT, ENFORCE_TIME_LIMIT)

        play_game(game_obj, playerX, playerO, log_file)

        save_metrics(game_obj, playerO, metrics, log_file, file_headline)

    # Play 10 games where AlphaBeta Agent plays as X (first player) against RandomAgent
    for i in range(GAMES_PER_ROUND):
        log_file = f"{log_folder}Game_{i + GAMES_PER_ROUND*2}_AlphaBeta_vs_Heuristic.txt"
        file_headline = f"Game {i+1}: AlphaBetaAgent (X) vs NoisyHeuristicAgent (O)"

        random.seed(i)
        game_obj = game.Game()
        
        playerX = agents.AlphaBetaAgent(game_obj, "X", DEPTH_LIMIT, ENFORCE_TIME_LIMIT)
        playerO = agents.NoisyHeuristicAgent(game_obj, "O")

        play_game(game_obj, playerX, playerO, log_file)

        save_metrics(game_obj, playerX, metrics, log_file, file_headline)

    # Play 10 games where AlphaBeta Agent plays as O (second player) against RandomAgent
    for i in range(GAMES_PER_ROUND):
        log_file = f"{log_folder}Game_{i + GAMES_PER_ROUND*3}_Heuristic_vs_AlphaBeta.txt"
        file_headline = f"Game {i+1}: NoisyHeuristicAgent (X) vs AlphaBetaAgent (O)"

        random.seed(i)
        game_obj = game.Game()
        
        playerX = agents.NoisyHeuristicAgent(game_obj, "X")
        playerO = agents.AlphaBetaAgent(game_obj, "O", DEPTH_LIMIT, ENFORCE_TIME_LIMIT)

        play_game(game_obj, playerX, playerO, log_file)

        save_metrics(game_obj, playerO, metrics, log_file, file_headline)

    print("\n")
    save_csv(metrics, log_folder+summary_file+".csv")
    save_summary(metrics, GAMES_PER_ROUND, log_folder+summary_file+".txt")

    print(f"Please refer to the log files in {log_folder} for summary and detailed log of each game.")

    return


def play_game(game : game.Game, playerX, playerO, log_file):
    """
    Plays an entire game of Tic Tac Toe while printing out the progress and logging into a file.

    Parameters
    ----------
    game : Game
        The game object to be played on and its related attributes and methods.
    playerX : Agent
        The agent playing as X in the game.
    playerO : Agent
        The agent playing as X in the game.
    log_file : str
        Location and name of file to store the game log to.

    Returns
    -------
    str
        Winner of the game ("X", "O", or "Draw").
    """
    game_over = False
    winner = ""
    row = 0
    col = 0
    mark = 0

    print(f"Starting Game: {playerX.label} as X vs {playerO.label} as O")
    print("-"*75)
    with open(log_file, "w") as f:
        f.write(f"Starting Game: {playerX.label} as X vs {playerO.label} as O\n")
        f.write("-"*75 + "\n")

        while not game_over:
            # Check which player's turn it is
            if game.turn_num % 2 == 0:
                curr_player = playerX
            else:
                curr_player = playerO

            # Print/save turn number and player
            print(f"Turn #{game.turn_num + 1}: {curr_player.label}")
            f.write(f"Turn #{game.turn_num + 1}: {curr_player.label}\n")
            
            # Let agent play a move
            row, col, mark, played_random = curr_player.play()

            # Save additional stats for AlphaBetaAgent
            if isinstance(curr_player, agents.AlphaBetaAgent):
                if played_random:
                    f.write("Time limit exceeded!\n")
                else:
                    f.write(f"Move computation time: {curr_player.move_comp_time:.3f}s\n")
                    f.write(f"Move value: {curr_player.move_value}\n")
                f.write(f"Nodes explored: {curr_player.move_node_count}\n")

            # Print and save grid with cell values
            state_val = game.get_state_val()
            print(f"\nGame state value: {state_val}")
            game.display_cell_val()
            print()
            f.write(f"\nGame state value: {state_val}\n")
            grid_str = game.format_cell_val_str()
            f.write(grid_str + "\n")

            # Print and save move made
            if played_random:
                print(f"{curr_player.label} {mark} played a random move!")
                f.write(f"{curr_player.label} {mark} played a random move!\n")
            print(f"{curr_player.label} placed {mark} in ({row}, {col})")
            f.write(f"{curr_player.label} placed {mark} in ({row}, {col})" + "\n")

            # Print and save game outcome
            if game.is_winning_move():
                print(f"{curr_player.label} {mark} has won the game.")
                f.write(f"{curr_player.label} {mark} has won the game." + "\n")
                winner = mark
                game_over = True
            elif game.is_over():
                print("The game ended in a draw!")
                f.write("The game ended in a draw!" + "\n")
                winner = "Draw"
                game_over = True

            print("-"*75)
            f.write("-"*75 + "\n")

    
    return winner


def save_metrics(game : game.Game, ABplayer:agents.AlphaBetaAgent, metrics, log_file, file_headline):
    """
    Saves the game metrics into the top of the log file and metrics dicitonary.

    Parameters
    ----------
    game : Game
        The game object with a completed game.
    ABplayer : AlphaBetaAgent
        The AlphaBetaAgent that played the game.
    metrics : dict[list[str, int, float, int, float]]
        Dicitonary where the game metrics are stored.
    log_file : str
        Location and name of file to store the game log to.
    file_headline : str
        Headline to be written at the top of the file.
    """
    
    # Make copy of log file contents
    with open(log_file, "r") as f:
        contents = f.read()

    # Save summary and metrics into start of file
    with open(log_file, "w") as f:
        f.write(file_headline + "\n")
        f.write("\nSummary and Stats")
        f.write("\n=================\n")

        winner = game.winner
        if winner == "Draw":
            outcome = winner
        elif winner == ABplayer.mark:
            outcome = "Win"
        else:
            outcome = "Loss"
        f.write(f"Outcome: {outcome}\n")
        metrics["AB_outcome"].append(outcome)

        f.write(f"Node Expansions: {ABplayer.total_node_count}\n")
        metrics["node_expansions"].append(ABplayer.total_node_count)

        f.write(f"Computation Time: {ABplayer.total_comp_time:.3f}s\n")
        metrics["comp_time"].append(ABplayer.total_comp_time)

        f.write(f"Game Length: {game.turn_num}\n")
        metrics[f"game_length"].append(game.turn_num)

        # Save end board state
        f.write(f"\nEnd board state:\n")
        f.write(game.format_grid_str())

        f.write("\n\nGame Log")
        f.write("\n=========\n\n")
        
        f.write(contents)

    return


def save_csv(metrics, csv_file):
    """
    Saves the metrics into a csv file.

    Parameters
    ----------
    metrics : dict[list[str, int, float, int, float]]
        Dicitonary where the game metrics are stored.
    csv_file : str
        Name of the csv file to store the game metrics to.
    """
    headers = ["Outcome", "Node Expansions", "Computational Time", "Game Length"]
    with open(csv_file, "w") as f:
        f.write(",".join(headers) + ",\n")
        for i in range(len(metrics["AB_outcome"])):
            f.write(f"{metrics["AB_outcome"][i]},{metrics["node_expansions"][i]},")
            f.write(f"{metrics["comp_time"][i]:.3f},{metrics["game_length"][i]},\n")


def tabulate_stats(metrics, games_per_round, round):
    """
    Formats the stats for 1 game set into a single string containing a table

    Parameters
    ----------
    metrics : dict[list[str, int, float, int, float]]
        Dicitonary where the game metrics are stored.
    games_per_round : int
        Number of games per round of opponent combinations.
    round : int
        Round number (0 to 3).

    Returns
    -------
    str
        String containing a table with the round summary.
    """
    
    start_game = round * games_per_round

    summary =  "+=========+=========+=================+====================+=============+\n"
    summary += "|  Game   | Outcome | Node Expansions | Computational Time | Game Length |\n"
    summary += "+=========+=========+=================+====================+=============+\n"
    for i in range(start_game, start_game+games_per_round):
        summary += f"| Game {i:<2} |{metrics["AB_outcome"][i]:>6}   |{metrics["node_expansions"][i]:>14}   "
        summary += f"|{metrics["comp_time"][i]:>16.3f}s   |{metrics["game_length"][i]:>10}   |\n"
        summary +=  "+---------+---------+-----------------+--------------------+-------------+\n"

    return summary


def save_summary(metrics, games_per_round, summary_file):
    """
    Prints out and saves the summary metrics of all the games.

    Parameters
    ----------
    metrics : dict[list[str, int, float, int, float]]
        Dicitonary where the game metrics are stored.
    games_per_round : int
        Number of games per round of opponent combinations
    summary_file : str
        Name of the file to store the game summary to.
    """
    round_headers = [
        "Round 1: AlphaBeta (X) vs Random (O)",
        "Round 2: Random (O) vs AlphaBeta (X)",
        "Round 3: AlphaBeta (X) vs NoisyHeuristic (O)",
        "Round 4: NoisyHeuristic (O) vs AlphaBeta (X)",
    ]

    with open(summary_file, "w") as f:
        print("Summary")
        print("=======\n")

        f.write("Summary\n=======\n\n")

        for round in range(len(round_headers)):
            print(round_headers[round])
            f.write(round_headers[round]+"\n")

            wins = 0
            losses = 0
            draws = 0
            total_node_expansions = 0
            total_comp_time = 0
            total_game_length = 0
            for game in range(games_per_round):
                outcome = metrics["AB_outcome"][round*games_per_round + game]
                if outcome == "Win":
                    wins += 1
                elif outcome == "Loss":
                    losses += 1
                else:
                    draws += 1

                total_node_expansions += metrics["node_expansions"][round*games_per_round + game]
                total_comp_time += metrics["comp_time"][round*games_per_round + game]
                total_game_length += metrics["game_length"][round*games_per_round + game]

            print(f"Total wins: {wins}")
            f.write(f"Total wins: {wins}\n")

            print(f"Total draws: {draws}")
            f.write(f"Total draws: {draws}\n")

            print(f"Total losses: {losses}")
            f.write(f"Total losses: {losses}\n")

            avg_expansion = total_node_expansions / games_per_round
            print(f"Average node expansion: {avg_expansion:.0f}")
            f.write(f"Average node expansion: {avg_expansion:.0f}\n")

            avg_time = total_comp_time / games_per_round
            print(f"Average computational time: {avg_time:.3f}s")
            f.write(f"Average computational time: {avg_time:.3f}s\n")

            avg_length = total_game_length / games_per_round
            print(f"Average game_length: {avg_length:.0f}")
            f.write(f"Average game_length: {avg_length:.0f}\n")

            table = tabulate_stats(metrics, games_per_round, round)
            print("\n" + table)
            f.write("\n" + table + "\n")

            print("-"*75 + "\n")
            f.write("-"*75 + "\n\n")


if __name__ == "__main__":
    main()