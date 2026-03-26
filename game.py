class Game:
    """
    A class representing the Tic-Tac-Toe game.
    
    Class Constants
    ---------------
    GRID_SIZE : int
        The size of the board to be played on: GRID_SIZE x GRID_SIZE.

    Attributes
    ----------
    grid : list[list[str]]
        A 2D array to store which marks have been placed in which cells.
    
    Methods
    -------
    place(row, col, mark)
        Places the mark in the specified (row, col) grid cell after checking validaty.
    display_grid()
        Prints out the current state of the grid to terminal.
    """
    GRID_SIZE = 5

    def __init__(self):
        """
        Initialises the game with an empty grid.
        """
        # Note: [[" "] * Game.GRID_SIZE] * Game.GRID_SIZE creates a shallow copy
        self.grid = [[" "] * Game.GRID_SIZE for _ in range(Game.GRID_SIZE)]

    def place(self, row, col, mark):
        """
        Places the mark in the specified (row, col) grid cell after checking validaty.

        Parameters
        ----------
        row : int
            The row index of the target cell the mark is to be placed in.
        col : int
            The column index of the target cell the mark is to be placed in.
        mark : str
            The mark to be placed (X or O).

        Retruns
        -------
        bool
            True if successfully placed, False if (row, col) cell is not valid.
        """

        # Check if row & col is within bounds
        if row >= Game.GRID_SIZE or row < 0:
            return False
        if col >= Game.GRID_SIZE or col < 0:
            return False
        
        # Check if row, col cell is empty
        if self.grid[row][col] != " ":
            return False
        
        # Save mark in row, col cell
        self.grid[row][col] = mark
        return True
    
    def display_grid(self):
        """
        Prints out the current state of the grid to terminal.
        """
        print()
        print("+" + "---+"*Game.GRID_SIZE)
        for row in self.grid:
            print("| " + " | ".join(row) + " |")
            print("+" + "---+"*Game.GRID_SIZE)
        print()

def main():
    """
    Test code to place 10 marks on the grid
    """
    game = Game()
    
    game.place(2, 2, "X")
    game.display_grid()

    game.place(2, 2, "O")
    game.display_grid()

    game.place(2, 5, "O")
    game.display_grid()

    game.place(2, 1, "O")
    game.display_grid()

    game.place(1, 2, "X")
    game.display_grid()

    game.place(3, 2, "O")
    game.display_grid()

    game.place(1, 0, "X")
    game.display_grid()

    game.place(1, 1, "O")
    game.display_grid()

    game.place(3, 1, "X")
    game.display_grid()

    game.place(1, 3, "O")
    game.display_grid()    
    
    game.place(2, 3, "X")
    game.display_grid()

    game.place(4, 3, "O")
    game.display_grid()

    return

if __name__ == "__main__":
    main()
