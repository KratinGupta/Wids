import numpy as np
from collections import defaultdict
from blackjack import BlackjackEnv

# 1. The Fixed Policy
def simple_policy(state):
    """
    Returns 0 (Stick) if score is 20 or 21.
    Returns 1 (Hit) otherwise (0-19).
    """
    player_score, _, _ = state
    if player_score >= 20:
        return 0 # Stick
    else:
        return 1 # Hit

# 2. Episode Generator
def generate_episode(env, policy):
    """
    Plays one full game and returns the history:
    [(state, action, reward), (state, action, reward), ...]
    """
    episode = []
    state = env.reset() #env is what is returned from blackjack.py that is ((score(some of values till now), card_val(value of card of dealer), has_ace)

    done = False
    
    while not done:
        action = policy(state)
        next_state, reward, done = env.step(action)
        episode.append((state, action, reward))
        state = next_state
        
    return episode

# 3. First-Visit Monte Carlo Algorithm
def mc_prediction(env, num_episodes, policy):
    # Dictionaries to store sum of returns and count of visits
    returns_sum = defaultdict(float)  #stores how much reward is earned over all the episode from a particular state
    returns_count = defaultdict(float) #stores how many times a particular state has been visited
    #here a state is Player_Sum, Dealer_Card, Usable_Ace
    V = defaultdict(float) # The Value Function (Average)
    #The actual averages (sum / count).
    print(f"Running MC Prediction for {num_episodes} episodes...")

    for i in range(num_episodes):
        # A. Generate an episode
        episode = generate_episode(env, policy)
        
        # B. Calculate Returns (G)
        # In Blackjack, reward is only at the end, so G is the same for all steps
        # G = Final Reward (-1, 0, or +1)
        G = episode[-1][2] 
        
        # C. First-Visit Check
        # We need to track states we've already counted this episode
        visited_states = set()
        #A Python set is a collection that cannot have duplicates. We use it as a "Checklist" for the current episode.
        
        for step in episode:
            state = step[0]
            
            # If this is the FIRST time seeing this state in this episode...
            if state not in visited_states:
                visited_states.add(state)
                
                # Update averages
                returns_sum[state] += G
                returns_count[state] += 1
                V[state] = returns_sum[state] / returns_count[state]

    return V

# --- Main Execution ---
if __name__ == "__main__":
    env = BlackjackEnv()
    
    # Run 10,000 episodes
    value_function = mc_prediction(env, num_episodes=10000, policy=simple_policy)

    # --- The Deliverable ---
    print("\n" + "="*40)
    print("RESULTS (Value of States)")
    print("="*40)
    
    # We need to find a state with score 21 and score 5
    # Note: State is (Score, DealerCard, UsableAce)
    # We'll just look for ANY state with those scores to print an example
    
    # Filter for Score 21
    states_21 = [s for s in value_function.keys() if s[0] == 21]
    # Filter for Score 5
    states_5  = [s for s in value_function.keys() if s[0] == 5]

    print(f"Value of having 21 (Example: {states_21[0]}): {value_function[states_21[0]]:.4f}")
    if states_5:
        print(f"Value of having 5  (Example: {states_5[0]}):  {value_function[states_5[0]]:.4f}")
    else:
        print("Value of having 5: State not visited (Very rare to stay at 5 in this policy!)")