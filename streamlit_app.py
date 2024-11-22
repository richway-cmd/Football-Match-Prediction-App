import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import poisson

# Sidebar inputs
st.sidebar.header("Match Parameters")
team1_attack = st.sidebar.number_input("Team 1 Attack (Home Avg)", min_value=0.0, value=1.5, step=0.1)
team1_defense = st.sidebar.number_input("Team 1 Defense (Home Avg)", min_value=0.0, value=1.0, step=0.1)
team2_attack = st.sidebar.number_input("Team 2 Attack (Away Avg)", min_value=0.0, value=1.2, step=0.1)
team2_defense = st.sidebar.number_input("Team 2 Defense (Away Avg)", min_value=0.0, value=1.1, step=0.1)

margin = st.sidebar.slider("Margin %", 0, 100, 10)
max_goals = st.sidebar.number_input("Max Goals to Display", min_value=1, value=5, step=1)

# Calculate team goal expectations
team1_goals = (team1_attack + team2_defense) / 2
team2_goals = (team2_attack + team1_defense) / 2

# Main app layout
st.title("Odds and Probabilities Calculator")
st.subheader("Team Goal Expectations")
st.write(f"Expected Goals for Team 1: {team1_goals:.2f}")
st.write(f"Expected Goals for Team 2: {team2_goals:.2f}")

# Correct Score Probabilities
st.header("Correct Score Probabilities")
scores_matrix = np.zeros((max_goals + 1, max_goals + 1))
odds_matrix = np.zeros((max_goals + 1, max_goals + 1))
for i in range(max_goals + 1):
    for j in range(max_goals + 1):
        prob = poisson.pmf(i, team1_goals) * poisson.pmf(j, team2_goals)
        scores_matrix[i, j] = prob
        odds_matrix[i, j] = (1 / prob) * (1 + margin / 100) if prob > 0 else 0

# Display probability table
st.subheader("Probability Table (Raw)")
prob_df = pd.DataFrame(
    scores_matrix,
    columns=[f"Team 2 {j} Goals" for j in range(max_goals + 1)],
    index=[f"Team 1 {i} Goals" for i in range(max_goals + 1)],
)
st.table(prob_df)

# Display odds table
st.subheader("Odds Table (With Margin)")
odds_df = pd.DataFrame(
    odds_matrix,
    columns=[f"Team 2 {j} Goals" for j in range(max_goals + 1)],
    index=[f"Team 1 {i} Goals" for i in range(max_goals + 1)],
)
st.table(odds_df)

# Over/Under Totals
st.header("Over/Under Totals")
total_goals_prob = [
    sum(
        poisson.pmf(i, team1_goals) * poisson.pmf(j, team2_goals)
        for i in range(max_goals + 1)
        for j in range(max_goals + 1)
        if i + j == k
    )
    for k in range(2 * max_goals + 1)
]
total_goals_df = pd.DataFrame({
    "Total Goals": list(range(2 * max_goals + 1)),
    "Probability": total_goals_prob,
})
st.bar_chart(data=total_goals_df.set_index("Total Goals"), width=700, height=400)

st.subheader("Cumulative Probability")
cumulative_prob = np.cumsum(total_goals_prob)
total_goals_df["Cumulative Probability"] = cumulative_prob
st.line_chart(data=total_goals_df.set_index("Total Goals")[["Cumulative Probability"]])

st.write("Explore different match outcomes using the inputs in the sidebar.")
