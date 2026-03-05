# utils.py
"""
Helper functions for the Genetic Algorithm
"""
import random
import csv
def generate_random_passcode(length):
    """
    Generate a random passcode of bits
    """
    result = []
    for i in range(length):
        bit = random.choice(['0', '1'])
        result.append(bit)
    return ''.join(result)
"""
'1010100101010101010101010'
"""


def calculate_fitness(individual, target):
    """
    Calculate how much the individual matches the target (fitness function)
    """
    matches = 0
    for i in range(len(individual)):
        if individual[i] == target[i]:
            matches += 1
    return matches



def initialize_population(pop_size, chromosome_length):
    """
    Create the initial population (random set of individuals)
    """
    population = []
    for i in range(pop_size):
        individual = generate_random_passcode(chromosome_length)
        population.append(individual)
    return population



def tournament_selection(population, fitnesses, tournament_size):
    """
    Select an individual from the population using Tournament Selection
    """
    population_length = len(population)
    all_indices = list(range(population_length))
    tournament_indices = random.sample(all_indices, tournament_size)
    tournament_fitnesses = []
    for single_index in tournament_indices:
        fitness_value = fitnesses[single_index]
        tournament_fitnesses.append(fitness_value)
    best_fitness = max(tournament_fitnesses)
    winner_index_inside = tournament_fitnesses.index(best_fitness)
    winner_index = tournament_indices[winner_index_inside]
    return population[winner_index]


def single_point_crossover(parent1, parent2, crossover_rate=0.8):
    """
    Crossover with a single cut point
    """
    random_value = random.random()
    if random_value > crossover_rate:
        return parent1, parent2
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2



def bit_flip_mutation(individual, mutation_rate):
    """
    Mutation: flip some bits randomly
    """
    individual_list = list(individual)
    for i in range(len(individual_list)):
        random_value = random.random()
        if random_value < mutation_rate:
            if individual_list[i] == '0':
                individual_list[i] = '1'
            else:
                individual_list[i] = '0'
    return ''.join(individual_list)


def save_convergence_data(convergence_data, filename):
    """
    Save convergence data to a CSV file
    """
    f = open(filename, 'w', newline='')
    writer = csv.DictWriter(
        f,
        fieldnames=['generation', 'best_fitness', 'avg_fitness']
    )
    writer.writeheader()
    writer.writerows(convergence_data)
    f.close()

    print(f" Data saved to: {filename}")
