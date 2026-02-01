The agent has to exploit what it already knows in order to obtain
reward, but it also has to explore in order to make better action selections in
the future. The dilemma is that neither exploration nor exploitation can be
pursued exclusively without failing at the task. The agent must try a variety of
actions and progressively favor those that appear to be best.

Beyond the agent and the environment, one can identify four main subelements
of a reinforcement learning system: a policy, a reward signal, a value function,
and, optionally, a model of the environment.
A policy is a mapping from perceived states of the environment to actions to be taken when in those states
On each time step, the environment sends to the reinforcement learning agent a
single number, a reward. The agent’s sole objective is to maximize the total
reward it receives over the long run.
Whereas the reward signal indicates what is good in an immediate sense,
a value function specifies what is good in the long run. Roughly speaking, the
value of a state is the total amount of reward an agent can expect to accumulate
over the future, starting from that state.
The fourth and final element of some reinforcement learning systems is
a model of the environment. This is something that mimics the behavior of
the environment, or more generally, that allows inferences to be made about
how the environment will behave. For example, given a state and action,
the model might predict the resultant next state and next reward. Models
are used for planning, by which we mean any way of deciding on a course of
action by considering possible future situations before they are actually experienced.

methods search in spaces of policies
defined by a collection of numerical parameters. They estimate the directions
the parameters should be adjusted in order to most rapidly improve a policy’s
performance. Unlike evolutionary methods, however, they produce these estimates while the agent is interacting with its environment and so can take
advantage of the details of individual behavioral interactions. Methods like
this, called policy gradient methods

any problem of learning goal-directed behavior
can be reduced to three signals passing back and forth between an agent and
its environment: one signal to represent the choices made by the agent (the
actions), one signal to represent the basis on which the choices are made (the
states), and one signal to define the agent’s goal (the rewards)

The additional concept that we need is that of discounting. According to
this approach, the agent tries to select actions so that the sum of the discounted
rewards it receives over the future is maximized. In particular, it chooses At
to maximize the expected discounted return:
Gt = Rt+1 + γRt+2 + γ^2(Rt+3) + · · ·
The discount rate determines the present value of future rewards: a reward
received k time steps in the future is worth only γ^k−1 times what it would be
worth if it were received immediately'

We use gama because we are uncertain about how accurate the model is and exploratory chances.

A state signal that succeeds in retaining all relevant information is said to be Markov, or to have
the Markov property (we define this formally below). For example, a checkers position—the current
configuration of all the pieces on the board—would serve as a Markov state because it
summarizes everything important about thecomplete sequence of positions that led to it. Much of the information about
the sequence is lost, but all that really matters for the future of the game is
retained.
A reinforcement learning task that satisfies the Markov property is called a
Markov decision process, or MDP. If the state and action spaces are finite,
then it is called a finite Markov decision process (finite MDP).

Monte Carlo Sims:

Dynamic Programming (Previous Chapter): Requires a "Model" of the environment.
You need to know the exact probability of moving from State A to State B and exactly
what reward you get. It solves the problem mathematically like solving a system of equations.

Monte Carlo (This Chapter): Requires only experience. It learns by playing the game,
observing what happens, and keeping score.

Actual Experience: The agent interacts with the real world (e.g., a robot walking). It doesn't need to know physics equations; it just tries to walk and learns from falling down.

Simulated Experience: You use a computer simulation. The text notes a crucial distinction here:

Dynamic Programming needs the Probability Distributions (e.g., "There is a 30% chance of rain, 70% sun"). This is hard to calculate for complex systems.

Monte Carlo only needs Samples (e.g., "I ran the sim, and it rained"). It is much easier to write a simulator that just does something than one that calculates the probabilities of everything it might do

Monte Carlo methods can
thus be incremental in an episode-by-episode sense, but not in a step-by-step
(online) sense

Monte Carlo methods sample and average returns for each state–action pair
and average rewards for each action.
the return after taking an action in one state depends on the actions
taken in later states in the same episode.

First-Visit MC
This method asks: "What was the total score from the first time we ever saw State A?" Like if we go A-->B--->A--->C then it will add reward for A to B then B to A then A to C ignoring the fact that we visit A twice.

Every-Visit MC
This method asks: "Every time we stood in State A, how much reward did we get after that?"
Like if we go A-->B--->A--->C then it will add reward for A to B then B to A then A to C and then just A to C. It will add both into account.

Both first-visit MC and every-visit MC converge to vπ(s) as the number
of visits (or first visits) to s goes to infinity

The general idea of a backup diagram is to show at the top the root node to be
updated and to show below all the transitions and leaf nodes whose rewards
and estimated values contribute to the update. For Monte Carlo estimation of
vπ, the root is a state node, and below it is the entire trajectory of transitions
along a particular single episode, ending at the terminal state
A --r=5--> B --r=6--> C (backup diagram for monte carlo)

An important fact about Monte Carlo methods is that the estimates for
each state are independent. The estimate for one state does not build upon
the estimate of any other state, as is the case in DP

Model vs policy
The policy represents how the agent behaves. It is the decision-making logic.
Function: It takes a State as input and outputs an Action (or probabilities of actions).

The model represents how the environment works. It is a simulation of the physics or rules of the game.
Function: It takes a State and an Action as input, and predicts the Next State and Reward.

State value vs Action Value function:
State Value Function (vpi(s)) = The expected total reward you will get if you start in state $s$ and follow policy $\pi$ forever.

Action Value Function (qpi)(s, a) = This is the value of taking a specific action in a state. Q-Learning (estimating Action Values)

The policy evaluation problem for action values is to estimate qπ(s, a),
the expected return when starting in state s, taking action a, and thereafter
following policy π. The Monte Carlo methods for this are essentially the same
as just presented for state values, except now we talk about visits to a state–
action pair rather than to a state. A state–action pair s, a is said to be visited
in an episode if ever the state s is visited and action a is taken in it. The everyvisit MC method estimates the value of a state–action pair as the average of the
returns that have followed visits all the visits to it.

The problem with this is that the agent would keep visiting same action value pairs in each episdode and the model will not learns...so we explore. For policy evaluation
to work for action values, we must assure continual exploration

One way to explore is
to do this by specifying that the episodes start in a state–action pair, and
that every pair has a nonzero probability of being selected as the start. This
guarantees that all state–action pairs will be visited an infinite number of times
in the limit of an infinite number of episodes. We call this the assumption of
exploring starts.

generalized policy iteration (GPI): In GPI one maintains both an
approximate policy and an approximate value function. The value function is
repeatedly altered to more closely approximate the value function for the current policy, and the policy is repeatedly improved with respect to the current value function

let us assume that we do indeed observe an infinite number of episodes and
that, in addition, the episodes are generated with exploring starts. Under
these assumptions, the Monte Carlo methods will compute each qπk
exactly,for arbitrary πk.
Policy improvement is done by making the policy greedy with respect to
the current value function. In this case we have an action-value function, and
therefore no model is needed to construct the greedy policy. For any actionvalue function q, the corresponding greedy policy is the one that, for each
s ∈ S, deterministically chooses an action with maximal action-value:
π(s) = arg max q(s, a)

How can we avoid the unlikely assumption of exploring starts? The only
general way to ensure that all actions are selected infinitely often is for the
agent to continue to select them. There are two approaches to ensuring this,
resulting in what we call on-policy methods and off-policy methods.

On policy methods attempt to evaluate or improve the policy that is used to make
decisions, whereas off-policy methods evaluate or improve a policy different
from that used to generate the data.
