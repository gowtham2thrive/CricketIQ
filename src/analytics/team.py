"""
CricketIQ — Team Analytics
============================
Functions for team win statistics.
"""


def get_team_wins(team_name: str, matches) -> str:
    """Get total wins and win rate for a team."""
    wins = matches[matches["winner"] == team_name].shape[0]
    total = matches[(matches["team1"] == team_name) | (matches["team2"] == team_name)].shape[0]
    rate = round((wins / total) * 100, 1) if total else 0
    return f"🏆 {team_name} | Wins: {wins}/{total} | Win Rate: {rate}%"
