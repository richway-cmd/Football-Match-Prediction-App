import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import poisson

# Sidebar inputs
st.sidebar.header("Input Parameters")
team1_attack = st.sidebar.number_input("Team 1 Attack Strength (Home Avg)", min_value=0.0, value=1.5, step=0.1)
team1_defense = st.sidebar.number_input("Team 1 Defense Strength (Home Avg)", min_value=0.0, value=1.0, step=0.1)
team2_attack = st.sidebar.number_input("Team 2 Attack Strength (Away Avg)", min_value=0.0, value=1.2, step=0.1)
team2_defense = st.sidebar.number_input("Team 2 Defense Strength (Away Avg)", min_value=0.0, value=1.1, step=0.1)
margin = st.sidebar.slider("Margin % (Odds Adjustment)", 0, 100, 10)  # Margin adjustment as input

# Calculate team goal expectations
team1_goals = (team1_attack + team2_defense) / 2
team2_goals = (team2_attack + team1_defense) / 2

# Header
st.title("Football Match Odds & Probabilities Calculator")
st.subheader("Match Parameters and Goal Expectations")
st.write(f"Team 1 Expected Goals: **{team1_goals:.2f}**")
st.write(f"Team 2 Expected Goals: **{team2_goals:.2f}**")

# Correct Score Probabilities
st.header("Correct Score Odds and Probabilities")

max_goals = st.number_input("Max Goals to Display", min_value=1, value=5, step=1)
scores_matrix = np.zeros((max_goals + 1, max_goals + 1))

# Populate scores matrix with probabilities
for i in range(max_goals + 1):
    for j in range(max_goals + 1):
        scores_matrix[i, j] = poisson.pmf(i, team1_goals) * poisson.pmf(j, team2_goals)

# Display probabilities as a table
score_labels = [f"{i}:{j}" for i in range(max_goals + 1) for j in range(max_goals + 1)]
score_probs = [scores_matrix[i, j] for i in range(max_goals + 1) for j in range(max_goals + 1)]

# Create a DataFrame for better visualization
scores_df = pd.DataFrame({
    "Score": score_labels,
    "Probability": score_probs
}).sort_values(by="Probability", ascending=False).reset_index(drop=True)

st.subheader("Top Score Probabilities")
st.table(scores_df.head(10))

# Correct Score Odds
st.subheader("Correct Score Odds")
scores_df["Odds"] = (1 / scores_df["Probability"]) * (1 + margin / 100)  # Adjust odds based on margin
st.table(scores_df.head(10)[["Score", "Odds"]])

# Over/Under Total Goals
st.header("Over/Under Totals")
total_goals = np.arange(0, 2 * max_goals + 1)
over_under_probs = [np.sum(
    [poisson.pmf(i, team1_goals) * poisson.pmf(j, team2_goals) for i in range(k + 1) for j in range(k + 1)]
) for k in total_goals]

# Visualize cumulative probabilities for total goals
st.line_chart(pd.DataFrame({
    "Total Goals": total_goals,
    "Cumulative Probability": over_under_probs
}).set_index("Total Goals"), use_container_width=True)

# Summary
st.header("Summary")
st.write("This app provides dynamic calculations for match probabilities, correct score odds, and over/under totals based on team attack and defense strengths. Adjust the inputs and explore the results!")
