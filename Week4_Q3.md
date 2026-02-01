a) 
The Markov Property states that "The future depends only on the present, not on the past."

In your Python code (Infinite Deck): The probability of drawing a King is always 1/13. It doesn't matter what happened 5 minutes ago. The current hand tells you everything you need to know.

In a Real Casino (Shoe of 6 Decks): If 20 Kings have already been played, the probability of drawing a King now is almost zero.

The Problem: If your state is just (12, 10), the agent assumes the odds are standard. But the actual odds depend on the "hidden" history of discarded cards. Because the current state description fails to capture this history, the environment appears "Non-Stationary" (the rules of probability seem to change randomly), violating the Markov assumption.


b)
To make the environment Markovian again, you must include the "missing information" in the State Tuple. You need to track the Running Count (e.g., Hi-Lo Count).

Current State: (PlayerSum, DealerCard, UsableAce)

New State: (PlayerSum, DealerCard, UsableAce, RunningCount)

By adding RunningCount (an integer that goes up when low cards appear and down when high cards appear), the agent can distinguish between a "State 12 vs 10 in a hot deck" (Hit!) and a "State 12 vs 10 in a cold deck" (Stick!).

c)
The convergence speed will decrease drastically (it will take much, much longer to learn). This is known as the Curse of Dimensionality.

Original Space: ~200 possible states (Combinations of sums 12-21 and dealer cards).

New Space: If the "Running Count" can range from -20 to +20, you now have roughly 40 times as many states (~8,000 states).

The Monte Carlo agent needs to visit every single state thousands of times to calculate a stable average. If you multiply the number of rooms in the house by 40, it takes the robot 40 times longer to map the building. You would likely need millions of episodes instead of 500,000 to get a good strategy.


B)
for first visit
it would be
+1 -1 +10 = 10 (recorded once)

for every visit
it would be
+1 -1 +10
+10(recorded twice as it landed on A twice.)