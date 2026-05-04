"""
CricketIQ — Main Application Entry Point
==========================================
Slim orchestrator that wires together all modules.
Run with: streamlit run src/app.py
"""

import sys
from pathlib import Path

# Ensure project root is on the Python path for module imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CricketIQ",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Inject Global CSS ────────────────────────────────────────────────────────
from src.styles import GLOBAL_CSS
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── Load Data ────────────────────────────────────────────────────────────────
from src.data_loader import load_data
matches, deliveries, data_ok = load_data()

# ── Render Header ────────────────────────────────────────────────────────────
from src.ui.header import render_hero, render_metrics, render_footer

render_hero()
if data_ok:
    render_metrics(matches, deliveries)

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🤖  AI Chat",
    "🔮  Smart Match Insights",
    "🏏  Player Stats",
    "🏆  Leaderboards"
])

# ── Tab 1: AI Chat ───────────────────────────────────────────────────────────
with tab1:
    from src.ui.chat_tab import render_chat_tab
    render_chat_tab(matches, deliveries, data_ok)

# ── Tab 2: Match Predictions ─────────────────────────────────────────────────
with tab2:
    if not data_ok:
        st.error("Load matches.csv to use this feature.")
    else:
        from src.ui.prediction_tab import render_prediction_tab
        render_prediction_tab(matches)

# ── Tab 3: Player Stats ─────────────────────────────────────────────────────
with tab3:
    if not data_ok:
        st.error("Load deliveries.csv to use this feature.")
    else:
        from src.ui.player_tab import render_player_tab
        render_player_tab(deliveries)

# ── Tab 4: Leaderboards ─────────────────────────────────────────────────────
with tab4:
    if not data_ok:
        st.error("Load CSV files to use this feature.")
    else:
        from src.ui.leaderboard_tab import render_leaderboard_tab
        render_leaderboard_tab(matches, deliveries)

# ── Footer ───────────────────────────────────────────────────────────────────
render_footer()
