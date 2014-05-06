# Mini-project #6 - Blackjack
# @jbutewicz
import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")

# initialize some useful global variables
in_play = False
scored = False
outcome = ""
score = 0
BET_AMOUNT = 1
deck = []
player_hand = []
dealer_hand = []
outcome = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank
    
    def __str__(self):
        return self.suit + self.rank
    
    def get_suit(self):
        return self.suit
    
    def get_rank(self):
        return self.rank
    
    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cards = []
    
    def __str__(self):
        # return a string representation of a hand
        return "Hand contains " + " ".join(map(str, self.cards))
    
    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)
    
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand
        value = 0
        if len(self.cards):
            for card in range(0, len(self.cards)):
                value += VALUES[self.cards[card].get_rank()]
        for card in range(0, len(self.cards)):
            if ("A" in self.cards[card].get_rank()):
                if value + 10 <= 21:
                    value += 10
        return value
    
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in range(0, len(self.cards)):
            self.cards[card].draw(canvas, [pos[0] + card * CARD_SIZE[0]*1.1, pos[1]])

# define deck class
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = []
        for suit in range(0, len(SUITS)):
            for rank in range(0, len(RANKS)):
                self.cards.append(Card(SUITS[suit], RANKS[rank]))
    
    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.cards)
    
    def deal_card(self):
        # deal a card object from the deck
        if len(self.cards):
            return self.cards.pop()
    
    def __str__(self):
        # return a string representing the deck
        return "Deck contains " + " ".join(map(str, self.cards))

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score, scored
    if in_play == True:
        score -= BET_AMOUNT
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()
    deck.shuffle()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    outcome = "Hit or stand?"
    in_play = True
    scored = False

def hit():
    global in_play, player_hand, deck, outcome, score, scored
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
    
    # if busted, assign a message to outcome, update in_play and
    if not scored:
        if player_hand.get_value() > 21:
            outcome = "Player has busted. New game?"
            score -= BET_AMOUNT
            in_play = False
            scored = True

def stand():
    global in_play, player_hand, dealer_hand, deck, outcome, score, scored
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
    in_play = False
    
    # assign a message to outcome, update in_play and score
    if not scored:
        if dealer_hand.get_value() > 21:
            outcome = "Dealer has busted. New game?"
            score += BET_AMOUNT
            scored = True
        elif player_hand.get_value() == dealer_hand.get_value():
            outcome = "Tie. Dealer wins. New game?"
            score -= BET_AMOUNT
            scored = True
        elif player_hand.get_value() > dealer_hand.get_value():
            outcome = "Player wins. New game?"
            score += BET_AMOUNT
            scored = True
        elif player_hand.get_value() < dealer_hand.get_value():
            outcome = "Dealer wins. New game?"
            score -= BET_AMOUNT
            scored = True

# draw handler
def draw(canvas):
    global in_play, score
    canvas.draw_text("Blackjack", (170, 60), 50, 'Black', 'monospace')
    player_hand.draw(canvas, [35,400])
    dealer_hand.draw(canvas, [35,100])
    if in_play:
        canvas.draw_image(card_back, (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1]), (CARD_BACK_SIZE[0], CARD_BACK_SIZE[1]), (35 + CARD_BACK_CENTER[0], 100 + CARD_BACK_CENTER[1]), (CARD_BACK_SIZE[0],CARD_BACK_SIZE[1]))
    canvas.draw_text(outcome, (35, 540), 25, 'Black', 'monospace')
    canvas.draw_text("Score: " + str(score), (35, 575), 20, 'Black', 'monospace')

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()