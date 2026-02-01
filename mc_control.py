import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from blackjack import BlackjackEnv

# --- Configuration ---
NUM_EPISODES = 500_000  
EPSILON = 0.05           # Exploration rate (10% random moves)
ALPHA = 0.01          # Learning rate (Small step size for stability)
GAMMA = 1.0           # Discount factor (No discounting needed for Blackjack)
#Q is not an array. It is a Dictionary (Hash Map).
#for every state array is stores an array [q_stick, q_hit]
#The variable state looks like this: (16, 10, False).

def get_best_action(Q, state):
    """
    Returns the action with the highest Q-value for a given state.
    If values are equal (e.g., all zeros), returns a random action.
    """
    # Q[state] is a numpy array [q_stick, q_hit]
    # We break ties randomly to encourage initial exploration
    values = Q[state] #Q[state] returns a list of two numbers: [Value_of_Stick, Value_of_Hit].
    if values[0] == values[1]:
        return np.random.choice([0, 1])
    return np.argmax(values)

def epsilon_greedy_policy(Q, state, epsilon):
    """
    Step 2: E-greedy policy.
    With prob epsilon: Random Action.
    With prob 1-epsilon: Best Action (Greedy).
    """
    if np.random.random() < epsilon:
        return np.random.choice([0, 1])
    else:
        return get_best_action(Q, state)

def generate_episode(env, Q, epsilon):
    """
    Plays one full game using the epsilon-greedy policy.
    Returns: List of (state, action, reward)
    """
    episode = []
    state = env.reset()
    done = False
    
    while not done:
        action = epsilon_greedy_policy(Q, state, epsilon)
        next_state, reward, done = env.step(action)
        episode.append((state, action, reward))
        state = next_state
        
    return episode

def train_mc_control(env, num_episodes):
    # 1. Initialize Q(s, a) arbitrarily
    # We use a defaultdict that returns [0.0, 0.0] for any new state
    Q = defaultdict(lambda: np.zeros(2))
    
    # Track rewards for the Learning Curve
    all_rewards = []
    
    print(f"Starting training for {num_episodes} episodes...")
    
    # 3. The Loop
    for i in range(1, num_episodes + 1):
        # A. Generate an episode
        episode = generate_episode(env, Q, EPSILON)
        
        # B. Calculate Returns & Update Q
        # Since Blackjack is episodic and reward is only at the end, 
        # G is the same for every step in the episode.
        G = episode[-1][2] 
        all_rewards.append(G)
        
        visited_in_episode = set()
        
        for state, action, reward in episode:
            state_action_pair = (state, action)
            
            # First-Visit Check (Standard MC stability)
            if state_action_pair not in visited_in_episode:
                visited_in_episode.add(state_action_pair)
                
                # C. Update Q(s,a) using incremental mean
                # Q_new = Q_old + alpha * (Target - Q_old)
                old_val = Q[state][action]
                Q[state][action] = old_val + ALPHA * (G - old_val)
        
        # Progress Log
        if i % 50_000 == 0:
            avg_r = np.mean(all_rewards[-1000:])
            print(f"Episode {i}/{num_episodes} | Avg Reward (Last 1k): {avg_r:.4f}")

    return Q, all_rewards

# --- Visualization Functions ---

def plot_learning_curve(rewards, window=5000):
    """
    Task 3.1: Plot 'Rolling Average Reward'
    """
    # Calculate rolling average using convolution for speed
    rolling_avg = np.convolve(rewards, np.ones(window)/window, mode='valid')
    
    plt.figure(figsize=(10, 5))
    plt.plot(rolling_avg, color='blue', label=f'Rolling Avg (Window={window})')
    plt.title("Learning Curve: Agent Performance Over Time")
    plt.xlabel("Episodes")
    plt.ylabel("Average Reward")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def plot_strategy_card(Q):
    """
    Task 3.2: Heatmap of Optimal Actions
    X-axis: Dealer Showing Card (2-11)
    Y-axis: Player Sum (12-21) - We ignore <12 because you always Hit.
    """
    # Define ranges
    dealer_range = range(2, 12) # 2 to Ace (11)
    player_range = range(21, 11, -1) # 21 down to 12
    
    # We need two grids: One for "Usable Ace" (Soft), One for "No Usable Ace" (Hard)
    
    def get_grid(usable_ace):
        grid = np.zeros((len(player_range), len(dealer_range)))
        for i, player in enumerate(player_range):
            for j, dealer in enumerate(dealer_range):
                state = (player, dealer, usable_ace)
                # Optimal action is max of Q-values
                action = np.argmax(Q[state]) 
                grid[i, j] = action
        return grid

    # Create plots
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # 1. Hard Hands (No Ace)
    sns.heatmap(get_grid(False), ax=axes[0], cmap="RdYlGn", 
                xticklabels=dealer_range, yticklabels=player_range, cbar=False, annot=True)
    axes[0].set_title("Hard Hands (No Usable Ace)\n0 = Stick (Red) | 1 = Hit (Green)")
    axes[0].set_xlabel("Dealer Showing")
    axes[0].set_ylabel("Player Sum")
    
    # 2. Soft Hands (Usable Ace)
    sns.heatmap(get_grid(True), ax=axes[1], cmap="RdYlGn", 
                xticklabels=dealer_range, yticklabels=player_range, cbar=False, annot=True)
    axes[1].set_title("Soft Hands (Usable Ace)\n0 = Stick (Red) | 1 = Hit (Green)")
    axes[1].set_xlabel("Dealer Showing")
    axes[1].set_ylabel("Player Sum")
    
    plt.tight_layout()
    plt.show()

# --- Main Execution ---
if __name__ == "__main__":
    env = BlackjackEnv()
    
    # Run Training
    optimal_Q, rewards = train_mc_control(env, num_episodes=NUM_EPISODES)
    
    # Run Visualization
    plot_learning_curve(rewards)
    plot_strategy_card(optimal_Q)