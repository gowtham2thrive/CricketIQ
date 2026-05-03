import google.generativeai as genai
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# ── Config ──────────────────────────────────────
API_KEY = os.getenv("GEMINI_API_KEY", "")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("⚠️ GEMINI_API_KEY not set in .env file. AI features will not work.")

# ── Load Data ────────────────────────────────────
try:
    matches    = pd.read_csv("matches.csv")
    deliveries = pd.read_csv("deliveries.csv")
except FileNotFoundError:
    print("Warning: CSV files not found. The tools will not work without them.")
    matches = pd.DataFrame(columns=['id', 'season', 'city', 'date', 'team1', 'team2', 'winner', 'player_of_match', 'venue', 'umpire1', 'umpire2', 'umpire3'])
    deliveries = pd.DataFrame(columns=['match_id', 'inning', 'batting_team', 'bowling_team', 'batsman', 'bowler', 'non_striker', 'is_super_over', 'wide_runs', 'bye_runs', 'legbye_runs', 'noball_runs', 'penalty_runs', 'batsman_runs', 'extra_runs', 'total_runs', 'player_dismissed', 'dismissal_kind', 'fielder'])

# ── Tools ────────────────────────────────────────

def get_player_stats(player_name: str) -> str:
    """Get batting stats for any IPL player"""
    bat = deliveries[deliveries['batsman'] == player_name]
    if bat.empty:
        return f"No data found for {player_name}"
    
    total_runs     = bat['batsman_runs'].sum()
    matches_played = bat['match_id'].nunique()
    average        = round(total_runs / matches_played, 2)
    highest        = bat.groupby('match_id')['batsman_runs'].sum().max()

    return f"""
    🏏 {player_name} IPL Stats:
    ├─ Total Runs    : {total_runs}
    ├─ Matches       : {matches_played}
    ├─ Average       : {average}
    └─ Highest Score : {highest}
    """

def predict_match(team1: str, team2: str) -> str:
    """Predict winner based on head to head history"""
    h2h = matches[
        ((matches['team1'] == team1) & (matches['team2'] == team2)) |
        ((matches['team1'] == team2) & (matches['team2'] == team1))
    ]
    
    t1_wins = matches[matches['winner'] == team1].shape[0]
    t2_wins = matches[matches['winner'] == team2].shape[0]
    total   = max(h2h.shape[0], 1)
    
    t1_prob   = round((t1_wins / (t1_wins + t2_wins)) * 100, 1) if (t1_wins + t2_wins) > 0 else 0
    t2_prob   = round((t2_wins / (t1_wins + t2_wins)) * 100, 1) if (t1_wins + t2_wins) > 0 else 0
    predicted = team1 if t1_wins >= t2_wins else team2

    return f"""
    🔮 Prediction: {team1} vs {team2}
    ├─ H2H Matches        : {total}
    ├─ {team1} Win %      : {t1_prob}%
    ├─ {team2} Win %      : {t2_prob}%
    └─ 🏆 Predicted Winner: {predicted}
    """

def get_top_scorers() -> str:
    """Get top 5 all time IPL run scorers"""
    top = (deliveries.groupby('batsman')['batsman_runs']
                     .sum()
                     .sort_values(ascending=False)
                     .head(5))
    
    result = "🏅 Top 5 IPL Run Scorers:\n"
    for i, (player, runs) in enumerate(top.items(), 1):
        result += f"  {i}. {player} — {runs} runs\n"
    return result

def get_team_wins(team_name: str) -> str:
    """Get total wins for a team"""
    wins  = matches[matches['winner'] == team_name].shape[0]
    total = matches[
        (matches['team1'] == team_name) | 
        (matches['team2'] == team_name)
    ].shape[0]
    rate = round((wins / total) * 100, 1) if total > 0 else 0

    return f"""
    🏆 {team_name}:
    ├─ Total Matches : {total}
    ├─ Wins          : {wins}
    ├─ Losses        : {total - wins}
    └─ Win Rate      : {rate}%
    """

def get_bowling_stats(bowler_name: str) -> str:
    """Get bowling stats for any IPL bowler including wickets, matches, and economy rate."""
    bowl = deliveries[deliveries['bowler'] == bowler_name]
    if bowl.empty:
        return f"No data found for {bowler_name}"

    wickets  = int(bowl['player_dismissed'].notna().sum())
    matches_ = bowl['match_id'].nunique()
    balls    = len(bowl[bowl['wide_runs'] == 0])
    runs     = int(bowl['total_runs'].sum() - bowl['bye_runs'].sum() - bowl['legbye_runs'].sum())
    overs    = balls / 6
    economy  = round(runs / overs, 2) if overs > 0 else 0

    return f"""
    🎳 {bowler_name} IPL Bowling Stats:
    ├─ Wickets      : {wickets}
    ├─ Matches      : {matches_}
    ├─ Economy Rate : {economy}
    └─ Balls Bowled : {balls}
    """

# ── Agent ────────────────────────────────────────

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=[get_player_stats, predict_match, 
           get_top_scorers, get_team_wins, get_bowling_stats],
    system_instruction="""
    You are CricketIQ — an expert IPL cricket analyst.
    
    Rules:
    - Always use tools to fetch real stats
    - Give short, sharp answers
    - Use cricket emojis 🏏🏆🔥
    - Never guess — always use data
    - End every answer with a confidence level
    """
)

chat = model.start_chat(enable_automatic_function_calling=True)

# ── Run ──────────────────────────────────────────

if __name__ == "__main__":
    print("🏏 CricketIQ is Ready!")
    print("Ask me anything about IPL.")
    print("Type 'quit' to exit\n")

    while True:
        try:
            question = input("You: ").strip()
            if question.lower() == "quit":
                break
            if question:
                response = chat.send_message(question)
                print(f"\nCricketIQ: {response.text}\n")
        except Exception as e:
            print(f"Error: {e}")
            break
