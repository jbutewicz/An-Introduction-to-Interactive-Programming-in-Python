# "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import math
import random
import simplegui

# initialize global variables used in your code
secret_number = 0
low = 0
high = 0
n = 0

# helper function to start and restart the game
def new_game():
    global secret_number, n
    secret_number = random.randrange(low, high)
    n = int(math.ceil(math.log((high - low + 1), 2)))
    print "New game. Range is from " + str(low) + " to " + str(high)
    print "Number of remaining guesses is " + str(n)
    print

# define event handlers for control panel
def range100():
    global high, n
    high = 100
    new_game()
    
def range1000():
    global high, n 
    high = 1000
    new_game()
    
def input_guess(guess):
    global n

    n -= 1
    print "Guess was " + guess
    print "Number of remaining guesses is " + str(n)
    
    guess_int = int(guess)
    
    if n == 0 and guess_int != secret_number:
        print "You ran out of guesses. The number was " + str(secret_number)
        print
        new_game()
    elif guess_int == secret_number:
        print "Correct!"
        print
        new_game()
    elif guess_int <= secret_number:
        print "Higher"
        print
    elif guess_int >= secret_number:
        print "Lower"
        print

# create frame
number_game_frame = simplegui.create_frame('Guess the Number', 100, 150)

# register event handlers for control elements
number_text_box_input = number_game_frame.add_input('Type number and press Enter', input_guess, 50)
button100 = number_game_frame.add_button('Range: 0 - 100', range100, 150)
button1000 = number_game_frame.add_button('Range: 0 - 1000', range1000, 150)

# call new_game and start frame
range100()
number_game_frame.start()