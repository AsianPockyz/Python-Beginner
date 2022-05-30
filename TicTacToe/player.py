import math
import random

class Player:
    def __init__(self, letter):
        # letter is x or o
        self.letter=letter
    
    # we want all the players to get their next move
    def get_move(self, game):
        pass

class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
    
    def get_move(self,game):
        # Get a random open spot on the board
        square = random.choice(game.available_moves())
        return square

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self,game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move(0-8)')
            # we're going to then check that this is a correct value by trying to cast
            # it to an integer, and if it's not, then we print that it's invalid
            # if that spot is not available on the board, we also print invalid
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val

class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves()) # take a random move
        else:
            # get the square based off a minimax algo
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter # picking yourself
        other_player = 'O' if player == 'X' else 'X' # select the other player

        # first check if the last move was a winner
        # the base case
        if state.current_winner == other_player:
            # we should return position AND score because we need to keep track of the score
            # for minimax to work
            return {'position': None, 'score': 1 * (state.num_emptySquares() +1 ) if other_player == max_player else -1 * (state.num_emptySquares() +1)}
        elif not state.empty_squares(): # no empty squares
            return{'position': None, 'score': 0}

        if player == max_player:
            best = {'position':None, 'score': -math.inf} # each score should maximize i.e., needs to be better than the initial -infinite score
        else:
             best= {'position':None, 'score': math.inf} # else when not maxing for the player, want to minimize, so initialize at the highest posible value aka infinity
        for possible_move in state.available_moves():
            # step1: attempt a move
            state.make_move(possible_move, player)
            # step2: recurse using minimax to simulate a game after making that move
            sim_score = self.minimax(state, other_player) 
            # step3: undo the move, so that the next scenario can be attempted
            state.board[possible_move]=' '
            state.current_winner = None
            sim_score['position'] = possible_move # represents the current most optimal move
            # step4: update the dictionaries, if the current scenario is the most optimal yet replace the most optimal scenario with this one
            if player == max_player: # X is max player
                if sim_score['score'] > best['score']:
                    best = sim_score # replace with the optimal
            else:
                if sim_score['score'] < best['score']:
                        best = sim_score # replace with the optimal route
        return best
