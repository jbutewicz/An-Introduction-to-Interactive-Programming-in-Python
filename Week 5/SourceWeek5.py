# implementation of card game - Memory
# @jbutewicz
import simplegui
import random

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 100
POSSIBLE_NUMBERS = range(8)
exposed = deck = [0]
first_card = second_card = [0, 0] #[value of card, index of card]
state = index = turn = 0

# helper function to initialize globals
def new_game():
    global deck, exposed, state, turn
    deck = POSSIBLE_NUMBERS * 2
    random.shuffle(deck)
    exposed = [False] * len(deck)
    state = 0
    turn = 0
    label.set_text("Turns = 0")

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, exposed, first_card, second_card, turn
    index = pos[0] // (CANVAS_WIDTH // len(deck))
    if exposed[index] == False:
        if state == 0:
            state = 1
            first_card = [deck[index], index]
        elif state == 1:
            state = 2
            second_card = [deck[index], index]
            turn += 1
            label.set_text("Turns = " + str(turn))
        else:
            state = 1
            if first_card[0] != second_card[0]:
                exposed[first_card[1]] = False
                exposed[second_card[1]] = False
            first_card[0] = deck[index]
            first_card[1] = index
    
    exposed[index] = True

# cards are logically 50x100 pixels in size
def draw(canvas):
    for i in range(len(deck)):
        if exposed[i] == False:
            canvas.draw_polygon([(i*CANVAS_WIDTH/len(deck), 0), (i*CANVAS_WIDTH/len(deck), CANVAS_HEIGHT), ((i + 1)*CANVAS_WIDTH/len(deck), CANVAS_HEIGHT), ((i + 1)*CANVAS_WIDTH/len(deck), 0), (i*CANVAS_WIDTH/len(deck), 0)], CANVAS_HEIGHT * 0.04, 'Black', 'Green')
        else:
            canvas.draw_text(str(deck[i]), (i*CANVAS_WIDTH/len(deck) + 5, CANVAS_HEIGHT * 0.7), CANVAS_HEIGHT * 0.6, 'Lime', 'monospace')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()