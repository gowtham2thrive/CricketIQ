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


def get_top_teams(matches) -> str:
    """Get top teams ranked by total wins."""
    teams_all = set(matches["team1"]) | set(matches["team2"])
    team_stats = []
    for team in teams_all:
        wins = matches[matches["winner"] == team].shape[0]
        total = matches[(matches["team1"] == team) | (matches["team2"] == team)].shape[0]
        rate = round((wins / total) * 100, 1) if total else 0
        team_stats.append((team, wins, total, rate))

    team_stats.sort(key=lambda x: x[1], reverse=True)

    result = "🏆 Top IPL Teams by Wins:\n"
    for i, (team, wins, total, rate) in enumerate(team_stats[:8], 1):
        bar = "█" * int(rate / 10)
        result += f"  {i}. {team} — {wins} wins / {total} matches ({rate}%) {bar}\n"
    return result
