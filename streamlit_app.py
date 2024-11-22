import streamlit as st
import pandas as pd

# Title of the app
st.title("Football Match Probability Prediction")

# Sidebar input
selected_points = st.sidebar.multiselect(
    "Select Points for Probabilities and Odds",
    options=[
        "HT/FT", "Correct Score", 
        "BTTS (Both Teams to Score)", "Exact Goals"
    ]
)

# Display selected points
st.subheader("Selected Points for Prediction")
st.write(selected_points)

# Mock probabilities for demonstration
ht_ft_probs = {
    "Half Time / Full Time": ["1/1", "1/X", "1/2", "X/1", "X/X", "X/2", "2/1", "2/X", "2/2"],
    "Probabilities (%)": [26.0, 4.8, 1.6, 16.4, 17.4, 11.2, 2.2, 4.8, 15.5]
}

correct_score_probs = {
    "Score": [
        "1:0", "2:0", "2:1", "3:0", "3:1", "3:2", "4:0", "4:1", "5:0", 
        "0:0", "1:1", "2:2", "3:3", "4:4", "5:5", "other",
        "0:1", "0:2", "1:2", "0:3", "1:3", "2:3", "0:4", "1:4", "0:5"
    ],
    "Probabilities (%)": [
        12.4, 8.5, 8.8, 3.9, 4.0, 2.1, 1.3, 1.4, 0.4, 
        9.0, 12.8, 4.6, 0.7, 0.1, 0.0, 2.9, 
        9.3, 4.8, 6.6, 1.7, 2.3, 1.6, 0.4, 0.6, 0.1
    ]
}

btts_probs = {
    "BTTS": ["Yes", "No"],
    "Probabilities (%)": [56.0, 44.0]
}

exact_goals_probs = {
    "Exact Goals": [0, 1, 2, 3, 4, 5],
    "Probabilities (%)": [11.3, 20.4, 26.7, 19.2, 12.0, 10.4]
}

# Display results
if selected_points:
    if "HT/FT" in selected_points:
        st.subheader("Half Time / Full Time Probabilities")
        ht_ft_df = pd.DataFrame(ht_ft_probs)
        st.table(ht_ft_df)

    if "Correct Score" in selected_points:
        st.subheader("Correct Score Probabilities")
        correct_score_df = pd.DataFrame(correct_score_probs)
        st.table(correct_score_df)

    if "BTTS (Both Teams to Score)" in selected_points:
        st.subheader("Both Teams to Score Probabilities")
        btts_df = pd.DataFrame(btts_probs)
        st.table(btts_df)

    if "Exact Goals" in selected_points:
        st.subheader("Exact Goals Probabilities")
        exact_goals_df = pd.DataFrame(exact_goals_probs)
        st.table(exact_goals_df)

    # Summary of predictions
    st.subheader("Summary")
    st.write("- Metrics with higher probabilities indicate stronger outcomes.")
    st.write("- Use these probabilities to make informed decisions.")
else:
    st.write("Please select points from the sidebar to see predictions.")
