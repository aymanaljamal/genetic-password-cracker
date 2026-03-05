# main.py
"""
Main program to run the Genetic Algorithm
"""
import time
import os
from config import PASSCODE_LENGTH, EXPERIMENT_CONFIGS
from utils import generate_random_passcode, save_convergence_data
from genetic_algorithm import genetic_algorithm
from visualizer import plot_convergence, plot_comparison, print_summary_table


def run_single_experiment(target, config):
    """
    Run a single experiment

    Args:
        target: Target password
        config: Experiment settings

    Returns:
        dict: Experiment results
    """
    print(f"\n{'==================================================================================='}")
    print(f" Experiment: {config['name']}")
    print(f"{'===================================================================================='}")
    print(f" Settings:")
    print(f"   - Population size: {config['pop_size']}")
    print(f"   - Mutation rate: {config['mutation_rate']}")
    print(f"   - Tournament size: {config['tournament_size']}")

    start_time = time.time()


    best_solution, convergence_data, generations = genetic_algorithm(
        target=target,
        pop_size=config['pop_size'],
        mutation_rate=config['mutation_rate'],
        tournament_size=config['tournament_size'],
        verbose=True
    )

    elapsed_time = time.time() - start_time


    success = (best_solution == target)

    print(f"\n  Time elapsed: {elapsed_time:.2f} seconds")


    data_filename = f"results/{config['name']}_convergence.csv"
    save_convergence_data(convergence_data, data_filename)


    plot_convergence(
        convergence_data,
        title=f"Convergence: {config['name']}",
        filename=config['name']
    )

    return {
        'config': config['name'],
        'generations': generations,
        'time': elapsed_time,
        'success': success,
        'convergence_data': convergence_data
    }


def main():
    """
    Main function
    """
    print("===================================================================================")
    print(" Password Cracker using Genetic Algorithm".center(80))
    print("===================================================================================")


    os.makedirs('results/plots', exist_ok=True)


    print(f"\n Generating random password ({PASSCODE_LENGTH} bits)...")
    target_passcode = generate_random_passcode(PASSCODE_LENGTH)
    print(f"   Target password: {target_passcode}")


    all_results = {}
    results_summary = []

    for config in EXPERIMENT_CONFIGS:
        result = run_single_experiment(target_passcode, config)
        all_results[config['name']] = result['convergence_data']
        results_summary.append(result)

    print(f"\n{'===================================================================================='}")
    print(" Plotting comparison of all experiments...")
    plot_comparison(all_results)


    print_summary_table(results_summary)


    best_result = None
    min_score = float('inf')
    for result in results_summary:
        if result['success']:

            current_score = result['generations']
        else:
            current_score = float('inf')
        if current_score < min_score:

            min_score = current_score
            best_result = result

    print(" Best Experiment:")
    print(f"   - Configuration: {best_result['config']}")
    print(f"   - Number of generations: {best_result['generations']}")
    print(f"   - Time: {best_result['time']:.2f} seconds")

    print("\n Program completed successfully!")
    print(f" Results saved in folder: results/")


if __name__ == "__main__":
    main()