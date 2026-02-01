from cards import Deck, Hand  # Importing your existing classes

class BlackjackEnv:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

    def reset(self):
        """Resets the game and deals the first 4 cards."""
        self.deck.reset()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        
        # Deal initial cards (matches your original logic)
        self.player_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())
        self.player_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())
        
        return self._get_state()

    def step(self, action):
        """
        Action 0: Stick
        Action 1: Hit
        Returns: (state, reward, done)
        """
        # --- PLAYER HITS (Action 1) ---
        if action == 1:
            self.player_hand.add_card(self.deck.draw())
            
            # Check for Bust
            if self.player_hand.get_value() > 21:
                return self._get_state(), -1, True  # Reward -1, Game Over
            else:
                return self._get_state(), 0, False  # Reward 0, Keep Playing
        
        # --- PLAYER STICKS (Action 0) ---
        else:
            # Dealer plays out their turn (Standard Rule: Hit until >= 17)
            while self.dealer_hand.get_value() < 17:
                self.dealer_hand.add_card(self.deck.draw())
            
            # Calculate Winner
            p_val = self.player_hand.get_value()
            d_val = self.dealer_hand.get_value()
            
            if d_val > 21:
                return self._get_state(), 1, True   # Dealer busted, You win (+1)
            elif p_val > d_val:
                return self._get_state(), 1, True   # You have higher score (+1)
            elif p_val < d_val:
                return self._get_state(), -1, True  # Dealer has higher score (-1)
            else:
                return self._get_state(), 0, True   # Tie (0)

    def _get_state(self):
        """
        Converts your objects into the standard RL tuple:
        (Player Score, Dealer Show Card Value, Usable Ace)
        """
        # 1. Player Score
        score = self.player_hand.get_value()
        
        # 2. Dealer Show Card (The first card dealt to dealer)
        # We need to convert the card object to a number (1-10)
        show_card = self.dealer_hand.cards[0]
        
        # Quick helper to safely get value from your card class
        # (Assumes your cards have a .rank attribute based on your print statement)
        try:
            if str(show_card.rank) in ['Jack', 'Queen', 'King']:
                card_val = 10
            elif str(show_card.rank) == 'Ace':
                card_val = 11
            else:
                card_val = int(show_card.rank)
        except:
            card_val = 10 # Fallback
            
        # 3. Usable Ace
        # (A simplified check: do we have an Ace and is the score <= 21?)
        # For a perfect implementation, check if value is 'soft' (counted as 11)
        # But for this assignment, just checking if an Ace exists is usually enough context
        has_ace = any(str(c.rank) == 'Ace' for c in self.player_hand.cards)
        
        return (score, card_val, has_ace)