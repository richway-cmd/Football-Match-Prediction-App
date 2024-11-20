import streamlit as st
import numpy as np
import math
import pandas as pd

# Helper function to calculate Poisson probabilities
def poisson_prob(mean, goal):
    try:
        return (np.exp(-mean) * mean**goal) / math.factorial(goal)
    except Exception as e:
        st.error(f"Error calculating Poisson probability: {e}")
        return 0

# Function to calculate probabilities for both teams
def calculate_probabilities(home_mean, away_mean, max_goals=5):
    home_probs = [poisson_prob(home_mean, g) for g in range(max_goals + 1)]
    away_probs = [poisson_prob(away_mean, g) for g in range(max_goals + 1)]
    return home_probs, away_probs

# Function to calculate match outcome probabilities
def calculate_match_probabilities(home_probs, away_probs):
    probabilities = []
    for h, hp in enumerate(home_probs):
        for a, ap in enumerate(away_probs):
            probabilities.append((h, a, hp * ap))
    return probabilities

# Streamlit app starts here
st.title("Football Match Prediction App")
st.markdown("This app predicts football match outcomes using the Poisson distribution.")

# Input fields
st.sidebar.header("Enter Team Statistics")
home_mean = st.sidebar.number_input("Home Team Average Goals", min_value=0.0, step=0.1, value=1.5)
away_mean = st.sidebar.number_input("Away Team Average Goals", min_value=0.0, step=0.1, value=1.2)
max_goals = st.sidebar.slider("Max Goals to Calculate", min_value=3, max_value=10, value=5)

# Button to calculate
if st.sidebar.button("Calculate Probabilities"):
    # Calculate probabilities
    home_probs, away_probs = calculate_probabilities(home_mean, away_mean, max_goals)
    match_probs = calculate_match_probabilities(home_probs, away_probs)

    # Display probabilities as a heatmap
    st.header("Probability Heatmap")
    heatmap_data = pd.DataFrame(
        [[p[2] for p in match_probs if p[0] == h] for h in range(max_goals + 1)],
        index=[f"Home {i}" for i in range(max_goals + 1)],
        columns=[f"Away {i}" for i in range(max_goals + 1)],
    )
    st.dataframe(heatmap_data.style.background_gradient(cmap="Blues"))

    # Display match probabilities in a table
    st.header("Predicted Match Probabilities")
    st.write(pd.DataFrame(match_probs, columns=["Home Goals", "Away Goals", "Probability"]))
