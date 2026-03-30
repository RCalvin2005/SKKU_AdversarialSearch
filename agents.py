import random
import copy
import time
import game

class AlphaBetaAgent():
    """
    A class representing an agent that plays based on minimax algorithm with alpha-beta pruning.
    """
    DEPTH_LIMIT = 4
    count = 0

    def __init__(self, game: game.Game, mark):
        self.game = game
        self.mark = mark

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
        # Checks if the game is at a terminal state or exceed depth limit
        if game.is_winning_move():
            # Value is +100 if X wins, -100 if O wins, adjusted for the number of moves to win
            AlphaBetaAgent.count += 1
            value = 100 - depth if game.curr_move["mark"] == "X" else -100 + depth
            return -1, -1, value
        elif game.is_over():
            # Value is 0 in case of draw
            AlphaBetaAgent.count += 1
            return -1, -1, 0
        elif depth >= AlphaBetaAgent.DEPTH_LIMIT:
            # Use evalutaion function to get value if depth limit exceeded
            AlphaBetaAgent.count += 1
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
        # Checks if the game is at a terminal state or exceed depth limit
        if game.is_winning_move():
            # Value is +100 if X wins, -100 if O wins, adjusted for the number of moves to win
            AlphaBetaAgent.count += 1
            value = 100 - depth if game.curr_move["mark"] == "X" else -100 + depth
            return -1, -1, value
        elif game.is_over():
            # Value is 0 in case of draw
            AlphaBetaAgent.count += 1
            return -1, -1, 0
        elif depth >= AlphaBetaAgent.DEPTH_LIMIT:
            # Use evalutaion function to get value if depth limit exceeded
            AlphaBetaAgent.count += 1
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
        """
        print("AlphaBeta agent is thinking...")
        AlphaBetaAgent.count = 0
        start_time = time.perf_counter()
        success = False
        while not success:
            row, col, value = self.minimax()
            success = self.game.place(row, col, self.mark)
        end_time = time.perf_counter()
        print(f"AlphaBeta agent thought for {end_time-start_time:.3f}s")
        print(f"AlphaBeta agent explored {AlphaBetaAgent.count} terminal nodes.")
        print("Move value:", value)
        return (row, col, self.mark)
        

class RandomAgent():
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
        self.game = game
        self.mark = mark

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
        """
        success = False
        while not success:
            row, col = random.choice(self.game.empty_cells)
            success = self.game.place(row, col, self.mark)
        return (row, col, self.mark)
    
class HumanAgent():
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
        self.game = game
        self.mark = mark

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
        """
        success = False
        while not success:
            row, col = map(int, input(f"Input where to place {self.mark} in format row,col: ").split(","))
            success = self.game.place(row, col, self.mark)
        return (row, col, self.mark)

def main():
    """ Test code to play one game with 2 agents """
    game_obj = game.Game()

    playerX = HumanAgent(game_obj, "X")
    playerO = AlphaBetaAgent(game_obj, "O")

    game_over = False
    row = 0
    col = 0
    mark = 0
    print("Starting Game:")
    print("-"*75)
    while not game_over:
        if game_obj.turn_num % 2 == 0:
            row, col, mark = playerX.play()
        else:
            row, col, mark = playerO.play()

        print()
        game_obj.display_cell_val()
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