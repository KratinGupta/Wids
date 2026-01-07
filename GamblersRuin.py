import numpy as np
import matplotlib.pyplot as plt

n_gam = 10000
rounds = 1000
start = 100

outcomes = np.random.choice([-1, 1], size=(n_gam, rounds))
starting_amounts = np.full((n_gam, 1), start)
bankrolls = np.hstack((starting_amounts, outcomes))

changes = np.cumsum(bankrolls, axis=1)
is_ruined = changes <= 0
ruin_mask = np.maximum.accumulate(is_ruined, axis=1)
bankrolls[ruin_mask] = 0
changes[ruin_mask] = 0


#spaghetti plot of paths

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
subset_to_plot = changes[:100]
no_rounds = np.arange(rounds + 1)

for i in range(len(subset_to_plot)):
    ax1.plot(no_rounds, subset_to_plot[i], alpha=0.2, color='gray')

mean_path = np.mean(changes, axis=0)
ax1.plot(no_rounds, mean_path, color='red', linestyle='--', linewidth=2.5, label='Mean Path')

final_wealths = changes[:, -1]
max_winner_idx = np.argmax(final_wealths)
min_winner_idx = np.argmin(final_wealths)
ax1.plot(no_rounds, changes[max_winner_idx], color='green', linewidth=1.5, label='Max Winner')
ax1.plot(no_rounds, changes[min_winner_idx], color='blue', linewidth=1.5, label='Min Winner')

ax1.set_title(f"Monte Carlo Simulation: {n_gam} Gamblers")
ax1.set_xlabel("Rounds")
ax1.set_ylabel("Wealth ($)")
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)

#Histogram of final wealths
ax2.hist(final_wealths, bins=66, color='skyblue', edgecolor='black')

# Add vertical lines indicating the Mean and Median final wealth.
mean_val = np.mean(final_wealths)
median_val = np.median(final_wealths)

ax2.axvline(mean_val, color='red', linestyle='dashed', linewidth=2, label=f'Mean: ${mean_val:.2f}')
ax2.axvline(median_val, color='orange', linestyle='dashed', linewidth=2, label=f'Median: ${median_val:.2f}')

ax2.set_title("Distribution of Final Wealth (Step 1000)")
ax2.set_xlabel("Final Wealth ($)")
ax2.set_ylabel("Frequency")
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()

plt.show()

#The final distribution is a Bell Curve (Normal Distribution) centered at $100.
#This is due to the Central Limit Theorem.
#The spread (Std Dev) is approx sqrt(1000) = 31.62
#The Mean and Median are very close, indicating a symmetric distribution.
#However, there are many players who have gone broke (final wealth = $0),
#which skews the distribution slightly to the left.
