import random
from Words import words
import string

def get_valid_word(words):
    word = random.choice(words) #randomly choose something from list "words"
    while '-' in words or ' ' in words:
        word = random.choice(words)
    return word.upper() 

def hangman():
    word = get_valid_word(words)
    word_letters=set(word) # Save all the letters in the word as a set
    alphabet = set(string.ascii_uppercase)
    used_letters = set() # Already guessed letters

    lives = 6 # introduce lives into the game, consequence

    # get user input
    while len(word_letters) > 0 and lives > 0:
        # Print used letters
        # ' '.join(['a','b','c']) = 'a b c' appends each iteration of the set to the string in this case appends each index to the space, therefore each index separated by space
        print('You have: ',lives,' lives left. You have already guessed letters: ',' '.join(used_letters))

        # Show the current status of the solution ie G - - E S S
        word_list = [letter if letter in used_letters else '-' for letter in word]
        print('Current word: ',' '.join(word_list))

        user_letter = input('Guess a letter: ' ).upper()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
            else:
                lives = lives - 1 # lose a life
                print('That letter is not in the word.')
        elif user_letter in used_letters:
            print('Character has already been guessed. Please guess again.')
        else:
            print('Invalid character. Please try a letter from A-Z.')
    # Exits when length of word_letters == 0 or when Lives == 0 died
    if lives == 0:
        print('You have been hung. The word was: ',word)
    else:
        print('You guessed the word correctly, it was: ', word)

hangman()