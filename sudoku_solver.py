import copy
def is_valid_row(row):
    for i in range(1, 10):
        if row.count(i) > 1:
            return False
    return True

def is_valid_column(grid, column_index):
    column = [grid[row_index][column_index] for row_index in range(9)]
    return is_valid_row(column)

def is_valid_subgrid(grid, row_index, column_index):
    subgrid = [grid[i][j] for i in range(row_index, row_index+3) for j in range(column_index, column_index+3)]
    return is_valid_row(subgrid)

def is_valid(grid):
    # Check rows
    for row in grid:
        if not is_valid_row(row):
            return False

    # Check columns
    for column_index in range(9):
        if not is_valid_column(grid, column_index):
            return False

    # Check subgrids
    for row_index in range(0, 9, 3):
        for column_index in range(0, 9, 3):
            if not is_valid_subgrid(grid, row_index, column_index):
                return False

    return True

def possible(row,column,number,grid):
    # Check if the grid is valid
    if not is_valid(grid):
        return False

    # Check if the number appears in the row
    for i in range(0,9):
        if grid[row][i] == number:
            return False

    # Check if the number appears in the column
    for i in range(0,9):
        if grid[i][column] == number:
            return False

    # Check if the number appears in the square
    a = (row//3) * 3
    b = (column//3) * 3
    square = set()
    for i in range(0,3):
        for j in range(0,3):
            square.add(grid[a+j][b+i])

    if number in square:
        return False

    return True

def solve(grid):
    # Check if the grid is valid
    if not is_valid(grid):
        return None

    # Create a copy of the original grid to avoid modifying the input
    grid_copy = copy.deepcopy(grid)

    for row in range(0,9):
        for column in range(0,9):
            if grid_copy[row][column] == 0:
                for num in range(1,10):
                    if possible(row,column,num,grid_copy):
                        grid_copy[row][column] = num
                        result = solve(grid_copy)
                        if result is not None:
                            return result
                        grid_copy[row][column] = 0
                    
                return None
    return grid_copy

