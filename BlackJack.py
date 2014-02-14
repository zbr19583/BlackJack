# Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://i39.tinypic.com/1nxxcz.png")

#back of card image
CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0


#initial positions of the cards on the table
player_pos = 50, 300
dealer_pos = 50, 100


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


#####################################################
# define card class 
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_SIZE[0] * (0.5 + RANKS.index(self.rank)), CARD_SIZE[1] * (0.5 + SUITS.index(self.suit)))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_SIZE[0] / 2, pos[1] + CARD_SIZE[1] / 2], CARD_SIZE)

    def cover_card(self, canvas, pos):
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_BACK_SIZE[0] / 2, pos[1] + CARD_BACK_SIZE[1] / 2], CARD_BACK_SIZE)
      
        
#####################################################
# define hand class 
class Hand:
    def __init__(self):
        self.hand = []
        self.value = 0
        
    def __str__(self):
        s = ""
        for card in self.hand:
            s += str(card) + " "
        return s 
    
    def add_card(self, card):
        self.hand.append(card)
        
    def get_value(self):
        self.value = 0
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        for card in self.hand:
            self.value += VALUES[card.rank]
        for card in self.hand:
            if card.rank == 'A':
                if (self.value + 10) < 22:
                    self.value += 10
        return self.value
    
    def draw(self, canvas, pos):
        global in_play, dealer_hand
        
        i = 0
        for card in self.hand:
            card.draw(canvas, [pos[0] + i, pos[1]])
            i += 100
            
        if (in_play) and (pos == dealer_pos):
            self.hand[0].cover_card(canvas, pos)
                 

#####################################################
# define deck class 
class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        
        #The below will create a tuple
        #self.deck = [(suit, rank) for suit in SUITS for rank in RANKS]

#	Pair of nested for loops(Alternate way)       
#        for suit in SUITS:
#            for rank in RANKS:
#                card = Card(suit, rank)
#                self.deck.append(card)

#	list comprehension, Don't create card object because you want
#	the Deck class to be independent of other classes

    def shuffle(self):
        random.shuffle(self.deck)
    
    #deal a card object from the deck
    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        s = ""
        for c in self.deck:
            s += str(c) + " "
        return "Deck contains " + s


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score
    
    if in_play == True:
        outcome = "Dealer wins!"
        in_play = False
        score -= 1
    else:
        deck = Deck()
        player_hand = Hand()
        dealer_hand = Hand()
        deck.shuffle()

        player_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())	#using a method requires adding 
        dealer_hand.add_card(deck.deal_card())	#empty parenthesis
        dealer_hand.add_card(deck.deal_card())
        in_play = True

#    print "The dealer's hand is " + str(dealer_hand)
#    print "The player's hand is " + str(player_hand)

def hit():
    global outcome, in_play, deck, score, player_hand
    if in_play:
        player_hand.add_card(deck.deal_card())
        print "The player's hand is " + str(player_hand)
        outcome = ""
    if player_hand.get_value() > 21:
        outcome = "You Busted!"
        in_play  = False
        score -= 1
        print outcome
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global outcome, in_play, deck, score, player_hand, dealer_hand
    if in_play == True:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            print "The dealer's hand is " + str(dealer_hand)
        if dealer_hand.get_value() <= 21:     
            if dealer_hand.get_value() >= player_hand.get_value():
                outcome = "Dealer wins"
                score -= 1
                print outcome
                in_play = False
            else:
                outcome = "You win"
                score += 1
                print outcome
                in_play = False
        else:
            outcome = "Dealer Busts! You win"
            score += 1
            print outcome
            in_play = False
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global player_hand, dealer_hand, in_play, outcome
    canvas.draw_text('Black', (170, 50), 48, 'Black', 'sans-serif')
    canvas.draw_text(' Jack!', (280, 50), 48, 'Red', 'sans-serif')
    canvas.draw_text('Dealer', (105, 90), 24, 'Black', 'serif')
    canvas.draw_text('Player', (105, 290), 24, 'Black', 'serif')
    #If the game is in_play, print the 'Hit or Stand?'
    if in_play:
        canvas.draw_text('Hit or Stand?', (240, 250), 36, 'Black', 'sans-serif')
    #otherwise print the outcome on the screen
    else:
        canvas.draw_text(outcome, (240, 250), 36, 'Blue', 'sans-serif')
    dealer_hand.draw(canvas, dealer_pos)
    player_hand.draw(canvas, player_pos)
    canvas.draw_text('Score: ' + str(score), (450, 100), 24, 'Yellow', 'sans-serif')

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


# remember to review the gradic rubric
