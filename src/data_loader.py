"""
CricketIQ — Data Loader
========================
Handles loading and normalizing IPL match and delivery datasets.
"""

import streamlit as st
import pandas as pd
from src.config import MATCHES_CSV, DELIVERIES_CSV, TEAM_MAPPING


@st.cache_data
def load_data():
    """
    Load and normalize IPL datasets.
    
    Returns:
        tuple: (matches_df, deliveries_df, success_bool)
    """
    try:
        matches = pd.read_csv(MATCHES_CSV)
        deliveries = pd.read_csv(DELIVERIES_CSV)

        # Normalize team names to modern equivalents
        for col in ["team1", "team2", "winner"]:
            matches[col] = matches[col].replace(TEAM_MAPPING)
        for col in ["batting_team", "bowling_team"]:
            deliveries[col] = deliveries[col].replace(TEAM_MAPPING)

        return matches, deliveries, True
    except Exception:
        return None, None, False
