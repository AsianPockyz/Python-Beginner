import player
import time

class TicTacToe:
    def __init__(self):
        self.board = [' 'for _ in range(9)] # we will use a single list to represent 3x3 board
        self.current_winner = None # keep track of if there is a winner or not

    def print_board(self):
        # define the rows of the 3x3 tic tac toe board
        for row in [self.board[i*3:(i+1)*3]for i in range(3)]:
            print('| '+' | '.join(row)+' |')

    @staticmethod
    def print_boardNums():
        # number the board into index 0 | 1 | 2 etc. for the 3x3
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range (3)]
        for row in number_board:
            print('| '+' | '.join(row)+' |')

    def available_moves(self):
        # moves=[]
        # for (i, spot) in enumerate(self.board):
        #     # the board: ['x', 'x' , 'o'] becomes indexed --> [(0,x), (1,x), (2,o)]
        #     if spot == ' ':
        #         move.append(i)
        # return moves 
        # Another way of doing this is with list comprehension
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    
    def empty_squares(self):
        return ' ' in self.board

    def num_emptySquares(self):
       # return len(self.available_moves()) 
        return self.board.count(' ') # same thing  

    def make_move(self, square, letter):
        # if valid move, then make the move (aka assign the square to a letter)
        # then return true, if invalid move return false
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False
    
    def winner(self, square, letter):
        # winner logic is that there is a 3 in a row anywhere, in the row column or diagonal
        # first check row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3] 
        if all([spot == letter for spot in row]):
            return True
        # check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3]for i in range(3)]
        if all(spot == letter for spot in column):
            return True
        # check diagonal
        # however since only diagonal possibilities are on even numbers (0, 2, 4, 6, 8)
        # these are the only moves possible to win diagonally
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0,4,8]] #left to right diagonal
            if all(spot == letter for spot in diagonal1):
                return True
            diagonal2 = [self.board[i] for i in [2,4,6]] # right to left diagonal 
            if all(spot == letter for spot in diagonal2):
                return True

        # if all these logic checks fail then there is no winner
        return False

def play(game, x_player, o_player, print_game=True):
    # reutnr the winner of the game and their letter, or return none if it's a tie 
    if print_game:
        game.print_boardNums()
    letter = 'X' # the player that starts
    # iterate while the game still has open spaces
    # we don't have to worry about when a winner happens because return will break the loop
    while game.empty_squares():
        # get a move from the appropriate player
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
        
        # define a function to get a move
        if game.make_move(square, letter):
            if print_game:
                print(letter + f' make a move to square {square}')
                game.print_board()
                print('') # empty line

            if game.current_winner:
                if print_game:
                    print(letter+' wins!')
                return letter

            # after a move has been made we need to alternate the players
            letter = 'O' if letter == 'X' else 'X'
        
        # add a time delay to make the gameplay feel smoother
        if print_game:
            time.sleep(0.8)
        
    if print_game:
        print('It\'s a tie!')

if __name__ == '__main__':
    x_wins = 0
    o_wins = 0 
    ties = 0
    for _ in range(100):
        x_player =  player.RandomComputerPlayer('X')
        o_player = player.GeniusComputerPlayer('O')
        t = TicTacToe()
        result = play(t, x_player, o_player, print_game=False)
        if result == 'X':
            x_wins+=1
        elif result =='O':
            o_wins+=1
        else:
            ties+=1

    print(f'After 100 games, we see {x_wins} X Wins, {o_wins} O wins, and {ties} Ties')
