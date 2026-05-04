"""
CricketIQ — Header UI
=======================
Hero header and top-level metric cards.
"""

import streamlit as st
from src.config import ACTIVE_TEAMS


def render_hero():
    """Render the CricketIQ hero header with gradient title."""
    st.markdown("""
    <div class="ciq-hero">
        <h1>CricketIQ</h1>
        <div class="tagline">AI-Powered IPL Intelligence Engine (2008 - 2020)</div>
    </div>
    """, unsafe_allow_html=True)


def render_metrics(matches, deliveries):
    """Render the top-level dashboard metric cards."""
    col_h1, col_h2, col_h3, col_h4, col_h5 = st.columns(5)

    with col_h1:
        st.markdown('<div class="metric-blue">', unsafe_allow_html=True)
        st.metric("🏏 Matches", len(matches))
        st.markdown('</div>', unsafe_allow_html=True)
    with col_h2:
        st.markdown('<div class="metric-purple">', unsafe_allow_html=True)
        st.metric("👤 Players", deliveries["batsman"].nunique())
        st.markdown('</div>', unsafe_allow_html=True)
    with col_h3:
        st.markdown('<div class="metric-orange">', unsafe_allow_html=True)
        st.metric("📅 Seasons", matches["season"].nunique())
        st.markdown('</div>', unsafe_allow_html=True)

    teams_active = [t for t in set(matches["team1"]) | set(matches["team2"]) if t in ACTIVE_TEAMS]
    with col_h4:
        st.markdown('<div class="metric-green">', unsafe_allow_html=True)
        st.metric("🏟️ Active Teams", len(teams_active))
        st.markdown('</div>', unsafe_allow_html=True)
    with col_h5:
        st.markdown('<div class="metric-red">', unsafe_allow_html=True)
        st.metric("⚾ Deliveries", f"{len(deliveries):,}")
        st.markdown('</div>', unsafe_allow_html=True)


def render_footer():
    """Render the footer."""
    st.markdown('<div class="ciq-footer">Built with CricketIQ Intelligence Engine</div>', unsafe_allow_html=True)
