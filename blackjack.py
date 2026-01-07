from cards import Deck, Hand
import time
import os

class BlackjackGame:
    def __init__(self):
        # [cite: 113] Maintains the state: deck, player hand, dealer hand
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

    def clear_screen(self):
        # Simple cross-platform clear screen
        os.system('cls' if os.name == 'nt' else 'clear')

    def play_round(self):
        self.clear_screen()
        print("Starting New Round...")
        
        # 1. Setup & Deal
        self.deck.reset()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

        # [cite: 116] The standard deal (2 cards each)
        self.player_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())
        self.player_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())

        # 2. Player Turn
        player_bust = False
        while True:
            self.display_table(hide_dealer=True)
            
            # Check for immediate Blackjack (21)
            if self.player_hand.get_value() == 21:
                print("\nBlackjack! You have 21!")
                break

            # [cite: 114] Actions: Hit or Stand
            choice = input("\nAction: [H]it or [S]tand? > ").strip().lower()
            
            if choice == 'h':
                new_card = self.deck.draw()
                self.player_hand.add_card(new_card)
                print(f"\nDealt: {new_card.rank} of {new_card.suit}")
                time.sleep(1) # Small delay for UX
                
                # Check for Bust
                if self.player_hand.get_value() > 21:
                    self.display_table(hide_dealer=False)
                    print("\nBUST! You went over 21.")
                    player_bust = True
                    break
            
            elif choice == 's':
                print("\nYou chose to Stand.")
                break
        
        # 3. Dealer Turn (only if player didn't bust)
        if not player_bust:
            print("\n--- Dealer's Turn ---")
            time.sleep(1)
            self.display_table(hide_dealer=False)
            
            # Dealer rules: Must hit until 17 or higher
            while self.dealer_hand.get_value() < 17:
                print("\nDealer hits...")
                time.sleep(1.5)
                self.dealer_hand.add_card(self.deck.draw())
                self.display_table(hide_dealer=False)
        
        # 4. Determine Winner
        self.resolve_winner(player_bust)
        
    def resolve_winner(self, player_bust):
        p_val = self.player_hand.get_value()
        d_val = self.dealer_hand.get_value()

        print("\n" + "="*30)
        print("FINAL RESULTS")
        print("="*30)
        
        if player_bust:
            print(f"You Busted with {p_val}. Dealer Wins.")
        elif d_val > 21:
            print(f"Dealer Busted with {d_val}. YOU WIN!")
        elif p_val > d_val:
            print(f"YOU WIN! ({p_val} vs {d_val})")
        elif p_val < d_val:
            print(f"Dealer Wins. ({d_val} vs {p_val})")
        else:
            print(f"Push (Tie) at {p_val}.")
            
    def display_table(self, hide_dealer=False):
        """
        [cite: 118] TUI Display Logic.
        Handles showing/hiding the dealer's hole card.
        """
        self.clear_screen()
        print(f"Dealer's Hand (Score: {self.dealer_hand.get_value() if not hide_dealer else '?'})")
        
        if hide_dealer:
            # We must manually stitch the hidden card art next to the visible card
            visible_card = self.dealer_hand.cards[0]
            
            # ASCII art for the back of a card
            hidden_card_art = [
                "┌─────────┐",
                "│░░░░░░░░░│",
                "│░░░░?░░░░│",
                "│░░░░░░░░░│",
                "└─────────┘"
            ]
            
            visible_lines = visible_card.get_lines()
            # Stitch them together
            for i in range(5):
                print(visible_lines[i] + " " + hidden_card_art[i])
        else:
            # If revealed, just use the Hand's string method
            print(self.dealer_hand)

        print(f"\n\nYour Hand (Score: {self.player_hand.get_value()})")
        print(self.player_hand)

if __name__ == "__main__":
    game = BlackjackGame()
    while True:
        game.play_round()
        if input("\nPlay again? (y/n): ").lower() != 'y':
            print("Thanks for playing!")
            break