"""
CricketIQ — Match Prediction Tab
==================================
Tab 2: Historical win probability analysis with interactive charts.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from src.config import ACTIVE_TEAMS


def render_prediction_tab(matches):
    """Render the Smart Match Insights tab."""
    st.markdown("<p class='section-label'>Select Teams</p>", unsafe_allow_html=True)

    teams_all_sorted = sorted(set(matches["team1"]) | set(matches["team2"]))
    teams_active_sorted = sorted([t for t in teams_all_sorted if t in ACTIVE_TEAMS])

    show_historical = st.toggle("🕰️ Include historical teams", value=False)
    team_list = teams_all_sorted if show_historical else teams_active_sorted

    c1, c2 = st.columns(2)
    with c1:
        team1 = st.selectbox("Team 1", team_list, index=0)
    with c2:
        team2 = st.selectbox("Team 2", team_list, index=min(1, len(team_list) - 1))

    st.markdown("")
    predict_btn = st.button("🔮  Analyze Historical Win Probability", use_container_width=True)

    if predict_btn:
        if team1 == team2:
            st.warning("Select two different teams.")
        else:
            t1_wins = matches[matches["winner"] == team1].shape[0]
            t2_wins = matches[matches["winner"] == team2].shape[0]
            total = max(t1_wins + t2_wins, 1)
            p1 = round((t1_wins / total) * 100, 1)
            p2 = round((t2_wins / total) * 100, 1)
            winner = team1 if t1_wins >= t2_wins else team2

            st.markdown("---")

            confidence = round(abs(p1 - p2), 1)
            h2h_total = matches[
                ((matches["team1"] == team1) & (matches["team2"] == team2)) |
                ((matches["team1"] == team2) & (matches["team2"] == team1))
            ].shape[0]

            # Historical Win Probability banner
            st.markdown(f"""
            <div style='text-align:center;padding:1.8rem 1.5rem;background:linear-gradient(135deg,#f8f9ff 0%,#ffffff 100%);border:1px solid #e2e5ea;border-top:3px solid #4361ee;border-radius:12px;margin-bottom:.6rem;'>
                <p style='font-size:.6rem;text-transform:uppercase;letter-spacing:.25em;color:#8892a8;margin:0 0 .15rem;'>Historical Win Probability</p>
                <p style='font-family:"Plus Jakarta Sans",sans-serif;font-size:2.2rem;font-weight:800;color:#4361ee;margin:.3rem 0 .4rem;letter-spacing:-.02em;'>{winner}</p>
                <span style='display:inline-block;background:#eef0ff;border:1px solid #c7d0ff;color:#4361ee;font-size:.68rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;padding:.25rem .75rem;border-radius:20px;'>
                    {confidence}% confidence
                </span>
                <p style='font-size:.72rem;color:#a0a8b8;margin:.8rem 0 0;'>Based on historical match wins across IPL seasons</p>
            </div>
            """, unsafe_allow_html=True)

            # Metrics row
            m1, m2, m3 = st.columns(3)
            m1.metric(team1, f"{p1}%", f"{t1_wins} wins")
            m2.metric("H2H Matches", h2h_total)
            m3.metric(team2, f"{p2}%", f"{t2_wins} wins")

            # Progress bar
            st.markdown(f"""
            <div style='display:flex;justify-content:space-between;margin-top:.6rem;margin-bottom:.2rem;'>
                <span style='font-size:.7rem;font-weight:600;color:{"#4361ee" if winner==team1 else "#8892a8"};'>{team1} {p1}%</span>
                <span style='font-size:.7rem;font-weight:600;color:{"#4361ee" if winner==team2 else "#8892a8"};'>{p2}% {team2}</span>
            </div>
            """, unsafe_allow_html=True)
            st.progress(int(p1))

            # Head to head chart
            h2h_df = pd.DataFrame({
                "Team": [team1, team2],
                "Wins": [t1_wins, t2_wins],
            })
            fig = px.bar(
                h2h_df, x="Team", y="Wins", text="Wins",
                color="Team",
                color_discrete_map={team1: "#4361ee", team2: "#c7d0e0"},
                title="Head-to-Head Wins"
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#5a6178"),
                showlegend=False,
                margin=dict(t=50, b=20, l=10, r=30),
                xaxis=dict(gridcolor="#eef0f4", showgrid=False),
                yaxis=dict(gridcolor="#eef0f4"),
                title_font=dict(size=13, color="#8892a8")
            )
            fig.update_traces(textfont_color="#ffffff")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
