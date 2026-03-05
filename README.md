# Genetic Password Cracker (GA)

A Python project that demonstrates how a **Genetic Algorithm (GA)** can be used to simulate password cracking.  
The system evolves candidate solutions across generations until the target password is discovered.

This project also provides a **GUI interface** to run multiple experiments and compare algorithm configurations.

---

## Screenshot

![GUI](gui.png)

---

## Features

- Genetic Algorithm implementation
- Password evolution simulation
- GUI for running experiments
- Convergence visualization
- Multiple configuration testing:
  - Default
  - Large Population
  - High Mutation
  - Small Tournament Selection
- Performance comparison between GA parameters

---

## Genetic Algorithm Workflow

The algorithm follows these steps:

1. **Initialize population** with random chromosomes
2. **Evaluate fitness** by comparing with target password
3. **Selection** using tournament selection
4. **Crossover** to produce offspring
5. **Mutation** to introduce randomness
6. **Repeat** until the password is discovered

---

## Experiment Configurations

| Configuration | Population | Mutation Rate | Tournament Size |
|---------------|------------|--------------|----------------|
| Default | 100 | 0.01 | 5 |
| Large Pop | 300 | 0.01 | 5 |
| High Mutation | 100 | 0.05 | 5 |
| Small Tour | 100 | 0.01 | 3 |

---

## Technologies Used

- Python
- Genetic Algorithms
- GUI Framework (Tkinter / PyQt depending on implementation)
- Matplotlib (for convergence visualization)

---

## Project Structure
