import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson

# App Title
st.title("🤖 Rabiotic Correct Score Prediction App")
st.subheader("Predict Football Match Outcomes with Accuracy")

# Sidebar for Inputs
st.sidebar.header("Match Details")
team_a = st.sidebar.text_input("Enter Team A Name", "Team A")
team_b = st.sidebar.text_input("Enter Team B Name", "Team B")
team_a_goals = st.sidebar.number_input(f"Average Goals Scored by {team_a}", min_value=0.0, step=0.1, value=1.2)
team_b_goals = st.sidebar.number_input(f"Average Goals Scored by {team_b}", min_value=0.0, step=0.1, value=1.5)
team_a_concede = st.sidebar.number_input(f"Average Goals Conceded by {team_a}", min_value=0.0, step=0.1, value=1.3)
team_b_concede = st.sidebar.number_input(f"Average Goals Conceded by {team_b}", min_value=0.0, step=0.1, value=1.4)

# Poisson Function to Predict Scores
def predict_score(avg_home, avg_away, max_goals=5):
    home_goals = np.arange(0, max_goals + 1)
    away_goals = np.arange(0, max_goals + 1)
    probabilities = np.zeros((len(home_goals), len(away_goals)))

    for i, h in enumerate(home_goals):
        for j, a in enumerate(away_goals):
            probabilities[i, j] = poisson.pmf(h, avg_home) * poisson.pmf(a, avg_away)

    return pd.DataFrame(probabilities, index=home_goals, columns=away_goals)

# Calculate Prediction
st.markdown(f"### Predicted Outcomes for {team_a} vs {team_b}")
avg_home = (team_a_goals + team_b_concede) / 2
avg_away = (team_b_goals + team_a_concede) / 2
score_matrix = predict_score(avg_home, avg_away)

# Display Prediction
st.write("Probability Matrix:")
st.dataframe(score_matrix.style.format("{:.2%}"))

# Highlight Most Likely Scores
st.markdown("### Most Likely Scores")
most_likely = score_matrix.unstack().sort_values(ascending=False).head(5)
for (home, away), prob in most_likely.items():
    st.write(f"{home}-{away}: {prob:.2%}")
