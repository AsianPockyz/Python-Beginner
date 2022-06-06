def find_next_empty(puzzle):
    # finds the next row, col that is not yet filled, represented by -1
    # return row, col tuple (or (None, None) if there is none)

    # keep in mind that this is a 0 index 0-8 
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == -1:
                return r,c
    return None, None # if no spaces in the puzzle are empty (==-1)

def is_valid(puzzle, guess, row, col):
    # figures out whether the guess at the row, col of the puzzle is valid
    # return true if valid, false otherwise

    # start with row
    row_vals = puzzle [row]
    if guess in row_vals:
        return False
    # now column
    col_vals = []
    # for i in range(9):
    #     col_vals.append(puzzle[i][col])
    # same function as above using list comprehension
    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False
    
    # and then the last 3x3 square
    # find the starting row index of the 3x3 and then find the starting col index of the 3x3
    # and then iterate over the 3 values in the square
    row_start = (row // 3) * 3 # divide by 3 throw away the remainder
    col_start = (col // 3) * 3

    for r in range(row_start, row_start +3):
        for c in range(col_start, col_start +3):
            if puzzle[r][c] == guess:
                return False
    
    # if we get here, passing all the checks
    return True

def solve_sudoku(puzzle):
    # solve sudoku using a backtracking technique 
    # out puzzle is a list of lists, where each inner list is a row in our sudoku puzzle
    # return whether a solution exists
    # mutates puzzle to be the solution (if the solution exists)
    
    # setp 1: choose somehwere on the puzzle to make a guess
    row, col = find_next_empty(puzzle)
    # if there i s nowhere left then we're done because we are only allowed valid inputs
    if row is None:
        return True
    
    # stepp 2: if there is a place to put a number, then make a guess between 1 and 9
    for guess in range(1,10): 
        # step 3: check if this is a valid guess
        if is_valid(puzzle, guess, row, col):
            # if valid then place the guess on the puzzle
            puzzle[row][col] = guess
            # now recurse using this mutated puzzle
            if solve_sudoku(puzzle):
                return True
        # step 5: if not valid or if the guess does not solve the puzzle
        # then we need to backtrack and try a new number
        puzzle[row][col] = -1
    
    # step 6: if none of the numbers that we try work, then the puzzle is unsolvable
    return False

if __name__ == '__main__':
    example_board = [
        [3, 9, -1,   -1, 5, -1,   -1, -1, -1],
        [-1, -1, -1,   2, -1, -1,   -1, -1, 5],
        [-1, -1, -1,   7, 1, 9,   -1, 8, -1],

        [-1, 5, -1,   -1, 6, 8,   -1, -1, -1],
        [2, -1, 6,   -1, -1, 3,   -1, -1, -1],
        [-1, -1, -1,   -1, -1, -1,   -1, -1, 4],

        [5, -1, -1,   -1, -1, -1,   -1, -1, -1],
        [6, 7, -1,   1, -1, 5,   -1, 4, -1],
        [1, -1, 9,   -1, -1, -1,   2, -1, -1]
    ]
    print(solve_sudoku(example_board)) # solvable or not, false is not solvable
    print(example_board) # print the mutated board that is the solution
