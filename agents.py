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

    def minimax(self, game: game.Game, depth, isMax):
        """
        Calculates the minimax value (best achievable utility) for the node.

        Returns
        -------
        int
            Value of the game given a particular move.
        """
        # Checks if the game is at a terminal state or exceed depth limit
        if game.is_winning_move():
            # Value is +100 if X wins, -100 if O wins
            AlphaBetaAgent.count += 1
            #game.display_grid()
            return 100 - depth if game.curr_move["mark"] == "X" else -100 + depth
        elif game.is_over():
            # Value is 0 in case of draw
            AlphaBetaAgent.count += 1
            return 0
        elif depth >= AlphaBetaAgent.DEPTH_LIMIT:
            # Use evalutaion function to get value if depth limit exceeded
            AlphaBetaAgent.count += 1
            return game.get_state_val()
        
        if isMax:
            # Initialise value to large negative number
            value = -1000
            
            # Play through all empty cells
            for row, col in game.empty_cells:
                # Create a deep copy of the game and place the mark on the copy
                game_copy = copy.deepcopy(game)
                game_copy.place(row, col)

                value = max(value, self.minimax(game_copy, depth+1, not isMax))
            
            # Return the max value
            return value
        
        else:
            # Initialise value to large positive number
            value = 1000
            
            # Play through all empty cells
            for row, col in game.empty_cells:
                # Create a deep copy of the game and place the mark on the copy
                game_copy = copy.deepcopy(game)
                game_copy.place(row, col)

                value = min(value, self.minimax(game_copy, depth+1, not isMax))
            
            # Return the min value
            return value

    def getBestMove(self):
        """
        Calculates the best possible move from the current state of the game.

        Returns
        -------
        int
            Row number of the best move to make.
        int 
            Column number of the best move to make.
        int
            Minimax value of the above move.
        """
        bestMoveRow = -1
        bestMoveCol = -1
        bestValue = -1000 if self.mark == "X" else 1000

        # Traverse all possible moves and evaluate it using minimax
        for row, col in self.game.empty_cells:
            # Create a deep copy of the game and place the mark on the copy
            game_copy = copy.deepcopy(self.game)
            game_copy.place(row, col)

            if self.mark == "X":
                # Play as max if agent is playing X
                moveValue = self.minimax(game_copy, 1, False)

                # Update best move if current move has higher value than the best one
                if moveValue > bestValue:
                    bestMoveRow = row
                    bestMoveCol = col
                    bestValue = moveValue

            else:
                # Play as min if agent is playing O
                moveValue = self.minimax(game_copy, 1, True)

                # Update best move if current move has lower value than the best one
                if moveValue < bestValue:
                    bestMoveRow = row
                    bestMoveCol = col
                    bestValue = moveValue
            print(moveValue)

        return bestMoveRow, bestMoveCol, bestValue
    
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
            row, col, value = self.getBestMove()
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

    playerX = AlphaBetaAgent(game_obj, "X")
    playerO = HumanAgent(game_obj, "O")

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