class Game:
    """
    A class representing the Tic-Tac-Toe game.
    
    Attributes
    ----------
    GRID_SIZE : int
        The size of the board to be played on: GRID_SIZE x GRID_SIZE.
    WIN_N_IN_LINE : int
        The required number of n-in-a-line marks to win the game. 
    CENTRE_PROX_VALS : list[list[int]]
        An 2D array with the centre proximity values for each cell in the grid.
    grid : list[list[str]]
        A 2D array to store which marks have been placed in which cells.
    curr_move : dict[int, int, str]
        A dictionary containing information of the current move: row, col, and mark.
    empty_cell : list[tuple[int, int]]
        An array containing the remaining empty (row, col) cells.
    turn_num : int
        The current turn number of the game.
    
    Methods
    -------
    place(row, col, mark)
        Places the mark in the specified (row, col) grid cell after checking validaty.
    update_cell_vals()
        Updates the n-in-line cell values of the current placed cell and adjacent cells.
    is_winning_move()
        Checks if the current move was a winning move.
    get_state_val()
        Calculates the game state value from the evaulutaion function.
    display_grid()
        Prints out the current state of the grid to terminal.
    display_cell_val()
        Prints out the current grid with all the cell values.
    """
    GRID_SIZE = 5
    WIN_N_IN_LINE = 4
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
        
        self.curr_move = {"row": 0, "col": 0, "mark": " "}

        # Empty cells not ordered
        # self.empty_cells = [(row, col)
        #                     for row in range(Game.GRID_SIZE) for col in range(Game.GRID_SIZE)]
        
        # Empty cells ordered from centre outwards for move ordering to reduce time for minimax
        self.empty_cells = [
            (2, 2), (1, 1), (1, 2), (1, 3), (2, 1),
            (2, 3), (3, 1), (3, 2), (3, 3), (0, 0),
            (0, 1), (0, 2), (0, 3), (0, 4), (1, 0),
            (1, 4), (2, 0), (2, 4), (3, 0), (3, 4),
            (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)
        ]
        
        self.turn_num = 0
        
    def place(self, row, col, mark=None):
        """
        Places the mark in the specified (row, col) grid cell after checking validaty.

        Parameters
        ----------
        row : int
            The row index of the target cell the mark is to be placed in.
        col : int
            The column index of the target cell the mark is to be placed in.
        mark : str, optional
            The mark to be placed (X or O). Selects mark based on turn number if not provided.

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
        
        # Get mark based on turn number if not provided
        if (mark == None):
            mark = "X" if self.turn_num % 2 == 0 else "O"

        # Save mark in row, col cell
        self.grid[row][col].mark = mark
        self.curr_move = {"row": row, "col": col, "mark": mark}

        # Update game status
        self.empty_cells.remove((row, col))
        self.turn_num += 1

        # Updates the cell values
        self.update_cell_vals()

        return True
    
    def update_cell_vals(self):
        """
        Updates the n-in-line cell values of last placed cell and adjacent cells.
        """
        row = self.curr_move["row"]
        col = self.curr_move["col"]
        mark = self.curr_move["mark"]

        # Update n-in-row values for left and right neighbours
        left_horz_val = 0
        if col - 1 >= 0:
            left_cell = self.grid[row][col-1]
            if left_cell.mark == mark:
                left_horz_val = left_cell.horz_val

        right_horz_val = 0
        if col + 1 < Game.GRID_SIZE: 
            right_cell = self.grid[row][col+1]
            if right_cell.mark == mark:
                right_horz_val = right_cell.horz_val

        n_in_row = left_horz_val + 1 + right_horz_val
        for i in range(-left_horz_val, right_horz_val + 1):
            self.grid[row][col+i].horz_val = n_in_row

        # Update n-in-column values for top and bottom neighbours
        top_vert_val = 0
        if row - 1 >= 0:
            top_cell = self.grid[row-1][col]
            if top_cell.mark == mark:
                top_vert_val = top_cell.vert_val

        bottom_vert_val = 0
        if row + 1 < Game.GRID_SIZE: 
            bottom_cell = self.grid[row+1][col]
            if bottom_cell.mark == mark:
                bottom_vert_val = bottom_cell.vert_val

        n_in_col = top_vert_val + 1 + bottom_vert_val
        for i in range(-top_vert_val, bottom_vert_val + 1):
            self.grid[row+i][col].vert_val = n_in_col

        # Update n-in-downward-diagonal values for top-left and bottom-right neighbour
        top_left_diag_val = 0
        if row - 1 >= 0 and col - 1 >= 0:
            top_left_cell = self.grid[row-1][col-1]
            if top_left_cell.mark == mark:
                top_left_diag_val = top_left_cell.down_diag_val

        bottom_right_diag_val = 0
        if row + 1 < Game.GRID_SIZE and col + 1 < Game.GRID_SIZE: 
            bottom_right = self.grid[row+1][col+1]
            if bottom_right.mark == mark:
                bottom_right_diag_val = bottom_right.down_diag_val

        n_in_down_diag = top_left_diag_val + 1 + bottom_right_diag_val
        for i in range(-top_left_diag_val, bottom_right_diag_val + 1):
            self.grid[row+i][col+i].down_diag_val = n_in_down_diag

        # Update n-in-upward-diagonal values for bottom-left and top-right neighbour
        bottom_left_diag_val = 0
        if row + 1 < Game.GRID_SIZE and col - 1 >= 0:
            bottom_left_cell = self.grid[row+1][col-1]
            if bottom_left_cell.mark == mark:
                bottom_left_diag_val = bottom_left_cell.up_diag_val

        top_right_diag_val = 0
        if row - 1 >= 0 and col + 1 < Game.GRID_SIZE: 
            top_right = self.grid[row-1][col+1]
            if top_right.mark == mark:
                top_right_diag_val = top_right.up_diag_val

        n_in_up_diag = bottom_left_diag_val + 1 + top_right_diag_val
        for i in range(-bottom_left_diag_val, top_right_diag_val + 1):
            self.grid[row-i][col+i].up_diag_val = n_in_up_diag

    def is_winning_move(self):
        """
        Checks if the current move was a winning move.

        Returns
        -------
        bool
            True if the last current was a winning move, False otherwise.
        """
        # Check if there is at least 4 in a row in any of the directions
        curr_cell = self.grid[self.curr_move["row"]][self.curr_move["col"]]
        if curr_cell.horz_val >= Game.WIN_N_IN_LINE:
            return True
        if curr_cell.vert_val >= Game.WIN_N_IN_LINE:
            return True
        if curr_cell.down_diag_val >= Game.WIN_N_IN_LINE:
            return True
        if curr_cell.up_diag_val >= Game.WIN_N_IN_LINE:
            return True
        return False
    
    def is_over(self):
        """
        Checks if the game is over (no remaining empty cells).

        Returns
        -------
        bool
            Returns true is the game is over (no remaining empty cells).
        """
        return len(self.empty_cells) == 0
    
    def get_state_val(self):
        """
        Calculates the game state value from the evaulutaion function.
        Evalutaion function: Centre proximity + all n-in-line values.

        Returns
        -------
        int
            Sum of all the grid cell values.
        """
        game_val = 0
        for row in range(Game.GRID_SIZE):
            for col in range(Game.GRID_SIZE):
                game_val += self.grid[row][col].get_value()
        return game_val

    def display_grid(self):
        """
        Prints out the current state of the grid to terminal.
        """
        print("+" + "---+"*Game.GRID_SIZE)
        for row_num in range(len(self.grid)):
            line = "|"
            for col_num in range(len(self.grid[row_num])):
                mark = self.grid[row_num][col_num].mark
                if row_num == self.curr_move["row"] and col_num == self.curr_move["col"]:
                    line += f" \033[93m{mark}\033[0m |"
                elif mark == "X":
                    line += f" \033[92m{mark}\033[0m |"
                elif mark == "O":
                    line += f" \033[91m{mark}\033[0m |"
                else:
                    line += f" {mark} |"
            print(line)
            print("+" + "---+"*Game.GRID_SIZE)

    def display_cell_val(self):
        """
        Prints out the current grid with all the cell values.
        Top left:       n-in-a-row
        Top centre:     centre proximity
        Top right:      n-in-a-column
        Bottom left:    n-in-downward-diagonal
        Bottom centre:  total value
        Bottom right:   n-in-upward-diagonal     
        Example:    
        +---------+
        |1   1   1|
        |    X    |
        |1  +11  1|
        +---------+
        """
        print("+" + "---------+"*Game.GRID_SIZE)
        for row in self.grid:
            line1 = "|"
            line2 = "|"
            line3 = "|"
            for cell in row:
                line1 += f"{cell.horz_val}   {cell.centre_prox}   {cell.vert_val}|"
                line2 += f"    {cell.mark}    |"
                line3 += f"{cell.down_diag_val} "
                # Print formatting and colours reference:
                # https://www.w3schools.com/python/python_string_formatting.asp
                # https://www.geeksforgeeks.org/python/print-colors-python-terminal/
                val = cell.get_value()
                if val > 0:
                    line3 += f"\033[92m{val:+3}\033[0m"
                elif val < 0:
                    line3 += f"\033[91m{val:+3}\033[0m"
                else:
                    line3 += f"{val:+3}"
                line3 += f"   {cell.up_diag_val}|"
            print(line1, line2, line3, sep="\n")
            print("+" + "---------+"*Game.GRID_SIZE)

        return
    
    def format_grid_str(self):
        """
        Formats current state of the grid to a single str for logging.

        Returns
        -------
        str
            The full grid in a single str.
        """
        grid_str = ("+" + "---+"*Game.GRID_SIZE + "\n")
        for row in self.grid:
            grid_str += ("| " + " | ".join(cell.mark for cell in row) + " |\n")
            grid_str += ("+" + "---+"*Game.GRID_SIZE + "\n")
        return grid_str
    
    def format_cell_val_str(self):
        """
        Formats the current grid with all the cell values into a single str
        Top left:       n-in-a-row
        Top centre:     centre proximity
        Top right:      n-in-a-column
        Bottom left:    n-in-downward-diagonal
        Bottom centre:  total value
        Bottom right:   n-in-upward-diagonal     
        Example:    
        +---------+
        |1   1   1|
        |    X    |
        |1  +11  1|
        +---------+

        Returns
        -------
        str
            The full grid with cell values in a single str.
        """
        grid_str = ("+" + "---------+"*Game.GRID_SIZE + "\n")
        for row in self.grid:
            line1 = "|"
            line2 = "|"
            line3 = "|"
            for cell in row:
                line1 += f"{cell.horz_val}   {cell.centre_prox}   {cell.vert_val}|"
                line2 += f"    {cell.mark}    |"
                line3 += f"{cell.down_diag_val} {cell.get_value():+3}   {cell.up_diag_val}|"
            grid_str += (line1 + "\n" + line2 + "\n" + line3 + "\n")
            grid_str += ("+" + "---------+"*Game.GRID_SIZE + "\n")
        return grid_str

class Cell:
    """
    A class representing a single cell and its value in the Tic-Tac-Toe grid.

    Attributes
    ----------
    mark : str
        The mark placed in the cell (X, O or " ").
    centre_prox: 
        Value of the cell from its proximity to the centre.
    horz_val : int
        The value of the cell from n-in-a-row marks (-- direction).
    vert_val : int
        The value of the cell from n-in-a-column marks ( | direction).
    down_diag_val : int
        The value of the cell from n-in-downward-diagonal-line marks (\\ direction).
    up_diag_val : int
        The value of the cell from n-in-upward-diagonal-line marks (/ direction).

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
        self.horz_val = 0
        self.vert_val = 0
        self.down_diag_val = 0
        self.up_diag_val = 0

    def get_value(self):
        """
        Calculates the total value of the cell accounting for centre proximity and
        n-in-a-line marks in horizontal, vertical, and diagonal directions.

        Retruns
        -------
        int
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
    Test code to place 14 marks on the grid with the 12th move the winning move.
    """
    game = Game()
    
    sequence = [
        [2, 2, "X"],
        [2, 2, "O"],
        [2, 5, "O"],
        [2, 3, "O"],
        [1, 2, "X"],
        [3, 2, "O"],
        [1, 3, "X"],
        [1, 4, "O"],
        [4, 1, "X"],
        [3, 1, "O"],
        [1, 1, "X"],
        [3, 3, "O"],
        [3, 4, "X"],
        [3, 0, "O"],
        [1, 0, "X"],
        [2, 1, "O"],
    ]
    
    for move in sequence:
        print(f"Placing {move[2]} in row {move[0]}, col {move[1]}.")
        success = game.place(move[0], move[1], move[2])
        print()
        print(game.format_cell_val_str())
        #game.display_cell_val()
        print()
        
        if success:
            print(f"Sucessfully placed {move[2]} in row {move[0]}, col {move[1]}.")
        else: 
            print(f"Failed to place {move[2]} in row {move[0]}, col {move[1]}.")

        print("Game state value:", game.get_state_val())

        if game.is_winning_move():
            print(f"Player {game.curr_move["mark"]} has won the game!")
            return
        elif game.is_over():
            print("Game ended in a draw!")

        print("-"*75)

    return

if __name__ == "__main__":
    main()
