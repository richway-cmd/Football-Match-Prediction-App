import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import poisson
from sklearn.ensemble import RandomForestRegressor

# Advanced Predictor Dashboard
st.title("Advanced Football Match Outcome Predictor")
st.markdown("Using Poisson Distribution, Machine Learning, Odds Analysis, and Advanced Metrics")

# Sidebar Inputs
st.sidebar.header("Match Details")
home_team = st.sidebar.text_input("Home Team", "Team A")
away_team = st.sidebar.text_input("Away Team", "Team B")
goals_home_mean = st.sidebar.number_input("Expected Goals (Home)", min_value=0.1, value=1.2, step=0.1)
goals_away_mean = st.sidebar.number_input("Expected Goals (Away)", min_value=0.1, value=1.1, step=0.1)
home_win_odds = st.sidebar.number_input("Odds: Home Win", value=2.50)
draw_odds = st.sidebar.number_input("Odds: Draw", value=3.20)
away_win_odds = st.sidebar.number_input("Odds: Away Win", value=3.10)

# Poisson Probability Function
def poisson_prob(mean, goal):
    return (np.exp(-mean) * mean**goal) / np.math.factorial(goal)

# Calculate Goal Probabilities
def calculate_probabilities(goals_home_mean, goals_away_mean, max_goals=5):
    home_probs = [poisson_prob(goals_home_mean, g) for g in range(max_goals + 1)]
    away_probs = [poisson_prob(goals_away_mean, g) for g in range(max_goals + 1)]
    score_probs = []
    for i, hp in enumerate(home_probs):
        for j, ap in enumerate(away_probs):
            prob = hp * ap
            score_probs.append((i, j, prob))
    return score_probs

# Calculate Odds Implied Probabilities
def odds_implied_probability(odds):
    return 1 / odds

# Normalize Odds
def normalize_probs(home, draw, away):
    total = home + draw + away
    return home / total, draw / total, away / total

# Machine Learning Predictor
def train_ml_model(data):
    df = pd.DataFrame(data)
    X = df[['Team 1 Attack', 'Team 2 Defense']]
    y = df['Expected Goals']
    model = RandomForestRegressor()
    model.fit(X, y)
    return model

def predict_expected_goals(model, team1_attack, team2_defense):
    return model.predict([[team1_attack, team2_defense]])[0]

# Real-Time Odds and Value Calculation
def calculate_value(home_prob, draw_prob, away_prob, normalized_home, normalized_draw, normalized_away):
    return {
        "Home Win": home_prob - normalized_home,
        "Draw": draw_prob - normalized_draw,
        "Away Win": away_prob - normalized_away,
    }

# Match Probabilities
match_probs = calculate_probabilities(goals_home_mean, goals_away_mean)

# Calculate Implied and Normalized Probabilities
home_prob = odds_implied_probability(home_win_odds)
draw_prob = odds_implied_probability(draw_odds)
away_prob = odds_implied_probability(away_win_odds)
normalized_home, normalized_draw, normalized_away = normalize_probs(home_prob, draw_prob, away_prob)

# Display Match Outcome Probabilities
st.subheader("Match Outcome Probabilities")
st.metric("Home Win (%)", f"{normalized_home * 100:.2f}")
st.metric("Draw (%)", f"{normalized_draw * 100:.2f}")
st.metric("Away Win (%)", f"{normalized_away * 100:.2f}")

# Display Correct Score Probabilities
st.subheader("Correct Score Probabilities")
score_probs = pd.DataFrame(match_probs, columns=["Home Goals", "Away Goals", "Probability"])
st.write(score_probs.sort_values("Probability", ascending=False).head(10))

# Visualize Probabilities
fig, ax = plt.subplots()
top_scores = score_probs.sort_values("Probability", ascending=False).head(5)
ax.bar(top_scores.apply(lambda x: f"{int(x[0])}-{int(x[1])}", axis=1), top_scores["Probability"], color="skyblue")
ax.set_title("Top Correct Scores")
ax.set_ylabel("Probability")
st.pyplot(fig)

# Value Betting Analysis
st.subheader("Value Betting Analysis")
value_bets = calculate_value(home_prob, draw_prob, away_prob, normalized_home, normalized_draw, normalized_away)
st.write(f"Value (Home Win): {value_bets['Home Win']:.2f}")
st.write(f"Value (Draw): {value_bets['Draw']:.2f}")
st.write(f"Value (Away Win): {value_bets['Away Win']:.2f}")

# Machine Learning Integration Example
st.subheader("Machine Learning Prediction")
example_data = {
    "Team 1 Attack": [1.5, 1.3, 1.6],
    "Team 2 Defense": [1.2, 1.4, 1.1],
    "Expected Goals": [1.5, 1.4, 1.6],
}
ml_model = train_ml_model(example_data)
predicted_goals = predict_expected_goals(ml_model, 1.5, 1.2)
st.write(f"Predicted Goals for {home_team} vs {away_team}: {predicted_goals:.2f}")

# Advanced Visualization
st.subheader("Poisson Probability Heatmap")
def visualize_poisson_heatmap(goals_home_mean, goals_away_mean, max_goals=5):
    prob_matrix = np.zeros((max_goals + 1, max_goals + 1))
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            prob_matrix[i, j] = poisson.pmf(i, goals_home_mean) * poisson.pmf(j, goals_away_mean)
    prob_matrix /= prob_matrix.sum()

    fig, ax = plt.subplots(figsize=(8, 6))
    cax = ax.matshow(prob_matrix, cmap="coolwarm")
    fig.colorbar(cax)
    ax.set_xticks(range(max_goals + 1))
    ax.set_yticks(range(max_goals + 1))
    ax.set_xticklabels(range(max_goals + 1))
    ax.set_yticklabels(range(max_goals + 1))
    ax.set_xlabel("Goals Away Team", fontsize=12)
    ax.set_ylabel("Goals Home Team", fontsize=12)
    ax.set_title("Poisson Probability Heatmap", fontsize=14)
    st.pyplot(fig)

visualize_poisson_heatmap(goals_home_mean, goals_away_mean)
