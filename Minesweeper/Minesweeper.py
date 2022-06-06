import random
import re

# create a board object because Object oriented programming, to represent the minesweeper game
# this is so that we can just call "create a new obard object", or dig here to render this for this object
class Board:
    def __init__(self, dim_size, num_bombs):
        # keep track of these parameters
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # create the board
        # using a helper function
        self.board = self.make_new_board() # as well plant the bombs
        self.assign_values_to_board() 

        #initialize a set to keep track of which locations we've uncovered
        self.dug = set()
    
    def make_new_board(self):
        # construct new board based on the dim size and num bombs
        # should construct the list of lists here
        # 2D board so list of lists is most natural array

        # generate a new board
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        # this initializes a 2D array like:
        # [ None, None, ..., None],
        # [ None, None, ..., None],
        # [ None, None, ..., None]
        # which represents the board

        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2-1) # returns a random integer N such that a <= N <= b
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == '*':
                # this means we've already planted a bomb here, so we keep planting
                continue
            board [row][col] = '*' # plant a bomb at the position
            bombs_planted += 1
        return board

    def assign_values_to_board(self):
        # Now with bombs planted, assign a value from 1-8 for all empty spaces; which respresent
        # how many neighboring bombs there are. 
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # if this is already a bomb, don't calculate
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r,c)

    def get_num_neighboring_bombs(self, row, col):
        # to do this, iterate through each neighboring position and sum the number of bombs
        # top left would be like (row-1,col-1) etc.
        # while making sure not to go out of bounds
        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, (row+1)+1)):
            for c in range(max(0, col-1), min(self.dim_size-1, (col+1)+1)):
                if r == row and c == col:
                    # original location don't check this
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs +=1
        return num_neighboring_bombs

    def dig(self, row, col):
        # dig at the specified location
        # return true if successful dig, false if bomb hit
        # few scenarios:
        # hit a bomb -> game over
        # dig at a location with neighboring bombs -> finish the dig
        # dig at a location with no neighboring bombs -> recursively dig neighbors

        self.dug.add((row,col)) # keep track of the already dug places

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] >0:
            return True
        # self.board [row][col] == 0
        for r in range(max(0, row-1), min(self.dim_size-1, (row+1)+1)):
            for c in range(max(0, col-1), min(self.dim_size-1, (col+1)+1)):
                if (r,c) in self.dug:
                    continue # skip, because don't dig where you've already dug pointless 
                self.dig(r,c)
        # if the initial dig didn't hit a bomb, we shouldn't be hitting a bomb here
        return True

    def __str__(self):
        # kind of a cheat function where if you call print on this object
        # i'll print out what this function returns
        # so here use this to return a string that shows the board to the player

        #first create a new array that represents what the user would see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        
        # put this together in a string
        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep

# play the game
def play(dim_size=10, num_bombs=10):
    # step 1: create the board and plant the bombs
    board = Board (dim_size, num_bombs)
    # step 2: show the user the board and ask where they want to dig
    # step 3: if location is a bomb; game over, if location is not a bomb dig recursively until each square is at least next to a bomb
    # step 4: repeat steps 2 and 3 until there ar eno more places to dig == victory
    safe = True
    while len(board.dug) < board.dim_size **2 - num_bombs:
        print(board)
        # this allows us to handle 0,0 or 0, 0 etc. i.e, 0,     0
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row, col: ")) # '0, 3'
        row, col= int(user_input[0]), int(user_input[-1])
        if row < 0 or row>= board.dim_size or col <0 or col >= dim_size:
            print("invalid location. Try again")
            continue
        # if it's valid, we dig
        safe = board.dig(row, col)
        if not safe:
            # we hit a bomb
            break # game over breka the loop
    # 2 ways out of the loop
    if safe:
        print("Congrats, all bombs found")
    else:
        print("BOOM! Game over")
        # and reveal the whole board
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == '__main__': # this is good practice if you have a large project and only want to run the one file.
    play()
     


