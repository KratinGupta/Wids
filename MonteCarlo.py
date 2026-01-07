import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf

def run_simulation(predicate_func, bounds, num_samples):
    x_min, x_max, y_min, y_max = bounds
    x = np.random.uniform(x_min, x_max, num_samples)
    y = np.random.uniform(y_min, y_max, num_samples)
    inside_mask = predicate_func(x, y)
    area_rect = (x_max - x_min) * (y_max - y_min)

    fraction_inside = np.sum(inside_mask) / num_samples
    estimated_area = area_rect * fraction_inside
    return estimated_area

def solve_circle(n):
    # [cite_start]Predicate: x^2 + y^2 <= 1 [cite: 243]
    # Bounds: [-1, 1] for x and y
    return run_simulation(
        predicate_func=lambda x, y: (x**2 + y**2) <= 1,
        bounds=(-1, 1, -1, 1),
        num_samples=n
    )

def solve_parabola(n):
    # [cite_start]Predicate: Point is "under" curve if y <= x^2 [cite: 244]
    # Bounds: x in [0, 1]. Max y is 1^2 = 1. So y in [0, 1].
    return run_simulation(
        predicate_func=lambda x, y: y <= x**2,
        bounds=(0, 1, 0, 1),
        num_samples=n
    )

def solve_gaussian(n):
    # [cite_start]Predicate: y <= e^(-x^2) [cite: 245]
    # Bounds: x in [0, 2]. Max y is e^0 = 1. So y in [0, 1].
    return run_simulation(
        predicate_func=lambda x, y: y <= np.exp(-x**2),
        bounds=(0, 2, 0, 1),
        num_samples=n
    )


def estimate_e_by_area(num_samples):

    x = np.random.uniform(1, 2, num_samples)
    y = np.random.uniform(0, 1, num_samples)
    
    area = 1/x
    inside_mask = area >= y



    e_estimate = 2**(1/(np.sum(inside_mask)/num_samples))

    return e_estimate
def estimate_e_by_prob(num_samples):
    # Method 2: Forsythe's "Magic" Method (Sequence Length) [cite: 213-221]
    # We need to find n such that u1 > u2 > ... > un <= un+1
    # The expected value of n is e.
    
    # 1. Create a "safety buffer" of columns. 
    # Sequences > 20 are statistically impossible (1/20! chance).
    max_cols = 20
    
    # 2. Generate matrix of random numbers (N rows, 20 cols)
    random_matrix = np.random.uniform(0, 1, (num_samples, max_cols))
    
    # 3. Prepend a column of 1s (u1 = 1.0)
    ones_col = np.ones((num_samples, 1))
    matrix = np.hstack((ones_col, random_matrix))
    
    # 4. Check Strict Decreasing Condition: Col[i] > Col[i+1]
    # This creates a boolean matrix
    condition_met = matrix[:, :-1] > matrix[:, 1:]
    
    # 5. Find length of valid sequence
    # cumprod works like a latch: T, T, F, T -> T, T, F, F
    valid_sequences = np.cumprod(condition_met, axis=1)
    
    # Summing the True values gives the length of the sequence
    # We add 1 because the count includes the starting number u1
    ns = np.sum(valid_sequences, axis=1) + 1
    
    # 6. Average length is our estimate for e
    return np.mean(ns)


# def estimate_pi(num_samples):
    
    

# Test it
if __name__ == "__main__": 
    # Only run simple print test if main
    N = 10000
    print(f"Simulating {N} points...")
    print(f"Estimated Pi: {solve_circle(N)}")
    print(f"Estimated e (Area): {estimate_e_by_area(N)}")
    print(f"Estimated e (Magic): {estimate_e_by_prob(N)}")
    print(f"Actual Pi: {np.pi}")

    print(f"--- Modular Shape Estimator (N={N}) ---")

    # 1. Circle Analysis
    circle_area = solve_circle(N)
    true_pi = np.pi
    print(f"\n[Circle] Estimated Area (Pi): {circle_area:.5f}")
    print(f"[Circle] True Area (Pi):      {true_pi:.5f}")

    # 2. Parabola Analysis
    parabola_area = solve_parabola(N)
    true_parabola = 1/3
    print(f"\n[Parabola] Estimated Area:    {parabola_area:.5f}")
    print(f"[Parabola] True Area (1/3):     {true_parabola:.5f}")

    # 3. Gaussian Analysis
    gaussian_area = solve_gaussian(N)
    
    # Calculating True Gaussian Area using Error Function (erf)
    # Integral of e^-x^2 dx = (sqrt(pi) / 2) * erf(x)
    # Evaluated from 0 to 2
    true_gaussian = (np.sqrt(np.pi) / 2) * erf(2)
    
    print(f"\n[Gaussian] Estimated Area:    {gaussian_area:.5f}")
    print(f"[Gaussian] True Area (erf):     {true_gaussian:.5f}")

def generate_pi_plots():
    print("Running convergence simulation for N = 10^1 to 10^7...")
    
    # [cite_start]# [cite: 262] recommends exponential scaling
    # We use fewer points (20) to keep it fast, but span up to 10^6 or 10^7
    ns = np.logspace(1, 6, num=20, dtype=int) 
    
    # --- Ground Truths for Error Calculation ---
    true_pi = np.pi                                # [cite: 166]
    true_parabola = 1/3                            # [cite: 244]
    true_gaussian = (np.sqrt(np.pi) / 2) * erf(2)  # [cite: 245, 315]
    true_e = np.e                                  # [cite: 202]

    # --- Data Storage ---
    # Shapes
    errors_circle = []
    errors_parabola = []
    errors_gaussian = []
    
    # Euler's Number
    estimates_e_area = []
    errors_e_area = []
    estimates_e_magic = []
    errors_e_magic = []
    
    # --- Simulation Loop ---
    for n in ns:
        # 1. Circle (Pi)
        est_c = solve_circle(n)
        errors_circle.append(abs(est_c - true_pi) / true_pi * 100)
        
        # 2. Parabola
        est_p = solve_parabola(n)
        errors_parabola.append(abs(est_p - true_parabola) / true_parabola * 100)
        
        # 3. Gaussian
        est_g = solve_gaussian(n)
        errors_gaussian.append(abs(est_g - true_gaussian) / true_gaussian * 100)
        
        # 4. e (Method 1: Area)
        est_e1 = estimate_e_by_area(n)
        estimates_e_area.append(est_e1)
        errors_e_area.append(abs(est_e1 - true_e) / true_e * 100)
        
        # 5. e (Method 2: Magic/Prob)
        est_e2 = estimate_e_by_prob(n)
        estimates_e_magic.append(est_e2)
        errors_e_magic.append(abs(est_e2 - true_e) / true_e * 100)

    # --- Plotting ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))

    # Plot 1: Shapes Error Convergence (Log-Log)
    # This fulfills the sub-task requirement to plot errors for Circle, Parabola, Gaussian
    ax1.plot(ns, errors_circle, '-o', label='Circle (Pi)', alpha=0.7)
    ax1.plot(ns, errors_parabola, '-s', label='Parabola (1/3)', alpha=0.7)
    ax1.plot(ns, errors_gaussian, '-^', label='Gaussian (erf)', alpha=0.7)
    
    # [cite_start]Theoretical 1/sqrt(N) line for reference [cite: 261]
    ref_line = 100 / np.sqrt(ns)
    ax1.plot(ns, ref_line, 'k--', label=r'Theoretical $1/\sqrt{N}$', linewidth=2)

    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('Number of Samples (N)')
    ax1.set_ylabel('Percent Error (%)')
    ax1.set_title('Shape Integration Error Convergence')
    ax1.legend()
    ax1.grid(True, which="both", alpha=0.3)

    # Plot 2: Euler's Number Comparison (Area vs Magic)
    ax2.plot(ns, errors_e_area, '-o', color='royalblue', label='Area Method Error', alpha=0.7)
    ax2.plot(ns, errors_e_magic, '-o', color='purple', label='Magic/Prob Method Error', alpha=0.7)
    ax2.plot(ns, ref_line, 'k--', label=r'Theoretical $1/\sqrt{N}$')
    
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel('Number of Samples (N)')
    ax2.set_ylabel('Percent Error (%)')
    ax2.set_title(r"Euler's Number Error Convergence")
    ax2.legend()
    ax2.grid(True, which="both", alpha=0.3)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    generate_pi_plots()

