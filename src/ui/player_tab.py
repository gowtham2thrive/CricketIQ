"""
CricketIQ — Player Stats Tab
==============================
Tab 3: Detailed player batting analytics with charts.
"""

import streamlit as st
import plotly.express as px


def render_player_tab(deliveries):
    """Render the Player Stats tab."""
    st.markdown("<p class='section-label'>Search Player</p>", unsafe_allow_html=True)

    all_players = sorted(deliveries["batsman"].unique().tolist())
    player = st.selectbox("Select player", all_players, label_visibility="collapsed")

    if player:
        bat = deliveries[deliveries["batsman"] == player]
        runs_per_match = bat.groupby("match_id")["batsman_runs"].sum()

        r1, r2, r3, r4 = st.columns(4)
        r1.metric("🔥 Total Runs", int(bat["batsman_runs"].sum()))
        r2.metric("🏏 Matches", bat["match_id"].nunique())
        r3.metric("📊 Average", round(bat["batsman_runs"].sum() / max(bat["match_id"].nunique(), 1), 1))
        r4.metric("🏅 Highest", int(runs_per_match.max()))

        st.markdown("---")

        c_a, c_b = st.columns(2)

        with c_a:
            st.markdown("<p class='section-label'>Runs Per Match</p>", unsafe_allow_html=True)
            rpm_df = runs_per_match.reset_index()
            rpm_df.columns = ["match_id", "runs"]
            fig2 = px.line(rpm_df, x="match_id", y="runs", title="Match-by-Match Performance")
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#5a6178"),
                margin=dict(t=50, b=20, l=10, r=30),
                xaxis=dict(gridcolor="#eef0f4", title="", showgrid=False),
                yaxis=dict(gridcolor="#eef0f4", title="Runs"),
                title_font=dict(size=13, color="#8892a8")
            )
            fig2.update_traces(line_color="#4361ee", line_width=1.5)
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

        with c_b:
            st.markdown("<p class='section-label'>Dismissal Types</p>", unsafe_allow_html=True)
            dismissals = deliveries[
                (deliveries["player_dismissed"] == player) &
                (deliveries["dismissal_kind"].notna())
            ]["dismissal_kind"].value_counts().reset_index()
            dismissals.columns = ["Type", "Count"]
            if not dismissals.empty:
                fig3 = px.pie(
                    dismissals, names="Type", values="Count",
                    color_discrete_sequence=["#4361ee", "#7b8cff", "#a5b4fc", "#c7d0e0", "#dde1e7"],
                    title="How They Got Out"
                )
                fig3.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter", color="#5a6178"),
                    margin=dict(t=40, b=20, l=10, r=10),
                    legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5, font=dict(color="#6b7489")),
                    title_font=dict(size=13, color="#8892a8")
                )
                st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
            else:
                st.caption("No dismissal data.")
