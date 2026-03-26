class Game:
    """
    A class representing the Tic-Tac-Toe game.
    
    Attributes
    ----------
    GRID_SIZE : int
        The size of the board to be played on: GRID_SIZE x GRID_SIZE.
    CENTRE_PROX_VALS : list[list[float]]
        An 2D array with the centre proximity values for each cell in the grid.
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
    CENTRE_PROX_VALS = [
        [1, 1, 1, 1, 1],
        [1, 2, 2, 2, 1],
        [1, 2, 3, 2, 1],
        [1, 2, 2, 2, 1],
        [1, 1, 1, 1, 1],
    ]

    def __init__(self):
        """
        Initialises the game with an empty grid with centre proximity values applied.
        """
        # Note: [[" "] * Game.GRID_SIZE] * Game.GRID_SIZE creates a shallow copy
        # 2D List Comprehension reference:
        # https://www.upgrad.com/tutorials/software-engineering/python-tutorial/2d-array-in-python/
        self.grid = [[Cell(Game.CENTRE_PROX_VALS[row][col]) for col in range(Game.GRID_SIZE)]
                     for row in range(Game.GRID_SIZE)]
        
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
        if self.grid[row][col].mark != " ":
            return False
        
        # Save mark in row, col cell
        self.grid[row][col].mark = mark
        return True
    
    def display_grid(self):
        """
        Prints out the current state of the grid to terminal.
        """
        print("+" + "---+"*Game.GRID_SIZE)
        for row in self.grid:
            print("| " + " | ".join(cell.mark for cell in row) + " |")
            print("+" + "---+"*Game.GRID_SIZE)

class Cell:
    """
    A class representing a single cell and its value in the Tic-Tac-Toe grid.

    Attributes
    ----------
    mark : str
        The mark placed in the cell (X, O or " ").
    centre_prox: 
        Value of the cell from its proximity to the centre.
    horz_ptr : list[float]
        An array containing the value of the cell from n-in-a-row marks (-- direction).
    vert_ptr : list[float]
        An array containing the value of the cell from n-in-a-column marks ( | direction).
    down_diag_ptr : list[float]
        An array containing the value of the cell from n-in-downward-diagonal-line marks (\\ direction).
    up_diag_ptr : list[float]
        An array containing the value of the cell from n-in-upward-diagonal-line marks (/ direction).
    
    Notes
    -----
    Use of list[float] allows for shallow copy for easy sync with adjacent cells
    (removing the need to implement a linked list or similar by passing the list by reference,
    basically simulating pointer behaviour in C/C++).

    Methods
    -------
    get_value()
        Returns the total value of the cell accounting for centre proximity and
        n-in-a-line marks in horizontal, vertical, and diagonal directions.
    """

    def __init__(self, centre_prox):
        """
        Initialises the cell with given centre proximity value, empty mark, and 0 n-in-line values.
        """
        self.mark = " "
        self.centre_prox = centre_prox
        self.horz_ptr = [0]
        self.vert_ptr = [0]
        self.down_diag_ptr = [0]
        self.up_diag_ptr = [0]

    def get_value(self):
        """
        Calculates the total value of the cell accounting for centre proximity and
        n-in-a-line marks in horizontal, vertical, and diagonal directions.

        Retruns
        -------
        float
            Returns positive value for X, negative value for O and 0 for no mark or otherwise.
        """
        if self.mark == "X":
            return (self.horz_val + self.vert_val + self.down_diag_val + self.up_diag_val
                    + self.centre_prox)
        elif self.mark == "O":
            return (self.horz_val + self.vert_val + self.down_diag_val + self.up_diag_val
                    + self.centre_prox) * -1
        else:
            return 0


def main():
    """
    Test code to place 10 marks on the grid
    """
    game = Game()
    
    sequence = [
        [2, 2, "X"],
        [2, 2, "O"],
        [2, 5, "O"],
        [2, 1, "O"],
        [1, 2, "X"],
        [3, 2, "O"],
        [1, 0, "X"],
        [1, 1, "O"],
        [3, 1, "X"],
        [1, 3, "O"],
        [2, 3, "X"],
        [4, 3, "O"]
    ]
    
    for move in sequence:
        print(f"Placing {move[2]} in row {move[0]}, col {move[1]}.")
        success = game.place(move[0], move[1], move[2])
        print()
        game.display_grid()
        print()
        if success:
            print(f"Sucessfully placed {move[2]} in row {move[0]}, col {move[1]}.")
        else: 
            print(f"Failed to place {move[2]} in row {move[0]}, col {move[1]}.")
        print("-"*75)

    return

if __name__ == "__main__":
    main()
