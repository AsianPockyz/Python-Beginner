# Number guessing game

import random

# Generate a random number so that the user can guess
def guess(x):
    random_number = random.randint(1,x)
    guess = 0
    while guess != random_number:
        guess = int(input(f"Guess a number between 1 and {x}: "))
        if guess < random_number:
            print('Too low')
        elif guess > random_number:
            print('Too high')
    print(f'Correct number: {random_number}')    

# computer will randomly generate a number and user will have to provide feedback is it too high or too low
def computer_guess(x):
    low = 1
    high = x
    feedback = ''
    while feedback != 'c':
        if low != high:
            guess = random.randint(low,high)
        else:
            guess = low
        feedback = input(f'Is {guess} too high (H), too low (L), or correct (C): ').lower()
        if feedback == 'h':
            high = guess-1
        if feedback == 'l':
            low = guess+1
    print(f'I guessed your numeber, it is {guess}!')

# call the function that I want to try
computer_guess(10)

