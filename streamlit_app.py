import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from scipy.stats import poisson
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Application Title and Description
st.set_page_config(page_title="Advanced Football Predictor", layout="wide")
st.title("⚽ Advanced Football Match Predictor")
st.markdown("""
Predict football outcomes using **advanced metrics**:
- Poisson Distribution
- Machine Learning
- Bayesian Updating
- Advanced Visualizations
""")

# Sidebar for Inputs
st.sidebar.header("Input Parameters")
home_team = st.sidebar.text_input("Home Team", "Team A")
away_team = st.sidebar.text_input("Away Team", "Team B")
goals_home_mean = st.sidebar.number_input("Expected Goals (Home)", min_value=0.1, value=1.2, step=0.1)
goals_away_mean = st.sidebar.number_input("Expected Goals (Away)", min_value=0.1, value=1.1, step=0.1)
max_goals = st.sidebar.slider("Max Goals to Calculate", min_value=3, max_value=10, value=5)

# Odds Inputs
home_odds = st.sidebar.number_input("Odds: Home Win", value=2.50, step=0.01)
draw_odds = st.sidebar.number_input("Odds: Draw", value=3.20, step=0.01)
away_odds = st.sidebar.number_input("Odds: Away Win", value=3.10, step=0.01)

# Submit Button
if st.sidebar.button("Predict Outcomes"):
    # Poisson Probabilities
    def poisson_prob(mean, goal):
        return (np.exp(-mean) * mean**goal) / np.math.factorial(goal)
    
    # Match Probabilities
    def calculate_match_probabilities(home_mean, away_mean, max_goals):
        home_probs = [poisson_prob(home_mean, g) for g in range(max_goals + 1)]
        away_probs = [poisson_prob(away_mean, g) for g in range(max_goals + 1)]
        match_probs = pd.DataFrame([
            {"Home Goals": h, "Away Goals": a, "Probability": home_probs[h] * away_probs[a]}
            for h in range(max_goals + 1) for a in range(max_goals + 1)
        ])
        return match_probs

    match_probs = calculate_match_probabilities(goals_home_mean, goals_away_mean, max_goals)
    
    # Display Match Probabilities as Heatmap
    st.subheader("Probability Heatmap")
    heatmap = alt.Chart(match_probs).mark_rect().encode(
        x=alt.X('Away Goals:O', title='Away Team Goals'),
        y=alt.Y('Home Goals:O', title='Home Team Goals'),
        color=alt.Color('Probability:Q', scale=alt.Scale(scheme='blues'), title='Probability'),
        tooltip=['Home Goals', 'Away Goals', 'Probability']
    ).properties(
        width=600,
        height=400,
        title="Goal Probabilities Heatmap"
    )
    st.altair_chart(heatmap)

    # Correct Score Predictions
    st.subheader("Top Correct Score Predictions")
    top_scores = match_probs.sort_values("Probability", ascending=False).head(5)
    top_scores['Probability (%)'] = (top_scores['Probability'] * 100).round(2)
    st.table(top_scores)

    # Implied Probabilities
    def implied_probability(odds):
        return 1 / odds
    
    st.subheader("Implied Probabilities")
    home_prob = implied_probability(home_odds)
    draw_prob = implied_probability(draw_odds)
    away_prob = implied_probability(away_odds)
    normalized_probs = {
        "Home Win (%)": (home_prob / (home_prob + draw_prob + away_prob)) * 100,
        "Draw (%)": (draw_prob / (home_prob + draw_prob + away_prob)) * 100,
        "Away Win (%)": (away_prob / (home_prob + draw_prob + away_prob)) * 100,
    }
    st.metric("Home Win (%)", f"{normalized_probs['Home Win (%)']:.2f}")
    st.metric("Draw (%)", f"{normalized_probs['Draw (%)']:.2f}")
    st.metric("Away Win (%)", f"{normalized_probs['Away Win (%)']:.2f}")

    # Bayesian Updating (Advanced)
    st.subheader("Bayesian Predictions")
    prior_home = 0.4  # Example prior for home win
    prior_draw = 0.3  # Example prior for draw
    prior_away = 0.3  # Example prior for away win
    likelihood_home = normalized_probs['Home Win (%)'] / 100
    likelihood_draw = normalized_probs['Draw (%)'] / 100
    likelihood_away = normalized_probs['Away Win (%)'] / 100
    posterior_home = prior_home * likelihood_home
    posterior_draw = prior_draw * likelihood_draw
    posterior_away = prior_away * likelihood_away
    total_posterior = posterior_home + posterior_draw + posterior_away
    st.metric("Posterior Home Win (%)", f"{(posterior_home / total_posterior) * 100:.2f}")
    st.metric("Posterior Draw (%)", f"{(posterior_draw / total_posterior) * 100:.2f}")
    st.metric("Posterior Away Win (%)", f"{(posterior_away / total_posterior) * 100:.2f}")

    # Export Data
    st.download_button(
        label="Download Predictions as CSV",
        data=match_probs.to_csv(index=False),
        file_name="match_predictions.csv",
        mime="text/csv"
    )
