# genetic_algorithm.py

from utils import (
    initialize_population,
    calculate_fitness,
    tournament_selection,
    single_point_crossover,
    bit_flip_mutation
)


def genetic_algorithm(target, pop_size=100, max_generations=1000,
                      mutation_rate=0.01, tournament_size=3, verbose=True):
    """
    Complete Genetic Algorithm to guess the password

    Steps:
    1. Generate initial population
    2. For each generation:
        a. Calculate fitness for each individual
        b. Check if solution is found
        c. Select the best (Selection)
        d. Crossover
        e. Mutation
    3. Return best solution

    Args:
        target: Target password
        pop_size: Population size
        max_generations: Maximum number of generations
        mutation_rate: Mutation rate
        tournament_size: Tournament size for selection
        verbose: Print progress

    Returns:
        tuple: (best individual, convergence data, number of generations)
    """


    chromosome_length = len(target)
    population = initialize_population(pop_size, chromosome_length)
    convergence_data = []  # To save data for each generation

    if verbose:
        print(f"\n Starting Genetic Algorithm")
        print(f"   Target: {target}")
        print(f"   Population size: {pop_size}")
        print(f"   Mutation rate: {mutation_rate}")
        print("=====================================================================================")


    for generation in range(max_generations):


        fitnesses = []
        for ind in population:
            score = calculate_fitness(ind, target)
            fitnesses.append(score)


        best_fitness = max(fitnesses)
        best_index = fitnesses.index(best_fitness)
        best_individual = population[best_index]


        avg_fitness = sum(fitnesses) / len(fitnesses)


        convergence_data.append({
            'generation': generation,
            'best_fitness': best_fitness,
            'avg_fitness': avg_fitness
        })


        if verbose and generation % 50 == 0:
            print(f"Generation {generation:4d} | "
                  f"Best fitness: {best_fitness:2d}/{chromosome_length} | "
                  f"Average fitness: {avg_fitness:.2f}")

        if best_fitness == chromosome_length:
            if verbose:
                print("====================================================================================")
                print(f" Password found")
                print(f"   Generation: {generation}")
                print(f"   Solution: {best_individual}")
                print(f"   Target: {target}")
            return best_individual, convergence_data, generation


        new_population = []


        while len(new_population) < pop_size:


            parent1 = tournament_selection(population, fitnesses, tournament_size)
            parent2 = tournament_selection(population, fitnesses, tournament_size)


            children = single_point_crossover(parent1, parent2)
            child1 = children[0]
            child2 = children[1]


            child1 = bit_flip_mutation(child1, mutation_rate)
            child2 = bit_flip_mutation(child2, mutation_rate)


            new_population.append(child1)
            if len(new_population) < pop_size:
                new_population.append(child2)


        population = new_population


    if verbose:
        print("====================================================================================")
        print(f" Solution not found in {max_generations} generations")
        print(f"   Best solution: {best_individual}")
        print(f"   Fitness: {best_fitness}/{chromosome_length}")

    return best_individual, convergence_data, max_generations