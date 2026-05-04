"""
CricketIQ — Predictions & Leaderboards
========================================
Match prediction and top scorer functions.
"""


def predict_match(team1: str, team2: str, matches) -> str:
    """Predict winner based on historical win counts."""
    t1 = matches[matches["winner"] == team1].shape[0]
    t2 = matches[matches["winner"] == team2].shape[0]
    total = max(t1 + t2, 1)
    p1 = round((t1 / total) * 100, 1)
    p2 = round((t2 / total) * 100, 1)
    winner = team1 if t1 >= t2 else team2
    return f"🔮 {team1} {p1}% vs {team2} {p2}% → 🏆 {winner}"


def get_top_scorers(deliveries) -> str:
    """Get top 5 all-time IPL run scorers."""
    top = deliveries.groupby("batsman")["batsman_runs"].sum().sort_values(ascending=False).head(5)
    result = "🏅 Top 5:\n"
    for i, (p, r) in enumerate(top.items(), 1):
        result += f"{i}. {p} — {int(r)} runs\n"
    return result
