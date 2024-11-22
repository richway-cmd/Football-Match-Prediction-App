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

# Mock function to calculate probabilities
def calculate_probabilities(selected_points):
    np.random.seed(42)  # For consistent random numbers
    data = {
        "Metric": selected_points,
        "Winning Percentage": [round(np.random.uniform(50, 100), 2) for _ in selected_points]
    }
    return pd.DataFrame(data)

# Generate predictions based on user selection
if selected_points:
    st.subheader("Prediction Results")
    predictions = calculate_probabilities(selected_points)
    st.table(predictions)

    # Summary of the results
    st.subheader("Summary")
    avg_percentage = predictions["Winning Percentage"].mean()
    st.write(f"The average winning percentage for the selected metrics is **{avg_percentage:.2f}%**.")
    
    st.write("**Key Insights:**")
    st.write("- Metrics with higher probabilities indicate stronger outcomes.")
    st.write("- Use these probabilities to make informed decisions.")

else:
    st.write("Please select points from the sidebar to see predictions.")
