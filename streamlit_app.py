import numpy as np
from math import factorial  # Import factorial from the math module

# Function to calculate Poisson probability
def poisson_prob(mean, goal):
    return (np.exp(-mean) * mean**goal) / factorial(goal)

# Function to calculate match probabilities
def calculate_probabilities(goals_home_mean, goals_away_mean, max_goals=5):
    home_probs = [poisson_prob(goals_home_mean, g) for g in range(max_goals + 1)]
    away_probs = [poisson_prob(goals_away_mean, g) for g in range(max_goals + 1)]

    match_probs = np.zeros((max_goals + 1, max_goals + 1))
    for i, home_prob in enumerate(home_probs):
        for j, away_prob in enumerate(away_probs):
            match_probs[i, j] = home_prob * away_prob

    return match_probs

# Example inputs
goals_home_mean = 1.5
goals_away_mean = 1.2

# Calculate match probabilities
match_probs = calculate_probabilities(goals_home_mean, goals_away_mean)

# Print match probabilities
print("Match probabilities matrix:")
print(match_probs)
