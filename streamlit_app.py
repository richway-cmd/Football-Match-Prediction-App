import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import poisson
from sklearn.linear_model import LinearRegression

# Define odds and margin targets
odds_data = {
    "Home": 2.60,
    "Draw": 3.25,
    "Away": 2.80,
    "Over 2.5": 2.40,
    "Under 2.5": 1.55,
}
margin_targets = {
    "Match Results": 4.95,
    "Over/Under": 6.18,
    "Correct Score": 57.97,
    "HT/FT": 20.0,
    "Asian Handicap Margin Target": 5.90,
    "Over/Under Margin Target": 6.18,
    "Exact Goals Margin Target": 20.25,
    "Correct Score Margin": 57.97,
}

# Function to calculate margin differences
def calculate_margin_difference(odds, margin_target):
    return round(margin_target - odds, 2)

# Calculate margin differences and store in a DataFrame
margin_differences = {
    bet: calculate_margin_difference(odds, margin_targets["Match Results"] if "2.5" not in bet else margin_targets["Over/Under"])
    for bet, odds in odds_data.items()
}
margin_df = pd.DataFrame.from_dict(margin_differences, orient='index', columns=['Margin Difference'])

# Visualization of margin differences
def plot_margin_differences(df):
    plt.figure(figsize=(10, 6))
    df['Margin Difference'].plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title("Margin Differences by Bet Type", fontsize=16)
    plt.xlabel("Bet Type", fontsize=14)
    plt.ylabel("Margin Difference", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, fontsize=12)
    plt.tight_layout()
    plt.show()

# Function to calculate and plot Poisson probabilities
def calculate_poisson_distribution(goals_team1, goals_team2, max_goals=5):
    prob_matrix = np.zeros((max_goals + 1, max_goals + 1))
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            prob_matrix[i, j] = poisson.pmf(i, goals_team1) * poisson.pmf(j, goals_team2)
    prob_matrix /= prob_matrix.sum()  # Normalize

    # Plot probability matrix
    plt.figure(figsize=(10, 6))
    plt.imshow(prob_matrix, cmap="coolwarm", extent=[0, max_goals, 0, max_goals])
    plt.title(f"Poisson Probability Distribution\n(Goals Team 1: {goals_team1}, Team 2: {goals_team2})", fontsize=14)
    plt.colorbar(label="Probability")
    plt.xlabel("Goals Team 2", fontsize=12)
    plt.ylabel("Goals Team 1", fontsize=12)
    plt.xticks(range(max_goals + 1))
    plt.yticks(range(max_goals + 1))
    plt.show()

    return prob_matrix

# Feature Engineering and Prediction with Linear Regression
def predict_expected_goals(data):
    """
    Use historical data to predict goals.
    Example data format:
    data = {'Team 1 Attack': [1.5, ...], 'Team 2 Defense': [1.2, ...], 'Expected Goals': [1.6, ...]}
    """
    df = pd.DataFrame(data)
    X = df[['Team 1 Attack', 'Team 2 Defense']]
    y = df['Expected Goals']
    model = LinearRegression()
    model.fit(X, y)

    # Predict next match goals
    new_match = np.array([[1.5, 1.2]])
    predicted_goals = model.predict(new_match)
    return predicted_goals[0]

# Main function to integrate all components
def main():
    # Example data
    data = {
        "Team 1 Attack": [1.5, 1.3, 1.6],
        "Team 2 Defense": [1.2, 1.4, 1.1],
        "Expected Goals": [1.5, 1.4, 1.6],
    }
    predicted_goals = predict_expected_goals(data)
    print(f"Predicted Goals for Next Match: {predicted_goals:.2f}")
    
    # Calculate Poisson distribution
    prob_matrix = calculate_poisson_distribution(1.5, 1.2)

    # Display margin differences
    print("\nMargin Differences:")
    print(margin_df)

    # Plot margin differences
    plot_margin_differences(margin_df)

if __name__ == "__main__":
    main()
