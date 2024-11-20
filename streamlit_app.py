import numpy as np
from math import factorial  # Correct import for factorial
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import poisson
import streamlit as st

# Streamlit Application Title
st.title("🤖 Advanced Rabiotic Football Outcome Predictor")
st.markdown("""
Predict football match outcomes using advanced metrics like:
- **Poisson Distribution**
- **Machine Learning**
- **Odds Analysis**
- **Margin Calculations**
""")

# Sidebar for Input Parameters
st.sidebar.header("Input Parameters")

# Match and Odds Input
home_team = st.sidebar.text_input("Home Team", "Team A")
away_team = st.sidebar.text_input("Away Team", "Team B")
goals_home_mean = st.sidebar.number_input("Expected Goals (Home)", min_value=0.1, value=1.2, step=0.1)
goals_away_mean = st.sidebar.number_input("Expected Goals (Away)", min_value=0.1, value=1.1, step=0.1)

# Odds Input
home_win_odds = st.sidebar.number_input("Odds: Home Win", value=2.50, step=0.01)
draw_odds = st.sidebar.number_input("Odds: Draw", value=3.20, step=0.01)
away_win_odds = st.sidebar.number_input("Odds: Away Win", value=3.10, step=0.01)
over_odds = st.sidebar.number_input("Over 2.5 Odds", value=2.40, step=0.01)
under_odds = st.sidebar.number_input("Under 2.5 Odds", value=1.55, step=0.01)

# Margin Targets
st.sidebar.subheader("Margin Targets")
margin_targets = {
    "Match Results": st.sidebar.number_input("Match Results Margin", value=4.95, step=0.01),
    "Asian Handicap": st.sidebar.number_input("Asian Handicap Margin", value=5.90, step=0.01),
    "Over/Under": st.sidebar.number_input("Over/Under Margin", value=6.18, step=0.01),"Exact goals": st.sidebar.number_input("Exaxt goals Margin", value=20.0, step=0.01),
    "Correct Score": st.sidebar.number_input("Correct Score Margin", value=57.97, step=0.01),
    "Exact goals": st.sidebar.number_input("Exaxt goals Margin", value=20.0, step=0.01),
    "HT/FT": st.sidebar.number_input("HT/FT Margin", value=20.0, step=0.01),
}

# Select Points for Probabilities and Odds
selected_points = st.sidebar.multiselect(
    "Select Points for Probabilities and Odds",
    options=["Home Win", "Draw", "Away Win", "Over 2.5", "Under 2.5", "Correct Score", "HT/FT", "BTTS", "Exact Goals"]
)

# Submit Button
submit_button = st.sidebar.button("Submit Prediction")

# Functions
def calculate_margin_difference(odds, margin_target):
    return round(margin_target - odds, 2)

def poisson_prob(mean, goal):
    return (np.exp(-mean) * mean**goal) / factorial(goal)  # Using `factorial` from `math`

def calculate_probabilities(home_mean, away_mean, max_goals=5):
    home_probs = [poisson_prob(home_mean, g) for g in range(max_goals + 1)]
    away_probs = [poisson_prob(away_mean, g) for g in range(max_goals + 1)]
    return [
        (i, j, home_probs[i] * away_probs[j])
        for i in range(max_goals + 1)
        for j in range(max_goals + 1)
    ]

def odds_implied_probability(odds):
    return 1 / odds

def normalize_probs(home, draw, away):
    total = home + draw + away
    return home / total, draw / total, away / total

# Run prediction when submit button is pressed
if submit_button:
    # Calculate Probabilities
    match_probs = calculate_probabilities(goals_home_mean, goals_away_mean)
    score_probs_df = pd.DataFrame(match_probs, columns=["Home Goals", "Away Goals", "Probability"])

    # Display Probabilities
    st.subheader("Match Outcome Probabilities")
    home_prob = odds_implied_probability(home_win_odds)
    draw_prob = odds_implied_probability(draw_odds)
    away_prob = odds_implied_probability(away_win_odds)
    normalized_home, normalized_draw, normalized_away = normalize_probs(home_prob, draw_prob, away_prob)

    if "Home Win" in selected_points:
        st.metric("Home Win (%)", f"{normalized_home * 100:.2f}")
    if "Draw" in selected_points:
        st.metric("Draw (%)", f"{normalized_draw * 100:.2f}")
    if "Away Win" in selected_points:
        st.metric("Away Win (%)", f"{normalized_away * 100:.2f}")

    # Correct Score Predictions
    if "Correct Score" in selected_points:
        st.subheader("Top Correct Score Predictions")
        top_scores = score_probs_df.sort_values("Probability", ascending=False).head(5)
        top_scores["Probability (%)"] = top_scores["Probability"] * 100
        st.write(top_scores)

        # Visualization: Correct Score Probabilities
        fig, ax = plt.subplots()
        ax.bar(
            top_scores.apply(lambda row: f"{int(row['Home Goals'])}-{int(row['Away Goals'])}", axis=1),
            top_scores["Probability (%)"],
            color="skyblue",
        )
        ax.set_title("Top Correct Scores")
        ax.set_ylabel("Probability (%)")
        st.pyplot(fig)

    # Margin Differences
    st.subheader("Margin Differences")
    margin_differences = {
        "Home Win": calculate_margin_difference(home_win_odds, margin_targets["Match Results"]),
        "Draw": calculate_margin_difference(draw_odds, margin_targets["Match Results"]),
        "Away Win": calculate_margin_difference(away_win_odds, margin_targets["Match Results"]),
        "Over 2.5": calculate_margin_difference(over_odds, margin_targets["Over/Under"]),
        "Under 2.5": calculate_margin_difference(under_odds, margin_targets["Over/Under"]),
    }
    margin_df = pd.DataFrame.from_dict(margin_differences, orient='index', columns=['Margin Difference'])
    st.write(margin_df)

    # Advanced Visualization: Poisson Heatmap
    st.subheader("Poisson Probability Heatmap")
    prob_matrix = np.zeros((5 + 1, 5 + 1))
    for i in range(5 + 1):
        for j in range(5 + 1):
            prob_matrix[i, j] = poisson.pmf(i, goals_home_mean) * poisson.pmf(j, goals_away_mean)
    prob_matrix /= prob_matrix.sum()

    fig, ax = plt.subplots(figsize=(8, 6))
    cax = ax.matshow(prob_matrix, cmap="coolwarm")
    fig.colorbar(cax)
    ax.set_xticks(range(5 + 1))
    ax.set_yticks(range(5 + 1))
    ax.set_xticklabels(range(5 + 1))
    ax.set_yticklabels(range(5 + 1))
    ax.set_xlabel("Away Goals")
    ax.set_ylabel("Home Goals")
    st.pyplot(fig)
