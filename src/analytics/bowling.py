"""
CricketIQ — Bowling Analytics
===============================
Functions for bowler statistics.
"""


def get_bowling_stats(bowler_name: str, deliveries) -> str:
    """Get bowling stats for any IPL bowler."""
    bowl = deliveries[deliveries["bowler"] == bowler_name]
    if bowl.empty:
        return f"No data for {bowler_name}"
    wickets = int(bowl["player_dismissed"].notna().sum())
    matches_ = bowl["match_id"].nunique()
    balls = len(bowl[bowl["wide_runs"] == 0])
    runs = int(bowl["total_runs"].sum() - bowl["bye_runs"].sum() - bowl["legbye_runs"].sum())
    overs = balls / 6
    economy = round(runs / overs, 2) if overs > 0 else 0
    return f"🎳 {bowler_name} | Wickets: {wickets} | Matches: {matches_} | Economy: {economy}"
