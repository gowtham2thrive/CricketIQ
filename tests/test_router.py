import pandas as pd

try:
    matches = pd.read_csv("matches.csv")
    deliveries = pd.read_csv("deliveries.csv")
    TEAM_MAPPING = {
        "Deccan Chargers": "Sunrisers Hyderabad",
        "Delhi Daredevils": "Delhi Capitals",
        "Kings XI Punjab": "Punjab Kings",
        "Rising Pune Supergiant": "Rising Pune Supergiants",
    }
    for col in ['team1', 'team2', 'winner']:
        matches[col] = matches[col].replace(TEAM_MAPPING)
    for col in ['batting_team', 'bowling_team']:
        deliveries[col] = deliveries[col].replace(TEAM_MAPPING)
    data_ok = True
except Exception as e:
    print(f"Data load error: {e}")
    data_ok = False

PLAYER_ALIASES = {
    "kohli": "V Kohli",
    "rohit": "RG Sharma",
    "dhoni": "MS Dhoni",
    "bumrah": "JJ Bumrah",
    "sachin": "SR Tendulkar",
    "gayle": "CH Gayle",
    "abd": "AB de Villiers",
    "russell": "AD Russell",
    "hardik": "HH Pandya",
    "jadeja": "RA Jadeja",
    "ashwin": "R Ashwin",
    "warner": "DA Warner",
    "pant": "RR Pant"
}

class SessionStateMock:
    def __init__(self):
        self.last_intent = None
        self.last_entity = None

st_session_state = SessionStateMock()

def get_player_stats(player_name: str) -> str:
    return f"🏏 {player_name} Stats..."

def predict_match(team1: str, team2: str) -> str:
    return f"🔮 {team1} vs {team2} Prediction..."

def compare_players(p1: str, p2: str) -> str:
    return f"⚔️ {p1} vs {p2} Comparison..."

def get_top_scorers() -> str:
    return "🏅 Top 5 Scorers..."

def get_team_wins(team_name: str) -> str:
    return f"🏆 {team_name} Win Stats..."

def get_bowling_stats(bowler_name: str) -> str:
    return f"🎳 {bowler_name} Bowling Stats..."

def route_intent(question: str):
    query = question.lower().strip()
    q_words = query.split()
    
    if any(k in query for k in ["who is", "father", "history", "meaning"]):
        return None, None, "This is outside IPL analytics scope. Please ask about IPL stats, players, or teams."

    intent = None
    entity = None
    
    if any(k in query for k in ["top", "highest", "most"]):
        intent = "top"
    elif any(k in query for k in ["vs", "predict", "win", "compare"]):
        intent = "compare_or_team"
    elif any(k in query for k in ["wicket", "bowler", "bowling"]):
        intent = "bowling"
    elif any(k in query for k in ["bat", "batting", "runs", "stats"]):
        intent = "batting"
    elif "what about" in query:
        intent = st_session_state.last_intent

    if data_ok:
        teams_all = set(matches['team1']) | set(matches['team2'])
        teams_sorted = sorted(teams_all, key=len, reverse=True)
        
        matched_teams = [t for t in teams_sorted if t.lower() in query]
        
        players = deliveries['batsman'].unique()
        matched_players = []
        for alias, full_name in PLAYER_ALIASES.items():
            if alias in q_words and full_name not in matched_players:
                matched_players.append(full_name)
        
        if not matched_players:
            for p in players:
                if any(part in query for part in p.lower().split() if len(part) > 2):
                    if p not in matched_players:
                        matched_players.append(p)
        
        entity_type = None
        if matched_teams and not matched_players:
            entity = matched_teams[0]
            entity_type = "team"
        elif matched_players:
            entity = matched_players[0]
            entity_type = "player"
        else:
            entity = st_session_state.last_entity
            if entity is not None:
                entity_type = "player" if entity in players else "team" if entity in teams_all else None

        print(f"DEBUG - Intent: {intent}, Entity: {entity}, EntityType: {entity_type}")

        if "vs" in query or "compare" in query:
            if len(matched_teams) >= 2:
                st_session_state.last_intent = "compare_or_team"
                return predict_match(matched_teams[0], matched_teams[1]), "High", None
            if len(matched_players) >= 2:
                st_session_state.last_intent = "batting"
                return compare_players(matched_players[0], matched_players[1]), "High", None
        
        if intent == "top":
            st_session_state.last_intent = "top"
            return get_top_scorers(), "High", None
        
        if entity:
            st_session_state.last_entity = entity
            if entity_type == "team":
                st_session_state.last_intent = "team"
                return get_team_wins(entity), "High", None
            elif entity_type == "player":
                if intent == "bowling":
                    st_session_state.last_intent = "bowling"
                    return get_bowling_stats(entity), "High", None
                else:
                    st_session_state.last_intent = "batting"
                    return get_player_stats(entity), "High", None
                    
    return None, "Low", "I couldn't understand that clearly. Try asking about player stats, team performance, or comparisons."

test_cases = [
    "kohli stats",
    "dhoni",
    "top runs",
    "mi wins",
    "rcb vs csk",
    "father of cricket"
]

print("--- ROUTER VALIDATION TESTS ---")
for q in test_cases:
    print(f"\nQuery: '{q}'")
    action, confidence, msg = route_intent(q)
    print(f"Confidence: {confidence}")
    if action:
        print(f"Action Output: {action.strip()}")
    else:
        print(f"Fallback Message: {msg}")
