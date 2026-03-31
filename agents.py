import random
import copy
import time
import game
from abc import ABC, abstractmethod

class Agent(ABC):
    """
    An Abstract Base Class parent representing a agent playing the Tic-Tac-Toe game.

    Attributes:
    -----------
    game : Game
        The game object containing the grid and the related methods.
    mark : str
        The mark the agent is playing as.

    Methods
    -------
    play()
        Plays a single move for the game. To be implemented by each child separately and
        return the (row, col, mark, random_status) that was placed.
    """

    def __init__(self, game: game.Game, mark):
        self.game = game
        self.mark = mark

    @abstractmethod
    def play():
        return

class AlphaBetaAgent(Agent):
    """
    A class representing an agent that plays based on minimax algorithm with alpha-beta pruning.

    Attributes
    ----------
    game : Game
        The game object containing the grid and the related methods.
    mark : str
        The mark the agent is playing as.
    move_value : int
        Value of the most recent move.
    time_limit_exceeded : bool
        Used to check if time limit was exceeded
    total_comp_time : float
        Total time in seconds agent spent computing throughout the entire game.
    start_time : float (Class Variable)
        Starting time before minimax is executed.
    move_node_count : int (Class Variable)
        Number of nodes explored per move.
    total_node_count : int (Class Variable)
        Total number of nodes explored throughout the game.
    DEPTH_LIMIT : int
        The depth to which minimax search is performed.
    TIME_LIMIT : float
        Time in seconds minimax is allowed to compute before falling back to a random move.
    TIME_LIMIT_ENFORCED : bool
        Toggle for whether the above time limit is enforced or not.

    Notes
    -----
    The above class variables are used for easy syncing across the many recursion calls in
    minimax search. As they are class variables, the computational time and node count is
    inaccurate when multiple AlphaBetaAgents are playing in the same game as the values
    are shared across the 2 agents.

    Methods
    -------
    minimax()
        Calculates the best possible move from the current state of the game using minimax search.
    max_value()
        Calculates the max value from the next possible moves.
    min_value()
        Calculates the min value from the next possible moves.
    play()
        Places a move according to the minimax algorithm.
    """
    DEPTH_LIMIT = 4
    
    TIME_LIMIT = 3 # seconds
    TIME_LIMIT_ENFORCED = True # Toggle to turn on time limit
    
    time_limit_exceeded = False # Code value used to check if time limit was exceeded.
    
    # Class variable for easy syncing across recursion calls
    # Warning: Computational time and node count is inaccurate when playing multiple
    # AlphaBeta Agents simultaneously
    start_time = 0
    move_node_count = 0 # Node count per move
    total_node_count = 0 # Total node count across entire game

    def __init__(self, game: game.Game, mark):
        super().__init__(game, mark)
        # Value of the most recent move
        self.move_value = 0
        # Total computational time across the game
        self.total_comp_time = 0

        # Reset class variables
        AlphaBetaAgent.time_limit_exceeded = False
        AlphaBetaAgent.start_time = 0
        AlphaBetaAgent.move_node_count = 0
        AlphaBetaAgent.total_node_count = 0

    def minimax(self):
        """
        Calculates the best possible move from the current state of the game using minimax search.

        Returns
        -------
        int
            Row number of the best move to make.
        int 
            Column number of the best move to make.
        int
            Minimax value of the above move.
        """
        row = -1
        col = -1
        value = 0
        if self.mark == "X":
            row, col, value = self.max_value(self.game, -1000, +1000, 0)
        else:
            row, col, value = self.min_value(self.game, -1000, +1000, 0)

        return row, col, value
    
    def max_value(self, game, alpha, beta, depth):
        """
        Calculates the max value from the next possible moves.

        Returns
        -------
        int
            Row number of the best move to make.
        int 
            Column number of the best move to make.
        int
            Max value of the next moves.
        """
        # Checks if time limit is exceeded
        if (time.perf_counter() - AlphaBetaAgent.start_time >= AlphaBetaAgent.TIME_LIMIT and
            AlphaBetaAgent.TIME_LIMIT_ENFORCED):
            AlphaBetaAgent.time_limit_exceeded = True
            return -1, -1, 0

        # Checks if the game is at a terminal state or exceed depth limit
        if game.is_winning_move():
            # Value is +100 if X wins, -100 if O wins, adjusted for the number of moves to win
            AlphaBetaAgent.move_node_count += 1
            value = 100 - depth if game.curr_move["mark"] == "X" else -100 + depth
            return -1, -1, value
        elif game.is_over():
            # Value is 0 in case of draw
            AlphaBetaAgent.move_node_count += 1
            return -1, -1, 0
        elif depth >= AlphaBetaAgent.DEPTH_LIMIT:
            # Use evalutaion function to get value if depth limit exceeded
            AlphaBetaAgent.move_node_count += 1
            return -1, -1, game.get_state_val()
        
        value = -1000
        move_row = -1
        move_col = -1

        # Play through all empty cells
        for row, col in game.empty_cells:
            # Create a deep copy of the game and place the mark on the copy
            game_copy = copy.deepcopy(game)
            game_copy.place(row, col)

            next_row, next_col, next_value = self.min_value(game_copy, alpha, beta, depth+1)

            if next_value > value:
                value = next_value
                move_row, move_col = row, col
                alpha = max(alpha, value)
            if value >= beta:
                return move_row, move_col, value
        return move_row, move_col, value
    
    def min_value(self, game, alpha, beta, depth):
        """
        Calculates the min value from the next possible moves.

        Returns
        -------
        int
            Row number of the best move to make.
        int 
            Column number of the best move to make.
        int
            Min value of the next moves.
        """
        # Checks if time limit is exceeded
        if (time.perf_counter() - AlphaBetaAgent.start_time >= AlphaBetaAgent.TIME_LIMIT and
            AlphaBetaAgent.TIME_LIMIT_ENFORCED):
            AlphaBetaAgent.time_limit_exceeded = True
            return -1, -1, 0
        
        # Checks if the game is at a terminal state or exceed depth limit
        if game.is_winning_move():
            # Value is +100 if X wins, -100 if O wins, adjusted for the number of moves to win
            AlphaBetaAgent.move_node_count += 1
            value = 100 - depth if game.curr_move["mark"] == "X" else -100 + depth
            return -1, -1, value
        elif game.is_over():
            # Value is 0 in case of draw
            AlphaBetaAgent.move_node_count += 1
            return -1, -1, 0
        elif depth >= AlphaBetaAgent.DEPTH_LIMIT:
            # Use evalutaion function to get value if depth limit exceeded
            AlphaBetaAgent.move_node_count += 1
            return -1, -1, game.get_state_val()
        
        value = +1000
        move_row = -1
        move_col = -1

        # Play through all empty cells
        for row, col in game.empty_cells:
            # Create a deep copy of the game and place the mark on the copy
            game_copy = copy.deepcopy(game)
            game_copy.place(row, col)

            next_row, next_col, next_value = self.max_value(game_copy, alpha, beta, depth+1)

            if next_value < value:
                value = next_value
                move_row, move_col = row, col
                beta = min(beta, value)
            if value <= alpha:
                return move_row, move_col, value
        return move_row, move_col, value
    
    def play(self):
        """
        Places a move according to the minimax algorithm.
        
        Returns
        -------
        int
            Row number where the mark is successfully placed.
        int
            Column number where the mark is successfully placed.
        str
            The mark that is successfully placed.
        bool
            True if a random move was played due to the time limit.
        """
        print("AlphaBeta agent is thinking...")

        AlphaBetaAgent.time_limit_exceeded = False
        AlphaBetaAgent.move_node_count = 0
        AlphaBetaAgent.start_time = time.perf_counter()

        success = False
        while not success:
            row, col, self.move_value = self.minimax()
            # Chose random move if time limit exceeded
            if AlphaBetaAgent.time_limit_exceeded:
                row, col = random.choice(self.game.empty_cells)
            success = self.game.place(row, col, self.mark)

        end_time = time.perf_counter()
        comp_time = end_time-AlphaBetaAgent.start_time

        AlphaBetaAgent.total_node_count += AlphaBetaAgent.move_node_count
        self.total_comp_time += comp_time

        if AlphaBetaAgent.time_limit_exceeded:
            print(f"Time limit exceeded after exploring {AlphaBetaAgent.move_node_count} nodes!")
        else:
            print(f"AlphaBeta agent thought for {comp_time:.3f}s")
            print(f"AlphaBeta agent explored {AlphaBetaAgent.move_node_count} terminal nodes.")
            print("Move value:", self.move_value)

        print()
        print(f"Total computational time: {self.total_comp_time:.3f}s")
        print("Total nodes explored:", AlphaBetaAgent.total_node_count)
        return (row, col, self.mark, AlphaBetaAgent.time_limit_exceeded)
        

class RandomAgent(Agent):
    """
    A class representing a player that picks a random empty cell.

    Attributes
    ----------
    game : Game
        The game object containing the grid and the related methods.
    mark : str
        The mark the agent is playing as.

    Methods
    -------
    play()
        Places a random move from the remaining empty cells.
    """

    def __init__(self, game: game.Game, mark):
        super().__init__(game, mark)

    def play(self):
        """
        Places a random move from the remaining empty cells.
        
        Returns
        -------
        int
            Row number where the mark is successfully placed.
        int
            Column number where the mark is successfully placed.
        str
            The mark that is successfully placed.
        bool
            True (agent always plays random moves as intended).
        """
        success = False
        while not success:
            row, col = random.choice(self.game.empty_cells)
            success = self.game.place(row, col, self.mark)
        return (row, col, self.mark, True)
    
class NoisyHeuristicAgent(Agent):
    """
    A class representing a rule-based heuristic agent with a chance of random move.
    
    Attributes
    ----------
    game : Game
        The game object containing the grid and the related methods.
    mark : str
        The mark the agent is playing as.

    Methods
    -------
    play()
        Places a move according to the rule-based heuristic.
    getBestMove()
        Calculates the best move for the current game state using a rule-based heuristic.
    """
    NOISE_PERCENT = 20

    def __init__(self, game: game.Game, mark):
        super().__init__(game, mark)

    def getBestMove(self):
        """
        Calculates the best move for the current game state using a rule-based heuristic.

        Returns
        -------
        int
            Row number of the best move to make.
        int 
            Column number of the best move to make.
        bool
            True if a random move was played due to the noise.
        """
        # Plays a random move with chance NOISE_PERCENT
        value = random.randint(0,99)
        if value < NoisyHeuristicAgent.NOISE_PERCENT:
            return random.choice(self.game.empty_cells) + (True,) 

        # Moves that leads to a win
        winning_moves = []
        # Moves that lead to blocking opponent's win
        blocking_moves = []
        # Available moves from the middle ring cells 
        middle_ring_cells = [(row, col) for row in range(1, 4) for col in range(1, 4)]
        # Shuffle list for variety of moves
        random.shuffle(middle_ring_cells)

        # Explore all moves as X
        for row, col in self.game.empty_cells:
            # Create a deep copy of the game and place the mark on the copy
            game_copy = copy.deepcopy(self.game)
            game_copy.place(row, col, "X")

            # Check if placing X leads to self win or opponent win
            if game_copy.is_winning_move():
                if self.mark == "X":
                    # Self win
                    winning_moves.append((row, col))
                else:
                    # Opponnent win
                    blocking_moves.append((row, col))

        # Explore all moves as O
        for row, col in self.game.empty_cells:
            # Create a deep copy of the game and place the mark on the copy
            game_copy = copy.deepcopy(self.game)
            game_copy.place(row, col, "O")

            # Check if placing O leads to self win or opponent win
            if game_copy.is_winning_move():
                if self.mark == "O":
                    # Self win
                    winning_moves.append((row, col))
                else:
                    # Opponnent win
                    blocking_moves.append((row, col))
            
        # 1st priority: win
        if len(winning_moves) > 0:
            return winning_moves[0] + (False,) 
        
        # 2nd priority: block opponnent win
        if len(blocking_moves) > 0:
            return blocking_moves[0] + (False,)
        
        # 3rd priority: centre cells
        if (2, 2) in self.game.empty_cells:
            return (2, 2, False)
        else:
            for move in middle_ring_cells:
                if move in self.game.empty_cells:
                    return move + (False,)
        
        # Last priorty random move
        return random.choice(self.game.empty_cells) + (False,)

    def play(self):
        """
        Places a move according to the rule-based heuristic.
        
        Returns
        -------
        int
            Row number where the mark is successfully placed.
        int
            Column number where the mark is successfully placed.
        str
            The mark that is successfully placed.
        bool
            True if a random move was played due to the noise.
        """
        success = False
        while not success:
            row, col, played_random = self.getBestMove()
            success = self.game.place(row, col, self.mark)
        return (row, col, self.mark, played_random)


class HumanAgent(Agent):
    """
    A class representing a human agent that moves based on human input.

    Attributes
    ----------
    game : Game
        The game object containing the grid and the related methods.
    mark : str
        The mark the agent is playing as.

    Methods
    -------
    play()
        Places a move according to the input provided.
    """
    def __init__(self, game: game.Game, mark):
        super().__init__(game, mark)

    def play(self):
        """
        Places a move according to the input provided.
        
        Returns
        -------
        int
            Row number where the mark is successfully placed.
        int
            Column number where the mark is successfully placed.
        str
            The mark that is successfully placed.
        bool
            False (agent plays as intended).
        """
        success = False
        while not success:
            row, col = map(int, input(f"Input where to place {self.mark} in format row,col: ").split(","))
            success = self.game.place(row, col, self.mark)
        return (row, col, self.mark, False)

def main():
    """ Test code to play one game with 2 agents """
    game_obj = game.Game()

    playerX = AlphaBetaAgent(game_obj, "X")
    playerO = RandomAgent(game_obj, "O")

    game_over = False
    row = 0
    col = 0
    mark = 0
    print("Starting Game:")
    print("-"*75)
    while not game_over:
        if game_obj.turn_num % 2 == 0:
            row, col, mark, played_random = playerX.play()
        else:
            row, col, mark, played_random = playerO.play()

        print()
        game_obj.display_grid()
        if played_random:
            print("A random move was played!")
        print(f"Player {mark} placed {mark} in {row}, {col}")

        if game_obj.is_winning_move():
            print(f"Player {mark} has won the game.")
            game_over = True
        elif game_obj.is_over():
            print("The game ended in a draw!")
            game_over = True

        print("-"*75)

if __name__ == "__main__":
    main()