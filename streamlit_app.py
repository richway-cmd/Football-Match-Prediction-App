import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import poisson
from sklearn.ensemble import RandomForestRegressor

# App Title and Description
st.title("🤖 Advanced Football Outcome Predictor")
st.markdown("""
This app predicts football match outcomes using advanced metrics:
- **Poisson Distribution**
- **Machine Learning**
- **Odds and Value Analysis**
- **Margin Calculations**
""")

# Sidebar for Match Input Details
st.sidebar.header("Match Details")
home_team = st.sidebar.text_input("Home Team", "Team A")
away_team = st.sidebar.text_input("Away Team", "Team B")
goals_home_mean = st.sidebar.number_input("Expected Goals (Home)", min_value=0.1, value=1.2, step=0.1)
goals_away_mean = st.sidebar.number_input("Expected Goals (Away)", min_value=0.1, value=1.1, step=0.1)
home_win_odds = st.sidebar.number_input("Odds: Home Win", value=2.50)
draw_odds = st.sidebar.number_input("Odds: Draw", value=3.20)
away_win_odds = st.sidebar.number_input("Odds: Away Win", value=3.10)
odds_data = {
    "Home Win": home_win_odds,
    "Draw": draw_odds,
    "Away Win": away_win_odds,
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

# Poisson Probability Function
def poisson_prob(mean, goal):
    return (np.exp(-mean) * mean**goal) / np.math.factorial(goal)

# Calculate Goal Probabilities
def calculate_probabilities(home_mean, away_mean, max_goals=5):
    home_probs = [poisson_prob(home_mean, g) for g in range(max_goals + 1)]
    away_probs = [poisson_prob(away_mean, g) for g in range(max_goals + 1)]
    score_probs = [
        (i, j, home_probs[i] * away_probs[j])
        for i in range(max_goals + 1)
        for j in range(max_goals + 1)
    ]
    return score_probs

# Odds Implied Probabilities
def odds_implied_probability(odds):
    return 1 / odds

# Normalize Odds
def normalize_probs(home, draw, away):
    total = home + draw + away
    return home / total, draw / total, away / total

# Calculate Probabilities
match_probs = calculate_probabilities(goals_home_mean, goals_away_mean)
score_probs_df = pd.DataFrame(match_probs, columns=["Home Goals", "Away Goals", "Probability"])

# Display Probabilities
st.subheader("Match Outcome Probabilities")
home_prob = odds_implied_probability(home_win_odds)
draw_prob = odds_implied_probability(draw_odds)
away_prob = odds_implied_probability(away_win_odds)
normalized_home, normalized_draw, normalized_away = normalize_probs(home_prob, draw_prob, away_prob)

st.metric("Home Win (%)", f"{normalized_home * 100:.2f}")
st.metric("Draw (%)", f"{normalized_draw * 100:.2f}")
st.metric("Away Win (%)", f"{normalized_away * 100:.2f}")

# Correct Score Predictions
st.subheader("Top Correct Score Predictions")
top_scores = score_probs_df.sort_values("Probability", ascending=False).head(5)
top_scores["Probability (%)"] = top_scores["Probability"] * 100
st.write(top_scores)

# Visualization of Correct Score Probabilities
fig, ax = plt.subplots()
ax.bar(
    top_scores.apply(lambda row: f"{int(row['Home Goals'])}-{int(row['Away Goals'])}", axis=1),
    top_scores["Probability (%)"],
    color="skyblue",
)
ax.set_title("Top Correct Scores")
ax.set_ylabel("Probability (%)")
st.pyplot(fig)

# Value Betting Analysis
st.subheader("Value Betting Analysis")
value_bets = {
    "Home Win": home_prob - normalized_home,
    "Draw": draw_prob - normalized_draw,
    "Away Win": away_prob - normalized_away,
}
st.write(f"Value (Home Win): {value_bets['Home Win']:.2f}")
st.write(f"Value (Draw): {value_bets['Draw']:.2f}")
st.write(f"Value (Away Win): {value_bets['Away Win']:.2f}")

# Display Margin Differences
st.subheader("Margin Differences for Various Bets")
st.write(margin_df)

# Advanced Visualization - Poisson Heatmap
st.subheader("Poisson Probability Heatmap")
def visualize_poisson_heatmap(home_mean, away_mean, max_goals=5):
    prob_matrix = np.zeros((max_goals + 1, max_goals + 1))
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            prob_matrix[i, j] = poisson.pmf(i, home_mean) * poisson.pmf(j, away_mean)
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
