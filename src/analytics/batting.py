"""
CricketIQ — Batting Analytics
===============================
Functions for player batting statistics and comparisons.
"""


def get_player_stats(player_name: str, deliveries) -> str:
    """Get batting stats for any IPL player."""
    bat = deliveries[deliveries["batsman"] == player_name]
    if bat.empty:
        return f"No data for {player_name}"
    runs = int(bat["batsman_runs"].sum())
    matches_ = bat["match_id"].nunique()
    avg = round(runs / matches_, 2) if matches_ > 0 else 0
    highest = int(bat.groupby("match_id")["batsman_runs"].sum().max()) if matches_ > 0 else 0
    return f"🏏 {player_name} | Runs: {runs} | Matches: {matches_} | Avg: {avg} | Highest: {highest}"


def compare_players(p1: str, p2: str, deliveries) -> str:
    """Compare two players' batting performance."""
    def get_stats(p):
        bat = deliveries[deliveries["batsman"] == p]
        runs = int(bat["batsman_runs"].sum())
        m = bat["match_id"].nunique()
        avg = round(runs / m, 2) if m > 0 else 0
        return runs, m, avg

    r1, m1, a1 = get_stats(p1)
    r2, m2, a2 = get_stats(p2)
    better = p1 if r1 >= r2 else p2
    return (
        f"⚔️ {p1} vs {p2}\n"
        f"{p1}: {r1} runs, {m1} matches, {a1} avg\n"
        f"{p2}: {r2} runs, {m2} matches, {a2} avg\n"
        f"🏆 Better performer overall: {better}"
    )
