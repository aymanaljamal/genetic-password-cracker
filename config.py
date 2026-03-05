# config.py
"""
Configuration settings for the Genetic Algorithm
"""

PASSCODE_LENGTH = 32      # Password length (32 bits)
MAX_GENERATIONS = 1000    # Maximum number of generations

# Default GA parameters
POPULATION_SIZE = 100     # Population size (number of individuals)
MUTATION_RATE = 0.01      # Mutation rate (1%)
CROSSOVER_RATE = 0.8      # Crossover rate (80%)
TOURNAMENT_SIZE = 3       # Tournament size for selection


# Multiple configurations for experiments and comparison
EXPERIMENT_CONFIGS = [

    {
        'name': 'Small_Population',
        'pop_size': 60,
        'mutation_rate': 0.01,
        'crossover_rate': 0.8,
        'tournament_size': 3
    },
    {
        'name': 'Medium_Population',
        'pop_size': 120,
        'mutation_rate': 0.01,
        'crossover_rate': 0.8,
        'tournament_size': 3
    },
    {
        'name': 'Large_Population',
        'pop_size': 240,
        'mutation_rate': 0.01,
        'crossover_rate': 0.8,
        'tournament_size': 3
    },


    {
        'name': 'High_Mutation',
        'pop_size': 120,
        'mutation_rate': 0.05,
        'crossover_rate': 0.8,
        'tournament_size': 3
    },
    {
        'name': 'Low_Mutation',
        'pop_size': 120,
        'mutation_rate': 0.001,
        'crossover_rate': 0.8,
        'tournament_size': 3
    },


    {
        'name': 'Low_Crossover',
        'pop_size': 120,
        'mutation_rate': 0.01,
        'crossover_rate': 0.6,
        'tournament_size': 3
    },
    {
        'name': 'High_Crossover',
        'pop_size': 120,
        'mutation_rate': 0.01,
        'crossover_rate': 0.9,
        'tournament_size': 3
    },

    {
        'name': 'Small_Tournament',
        'pop_size': 120,
        'mutation_rate': 0.01,
        'crossover_rate': 0.8,
        'tournament_size': 2
    },
    {
        'name': 'Large_Tournament',
        'pop_size': 120,
        'mutation_rate': 0.01,
        'crossover_rate': 0.8,
        'tournament_size': 5
    }
]
