import random
from game import Game

class RandomAgent():
    """
    A class representing a player that picks a random empty cell.
    """

    def __init__(self, game, mark):
        self.game = game
        self.mark = mark

    def play(self):
        """
        Places a random move from the remaining empty cells
        
        Returns
        -------
        int
            Row number where the mark is successfully placed.
        int
            Column number where the mark is successfully placed.
        str
            The mark that is successfully placed.
        """
        row, col = random.choice(self.game.empty_cells)
        success = False
        while not success:
            success = self.game.place(row, col, self.mark)
        return (row, col, self.mark)

def main():
    """ Test code to play the Random Agent """
    game = Game()

    playerX = RandomAgent(game, "X")
    playerO = RandomAgent(game, "O")

    game_over = False
    row = 0
    col = 0
    mark = 0
    print("Starting Game:")
    print("-"*75)
    while not game_over:
        if game.turn_num % 2 == 0:
            row, col, mark = playerX.play()
        else:
            row, col, mark = playerO.play()

        print()
        game.display_grid()
        print(f"Player {mark} placed {mark} in {row}, {col}")

        if game.is_winning_move():
            print(f"Player {mark} has won the game.")
            game_over = True
        elif game.is_over():
            print("The game ended in a draw!")
            game_over = True

        print("-"*75)

if __name__ == "__main__":
    main()