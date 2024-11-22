import streamlit as st
from scipy.stats import poisson

# Title of the App
st.title("Football Match Outcome Predictor")

# Sidebar Input
st.sidebar.header("Input Team Data")

st.sidebar.subheader("Home Team")
avg_home_goals_scored = st.sidebar.number_input("Average Goals Scored (Home)", min_value=0.0, value=1.5, step=0.1)
avg_home_goals_conceded = st.sidebar.number_input("Average Goals Conceded (Home)", min_value=0.0, value=1.2, step=0.1)
avg_home_points = st.sidebar.number_input("Average Points (Home)", min_value=0.0, value=1.8, step=0.1)

st.sidebar.subheader("Away Team")
avg_away_goals_scored = st.sidebar.number_input("Average Goals Scored (Away)", min_value=0.0, value=1.2, step=0.1)
avg_away_goals_conceded = st.sidebar.number_input("Average Goals Conceded (Away)", min_value=0.0, value=1.3, step=0.1)
avg_away_points = st.sidebar.number_input("Average Points (Away)", min_value=0.0, value=1.4, step=0.1)

st.sidebar.subheader("League Averages")
league_avg_goals_scored = st.sidebar.number_input("League Average Goals Scored per Match", min_value=0.1, value=1.5, step=0.1)
league_avg_goals_conceded = st.sidebar.number_input("League Average Goals Conceded per Match", min_value=0.1, value=1.5, step=0.1)

# Calculate Attack and Defense Strengths
home_attack_strength = avg_home_goals_scored / league_avg_goals_scored
home_defense_strength = avg_home_goals_conceded / league_avg_goals_conceded

away_attack_strength = avg_away_goals_scored / league_avg_goals_scored
away_defense_strength = avg_away_goals_conceded / league_avg_goals_conceded

# Calculate Expected Goals
home_expected_goals = home_attack_strength * away_defense_strength * league_avg_goals_scored
away_expected_goals = away_attack_strength * home_defense_strength * league_avg_goals_scored

# Display Calculated Strengths and Expected Goals
st.subheader("Calculated Strengths")
st.write(f"**Home Attack Strength:** {home_attack_strength:.2f}")
st.write(f"**Home Defense Strength:** {home_defense_strength:.2f}")
st.write(f"**Away Attack Strength:** {away_attack_strength:.2f}")
st.write(f"**Away Defense Strength:** {away_defense_strength:.2f}")

st.subheader("Expected Goals")
st.write(f"**Home Team Expected Goals:** {home_expected_goals:.2f}")
st.write(f"**Away Team Expected Goals:** {away_expected_goals:.2f}")

# Function to Calculate Score Probabilities
def calculate_score_probabilities(home_goals, away_goals):
    home_probs = poisson.pmf(home_goals, home_expected_goals)
    away_probs = poisson.pmf(away_goals, away_expected_goals)
    return home_probs * away_probs

# Predict Probabilities for Scorelines
st.subheader("Scoreline Probabilities")
max_goals = st.slider("Max Goals to Display", min_value=3, max_value=10, value=5)
probabilities = {}

for home_goals in range(max_goals + 1):
    for away_goals in range(max_goals + 1):
        prob = calculate_score_probabilities(home_goals, away_goals)
        probabilities[(home_goals, away_goals)] = prob

# Display Probabilities as a Table
st.write("Probabilities for Each Scoreline:")
prob_table = {
    "Home Goals": [],
    "Away Goals": [],
    "Probability (%)": [],
}

for (home_goals, away_goals), prob in probabilities.items():
    prob_table["Home Goals"].append(home_goals)
    prob_table["Away Goals"].append(away_goals)
    prob_table["Probability (%)"].append(round(prob * 100, 2))

st.dataframe(prob_table)

# Recommend Most Likely Scoreline
most_likely_scoreline = max(probabilities, key=probabilities.get)
most_likely_prob = probabilities[most_likely_scoreline] * 100

st.subheader("Most Likely Outcome")
st.write(
    f"The most likely scoreline is **{most_likely_scoreline[0]}-{most_likely_scoreline[1]}** "
    f"with a probability of **{most_likely_prob:.2f}%**."
)
