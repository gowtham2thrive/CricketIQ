"""
CricketIQ — Leaderboards Tab
==============================
Tab 4: Top run scorers, team wins, and season-wise match trends.
"""

import streamlit as st
import plotly.express as px


def render_leaderboard_tab(matches, deliveries):
    """Render the Leaderboards tab."""
    l1, l2 = st.columns(2)

    with l1:
        st.markdown("<p class='section-label'>🏏 Top 10 Run Scorers</p>", unsafe_allow_html=True)
        top_bat = (deliveries.groupby("batsman")["batsman_runs"]
                             .sum()
                             .sort_values(ascending=False)
                             .head(10)
                             .reset_index())
        top_bat.columns = ["Player", "Runs"]
        top_bat["Runs"] = top_bat["Runs"].astype(int)
        top_bat.index = top_bat.index + 1

        fig4 = px.bar(top_bat, x="Runs", y="Player", orientation="h", text="Runs", title="All-Time Run Leaders")
        fig4.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#5a6178"),
            margin=dict(t=50, b=20, l=10, r=30),
            yaxis=dict(autorange="reversed", gridcolor="#eef0f4", title=""),
            xaxis=dict(gridcolor="#eef0f4", title="", showgrid=False),
            title_font=dict(size=13, color="#8892a8")
        )
        fig4.update_traces(marker_color="#4361ee", textfont_color="#ffffff")
        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

    with l2:
        st.markdown("<p class='section-label'>🏆 Team Win Count</p>", unsafe_allow_html=True)
        team_wins = matches["winner"].value_counts().head(10).reset_index()
        team_wins.columns = ["Team", "Wins"]
        team_wins.index = team_wins.index + 1

        fig5 = px.bar(team_wins, x="Wins", y="Team", orientation="h", text="Wins", title="Most Successful Teams")
        fig5.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#5a6178"),
            margin=dict(t=50, b=20, l=10, r=30),
            yaxis=dict(autorange="reversed", gridcolor="#eef0f4", title=""),
            xaxis=dict(gridcolor="#eef0f4", title="", showgrid=False),
            title_font=dict(size=13, color="#8892a8")
        )
        fig5.update_traces(
            marker_color="#eef0ff",
            marker_line_color="#4361ee",
            marker_line_width=1,
            textfont_color="#4361ee"
        )
        st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})

    st.markdown("---")

    st.markdown("<p class='section-label'>📈 Season-wise Match Count</p>", unsafe_allow_html=True)
    season_df = matches.groupby("season").agg(Matches=("id", "count")).reset_index()
    fig6 = px.line(season_df, x="season", y="Matches", markers=True, title="Matches Per Season")
    fig6.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#5a6178"),
        margin=dict(t=50, b=20, l=10, r=30),
        xaxis=dict(gridcolor="#eef0f4", title="Season", showgrid=False),
        yaxis=dict(gridcolor="#eef0f4", title="Matches"),
        title_font=dict(size=13, color="#8892a8")
    )
    fig6.update_traces(line_color="#4361ee", marker_color="#4361ee", line_width=2)
    st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})
