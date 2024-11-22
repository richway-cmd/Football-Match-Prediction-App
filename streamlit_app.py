import streamlit as st
import pandas as pd
import numpy as np

# Title of the app
st.title("Football Match Probability Prediction")

# Sidebar input
selected_points = st.sidebar.multiselect(
    "Select Points for Probabilities and Odds",
    options=[
        "Home Win", "Draw", "Away Win",
        "Over 2.5", "Under 2.5",
        "Correct Score", "HT/FT",
        "BTTS", "Exact Goals"
    ]
)

# Display selected points
st.subheader("Selected Points for Prediction")
st.write(selected_points)

# Mock functions to calculate probabilities
def calculate_ht_ft_probabilities():
    np.random.seed(42)  # For consistent random numbers
    data = {
        "Half Time / Full Time": ["1/1", "1/X", "1/2", "X/1", "X/X", "X/2", "2/1", "2/X", "2/2"],
        "Probabilities (%)": [26.0, 4.8, 1.6, 16.4, 17.4, 11.2, 2.2, 4.8, 15.5]
    }
    return pd.DataFrame(data)

def calculate_correct_score_probabilities():
    np.random.seed(42)
    data = {
        "Score": [
            "1:0", "2:0", "2:1", "3:0", "3:1", "3:2", "4:0", "4:1", "5:0",
            "0:0", "1:1", "2:2", "3:3", "4:4", "5:5", "Other",
            "0:1", "0:2", "1:2", "0:3", "1:3", "2:3", "0:4", "1:4", "0:5"
        ],
        "Probabilities (%)": [
            12.4, 8.5, 8.8, 3.9, 4.0, 2.1, 1.3, 1.4, 0.4,
            9.0, 12.8, 4.6, 0.7, 0.1, None, 2.9,
            9.3, 4.8, 6.6, 1.7, 2.3, 1.6, 0.4, 0.6, 0.1
        ]
    }
    return pd.DataFrame(data)

def calculate_btts_probabilities():
    return pd.DataFrame({
        "BTTS (Yes/No)": ["Yes", "No"],
        "Probabilities (%)": [53.0, 47.0]
    })

def calculate_exact_goals_probabilities():
    return pd.DataFrame({
        "Exact Goals": [0, 1, 2, 3, 4, 5],
        "Probabilities (%)": [8.0, 22.0, 35.0, 20.0, 10.0, 5.0]
    })

# Generate predictions based on user selection
if selected_points:
    st.subheader("Prediction Results")

    if "HT/FT" in selected_points:
        st.write("### Half Time / Full Time - Probabilities (%)")
        ht_ft_probs = calculate_ht_ft_probabilities()
        st.table(ht_ft_probs)

    if "Correct Score" in selected_points:
        st.write("### Correct Score - Probabilities (%)")
        correct_score_probs = calculate_correct_score_probabilities()
        st.table(correct_score_probs)

    if "BTTS" in selected_points:
        st.write("### Both Teams to Score (Yes/No) - Probabilities (%)")
        btts_probs = calculate_btts_probabilities()
        st.table(btts_probs)

    if "Exact Goals" in selected_points:
        st.write("### Exact Goals - Probabilities (%)")
        exact_goals_probs = calculate_exact_goals_probabilities()
        st.table(exact_goals_probs)

    # Summary of the results
    st.subheader("Summary")
    st.write("- Metrics with higher probabilities indicate stronger outcomes.")
    st.write("- Use these probabilities to make informed decisions.")
else:
    st.write("Please select points from the sidebar to see predictions.")
