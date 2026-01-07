import random
from enum import Enum

#Enum for Suits to prevent typos and manage .
#An Enum (short for Enumeration) is a way to define a set of named,
#constant values that belong together.
#Think of it as a Drop-Down Menu in code. 
#It forces you to choose from a specific list of options, rather than
#typing in raw text or number
class Suit(Enum):
    SPADES = "♠"
    HEARTS = "♥"
    CLUBS = "♣"
    DIAMONDS = "♦"

class Card:
    def __init__(self, rank, suit: Suit):
        self.rank = rank
        self.suit = suit.value

    @property 
    #Using property we can use a method as an attribute
    # A object is like a real world thing like a dog.
    # A attribute is like a characteristic of that thing like color, breed etc.
    # like dog.breed, dog.color.
    # A method is like an action the object can perform like dog.bark().
    # So here we can use card.value instead of card.value().

    def value(self):
        """Returns the base value of the card."""
        if self.rank in ["J", "Q", "K"]:
            return 10
        elif self.rank == "A":
            return 11
        return int(self.rank)

    def get_lines(self):
        """
        Breaking the card into a list of strings (lines)
        so they can be stitched horizontally later.
        """
        rank_str = str(self.rank)
        # Handle spacing for "10" vs single digits
        space = " " if len(rank_str) == 1 else ""
        
        return [
            "┌─────────┐",
            f"│ {rank_str}{space}      │",
            f"│    {self.suit}    │",
            f"│      {space}{rank_str} │",
            "└─────────┘"
        ]

    def __str__(self):
        return "\n".join(self.get_lines())

class Deck:
    def __init__(self):
        self.cards = []
        self.reset()

    def reset(self):
        """[cite: 103] Refills the deck and shuffles."""
        ranks = [str(n) for n in range(2, 11)] + list("JQKA")
        # [cite: 102] Create a list of Card objects
        self.cards = [Card(rank, suit) for suit in Suit for rank in ranks]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        """
        [cite: 107] Critical Logic: Calculate hand value.
        Handles the Ace (1 or 11) rule dynamically.
        """
        val = 0
        aces = 0
        for card in self.cards:
            val += card.value
            if card.rank == "A":
                aces += 1
        
        # Downgrade Aces from 11 to 1 if the hand is Bust (>21)
        while val > 21 and aces > 0:
            val -= 10
            aces -= 1
        return val

    def __str__(self):
        """
        [cite: 146] The Horizontal Join Logic.
        Stitches the lines of multiple cards side-by-side.
        """
        if not self.cards:
            return ""
        
        # 1. Get the list of lines for every card in the hand
        card_views = [c.get_lines() for c in self.cards]
        
        # 2. Stitch them row by row
        final_string = ""
        # We have 5 lines per card (defined in Card.get_lines)
        for i in range(5): 
            # Join the i-th line of each card with a space separator
            row_pieces = [view[i] for view in card_views]
            final_string += " ".join(row_pieces) + "\n"
            
        return final_string