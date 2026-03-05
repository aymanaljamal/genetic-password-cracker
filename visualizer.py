# visualizer.py
"""
Plotting and visualization of Genetic Algorithm results
"""
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table
import os


def plot_convergence(convergence_data, title, filename=None):
    """
    Plot algorithm convergence curve

    Args:
        convergence_data: Convergence data (list of dictionaries)
        title: Plot title
        filename: File name for saving (optional)
    """

    if not convergence_data:
        print(" No convergence data to plot.")
        return

    # Extract data
    generations = []
    best_fitnesses = []
    avg_fitnesses = []
    for d in convergence_data:
        generations.append(d['generation'])
        best_fitnesses.append(d['best_fitness'])
        avg_fitnesses.append(d['avg_fitness'])

    calculated_step = len(generations) // 20
    if calculated_step < 1:
        marker_step = 1
    else:
        marker_step = calculated_step


    plt.figure(figsize=(12, 6))


    plt.plot(
        generations,
        best_fitnesses,
        label='Best Fitness',
        color='#2E86AB',
        linewidth=2.5,
        marker='o',
        markersize=3,
        markevery=marker_step
    )


    plt.plot(
        generations,
        avg_fitnesses,
        label='Average Fitness',
        color='#A23B72',
        linewidth=2,
        linestyle='--',
        alpha=0.7
    )


    plt.xlabel('Generation', fontsize=12, fontweight='bold')
    plt.ylabel('Fitness (Matching Bits)', fontsize=12, fontweight='bold')
    plt.title(title, fontsize=14, fontweight='bold', pad=20)
    plt.legend(fontsize=11, loc='lower right')
    plt.grid(True, alpha=0.3, linestyle=':', linewidth=0.8)


    plt.gca().set_facecolor('#F8F9FA')


    plt.xlim(0, max(generations))
    plt.ylim(min(avg_fitnesses) - 2, 32)

    # Save plot
    if filename:
        os.makedirs('results/plots', exist_ok=True)
        plt.savefig(
            f'results/plots/{filename}.png',
            dpi=300,
            bbox_inches='tight',
            facecolor='white'
        )
        print(f" Plot saved: results/plots/{filename}.png")

    plt.tight_layout()
    plt.show()

def plot_comparison(all_results):
    """
    Compare results of multiple experiments

    Args:
        all_results: Dictionary containing results for each experiment
                    {config_name: convergence_data}
    """
    plt.figure(figsize=(14, 7))

    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']
    idx = 0
    for config_name in all_results:
        convergence_data = all_results[config_name]
        generations = []
        best_fitnesses = []
        for d in convergence_data:
            generations.append(d['generation'])
            best_fitnesses.append(d['best_fitness'])

        color_index = idx % len(colors)
        current_color = colors[color_index]

        plt.plot(generations, best_fitnesses,
                 label=config_name,
                 color=current_color,
                 linewidth=2,
                 alpha=0.8)

        idx = idx + 1

    plt.xlabel('Generation', fontsize=12, fontweight='bold')
    plt.ylabel('Best Fitness', fontsize=12, fontweight='bold')
    plt.title('Comparison of Different Parameter Configurations',
              fontsize=14, fontweight='bold', pad=20)
    plt.legend(fontsize=10, loc='lower right')
    plt.grid(True, alpha=0.3, linestyle=':', linewidth=0.8)
    plt.gca().set_facecolor('#F8F9FA')

    os.makedirs('results/plots', exist_ok=True)
    plt.savefig('results/plots/comparison.png',
                dpi=300,
                bbox_inches='tight',
                facecolor='white')
    print(f" Comparison plot saved: results/plots/comparison.png")

    plt.tight_layout()
    plt.show()





def print_summary_table(results_summary):
    console = Console()
    table = Table(title="Experiment Results Summary")
    table.add_column("Configuration", style="cyan", no_wrap=True)
    table.add_column("Generations", style="magenta")
    table.add_column("Time (s)", justify="right", style="green")
    table.add_column("Success", justify="center")

    for res in results_summary:

        if res['success']:

            success_str = " Yes"
            success_style = "bold green"
        else:

            success_str = " No"
            success_style = "bold red"

        table.add_row(
            str(res['config']),
            str(res['generations']),
            f"{res['time']:.2f}",
            f"[{success_style}]{success_str}[/{success_style}]"
        )


    console.print("\n")
    console.print(table)
    console.print("\n")