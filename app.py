import streamlit as st
from google import genai
from google.genai import types
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

# ── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CricketIQ",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-display: 'Plus Jakarta Sans', 'Inter', sans-serif;
    --accent: #4361ee;
    --accent-hover: #3a56d4;
    --accent-soft: rgba(67, 97, 238, 0.08);
    --accent-glow: rgba(67, 97, 238, 0.15);
    --bg: #f0f2f7;
    --card: rgba(255, 255, 255, 0.65);
    --card-hover: rgba(255, 255, 255, 0.85);
    --border: rgba(226, 230, 238, 0.6);
    --border-light: rgba(255, 255, 255, 0.8);
    --text: #1a1e2d;
    --text-muted: #5a6178;
    --text-light: #8892a8;
    --shadow-sm: 0 4px 15px rgba(0,0,0,.03);
    --shadow-md: 0 8px 30px rgba(0,0,0,.06);
    --shadow-lg: 0 12px 40px rgba(0,0,0,.08);
    --radius: 16px;
    --radius-sm: 10px;
    --transition: all .3s cubic-bezier(.4,0,.2,1);
}

* { font-family: var(--font-body); box-sizing: border-box !important; -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility; }
html { font-size: 16px; }

/* ── Background depth ── */
.stApp {
    background: linear-gradient(135deg, #e4eaff 0%, #f4f5f8 50%, #eaeefe 100%);
    background-attachment: fixed;
    color: var(--text); font-size: .9rem; line-height: 1.65;
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; visibility: hidden !important; }
.block-container { padding-top: 1rem; padding-bottom: 1.5rem; max-width: 1200px; }

/* ── Tabs — premium pill bar ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--card); border: 1px solid var(--border-light); border-radius: var(--radius);
    padding: .35rem; gap: .35rem; box-shadow: var(--shadow-sm);
    justify-content: center; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: var(--text-light) !important;
    font-size: .84rem !important; font-family: var(--font-body) !important;
    font-weight: 500 !important; padding: .7rem 1.5rem !important;
    border-radius: var(--radius-sm) !important; border-bottom: none !important;
    transition: var(--transition) !important; position: relative !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-muted) !important; background: var(--card-hover) !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent) !important; background: var(--card) !important;
    font-weight: 600 !important; border-bottom: none !important;
    box-shadow: 0 4px 15px var(--accent-glow) !important;
    border: 1px solid var(--border-light) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; background-color: transparent !important; }

/* ── Inputs ── */
.stTextInput input, .stSelectbox div[data-baseweb="select"] {
    background: var(--card) !important; border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important; color: var(--text) !important;
    font-family: var(--font-body) !important; font-size: .88rem !important;
    transition: var(--transition) !important; backdrop-filter: blur(8px);
}
.stTextInput input:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 3px var(--accent-glow) !important; }

/* ── Buttons — micro-interaction ── */
.stButton > button {
    background: var(--card) !important; color: var(--text-muted) !important;
    border: 1px solid var(--border-light) !important; border-radius: var(--radius-sm) !important;
    font-family: var(--font-body) !important; font-weight: 500 !important;
    font-size: .82rem !important; padding: .55rem 1.2rem !important;
    box-shadow: var(--shadow-sm); transition: var(--transition) !important;
    backdrop-filter: blur(8px);
}
.stButton > button:hover {
    border-color: var(--accent) !important; color: var(--accent) !important;
    background: var(--card-hover) !important;
    box-shadow: 0 6px 20px var(--accent-glow) !important;
    transform: translateY(-2px) scale(1.02);
}

/* ── Metric cards — colored accents ── */
[data-testid="stMetric"] {
    background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
    border-top: 1px solid var(--border-light); border-left: 1px solid var(--border-light);
    padding: 1.3rem 1.5rem !important; box-shadow: var(--shadow-sm);
    transition: var(--transition); position: relative; overflow: hidden;
    backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
}
[data-testid="stMetric"]:hover { box-shadow: var(--shadow-md); transform: translateY(-4px); background: var(--card-hover); }
[data-testid="stMetricLabel"] {
    font-family: var(--font-body) !important; font-size: .58rem !important;
    font-weight: 600 !important; text-transform: uppercase; letter-spacing: .12em;
    color: var(--text-light) !important;
}
[data-testid="stMetricValue"] {
    font-family: var(--font-display) !important; font-size: 1.9rem !important;
    font-weight: 800 !important; color: var(--text) !important;
    letter-spacing: -.03em; line-height: 1.15 !important;
}
[data-testid="stMetricDelta"] { font-family: var(--font-body) !important; font-size: .72rem !important; font-weight: 500 !important; }

/* Metric color accents via nth-child on columns */
.metric-blue [data-testid="stMetricValue"] { color: #3b82f6 !important; }
.metric-purple [data-testid="stMetricValue"] { color: #8b5cf6 !important; }
.metric-orange [data-testid="stMetricValue"] { color: #f59e0b !important; }
.metric-green [data-testid="stMetricValue"] { color: #10b981 !important; }
.metric-red [data-testid="stMetricValue"] { color: #ef4444 !important; }
.metric-blue [data-testid="stMetric"] { border-top: 3px solid rgba(59, 130, 246, 0.8); }
.metric-purple [data-testid="stMetric"] { border-top: 3px solid rgba(139, 92, 246, 0.8); }
.metric-orange [data-testid="stMetric"] { border-top: 3px solid rgba(245, 158, 11, 0.8); }
.metric-green [data-testid="stMetric"] { border-top: 3px solid rgba(16, 185, 129, 0.8); }
.metric-red [data-testid="stMetric"] { border-top: 3px solid rgba(239, 68, 68, 0.8); }

/* ── Chat bubbles ── */
.stChatMessage { border: 1px solid var(--border-light) !important; border-radius: var(--radius) !important; box-shadow: var(--shadow-sm); margin-bottom: .5rem !important; backdrop-filter: blur(12px); }
.stChatMessage[data-testid="chat-message-user"] { background: var(--accent-soft) !important; border-color: rgba(67, 97, 238, 0.2) !important; }
.stChatMessage[data-testid="chat-message-assistant"] { background: var(--card) !important; }
[data-testid="stChatMessageContent"] { color: #3a3f52 !important; font-family: var(--font-body) !important; font-size: .88rem !important; line-height: 1.75 !important; }

/* ── Chat input ── */
.stChatInput > div {
    background: var(--card) !important;
    backdrop-filter: blur(18px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(18px) saturate(180%) !important;
    border: 1px solid var(--border-light) !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow-sm) !important;
    transition: var(--transition) !important;
}
.stChatInput > div:focus-within { border-color: rgba(67,97,238,.4) !important; box-shadow: 0 6px 30px var(--accent-glow), 0 0 0 3px var(--accent-glow) !important; background: var(--card-hover) !important;}
.stChatInput input { color: var(--text) !important; font-family: var(--font-body) !important; font-size: .88rem !important; background: transparent !important; }
.stChatInput input::placeholder { color: #9aa3b8 !important; }
.stChatInput button {
    background: var(--accent) !important; color: #fff !important;
    border: none !important; border-radius: var(--radius-sm) !important;
    transition: var(--transition) !important;
}
.stChatInput button:hover { background: var(--accent-hover) !important; transform: scale(1.05); }

/* ── Charts & Progress & Data ── */
.stProgress > div { background-color: rgba(226, 229, 234, 0.5) !important; border-radius: 8px !important; height: 10px !important; backdrop-filter: blur(4px); }
.stProgress > div > div { background: linear-gradient(90deg, var(--accent), #7b8cff) !important; border-radius: 8px !important; box-shadow: 0 0 10px var(--accent-glow) !important;}
[data-testid="stPlotlyChart"] {
    box-sizing: border-box !important;
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-top: 1px solid var(--border-light) !important;
    border-left: 1px solid var(--border-light) !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    box-shadow: var(--shadow-sm) !important;
    transition: var(--transition);
    backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
}
[data-testid="stPlotlyChart"]:hover { box-shadow: var(--shadow-md) !important; transform: translateY(-2px); background: var(--card-hover) !important; }
[data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius: var(--radius) !important; overflow: hidden; backdrop-filter: blur(16px); }
hr { border-color: var(--border) !important; opacity: .4; }

/* ── Hero header — gradient title ── */
.ciq-hero { text-align: center; padding: 2rem 0 1rem; }
.ciq-hero h1 {
    font-family: var(--font-display); font-size: 3.5rem; font-weight: 800;
    letter-spacing: -.04em; margin: 0; line-height: 1.1;
    background: linear-gradient(270deg, #1a1e2d, #4361ee, #7b8cff, #4361ee);
    background-size: 200% 200%;
    animation: GradientShift 6s ease infinite;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
@keyframes GradientShift { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
.ciq-hero .tagline {
    font-family: var(--font-body); font-size: .75rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: .25em; color: var(--text-muted);
    margin-top: .75rem;
}

/* ── Section label ── */
.section-label { font-family: var(--font-body); font-size: .65rem; font-weight: 600; text-transform: uppercase; letter-spacing: .18em; color: var(--text-light); margin-bottom: .6rem; }

/* ── Card wrapper ── */
.ui-card {
    background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
    border-top: 1px solid var(--border-light); border-left: 1px solid var(--border-light);
    padding: 1.5rem; box-shadow: var(--shadow-sm); margin-bottom: .8rem;
    backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); transition: var(--transition);
}
.ui-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); background: var(--card-hover); }

/* ── Chat card container ── */
.chat-card {
    background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
    border-top: 1px solid var(--border-light); border-left: 1px solid var(--border-light);
    padding: 1.4rem 1.6rem 1rem; box-shadow: var(--shadow-sm); margin-bottom: .6rem;
    backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); transition: var(--transition);
}
.chat-card-title {
    font-family: var(--font-display); font-size: 1.05rem; font-weight: 700;
    color: var(--text); margin: 0 0 .2rem; display: flex; align-items: center; gap: .4rem;
}
.chat-card-subtitle {
    font-family: var(--font-body); font-size: .65rem; font-weight: 500;
    color: var(--text-muted); text-transform: uppercase; letter-spacing: .12em; margin: 0;
}

/* ── Quick Insights grid ── */
.insights-title {
    font-family: var(--font-display); font-size: 1rem; font-weight: 700;
    color: var(--text); margin: 0 0 .7rem; display: flex; align-items: center; gap: .35rem;
}
.insights-grid .stButton > button {
    min-height: 2.8rem; font-size: .78rem !important; font-weight: 600 !important;
    border: 1px solid var(--border-light) !important; box-shadow: var(--shadow-sm) !important;
    transition: var(--transition) !important;
}
.insights-grid .stButton > button:hover {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: var(--shadow-md) !important;
}

/* ── Footer ── */
.ciq-footer {
    text-align: center; padding: 1.5rem 0 .5rem;
    font-family: var(--font-body); font-size: .6rem; font-weight: 500;
    text-transform: uppercase; letter-spacing: .2em; color: var(--text-light);
}

/* ── Dots / Trust ── */
.dot-green { color: #22c55e; font-size: .55rem; }
.dot-red   { color: #ef4444; font-size: .55rem; }
.trust-badge { display: inline-block; font-family: var(--font-body); font-size: .6rem; font-weight: 500; color: var(--text-light); background: var(--bg); border: 1px solid var(--border); border-radius: 20px; padding: .2rem .7rem; }

/* ── Responsive ── */
@media (max-width: 1024px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
    .ciq-hero h1 { font-size: 2.6rem; }
    [data-testid="stMetricValue"] { font-size: 1.5rem !important; }
    .stTabs [data-baseweb="tab"] { font-size: .78rem !important; padding: .6rem 1.1rem !important; }
}
@media (max-width: 768px) {
    .block-container { padding-left: .75rem; padding-right: .75rem; }
    .ciq-hero h1 { font-size: 2.1rem; }
    [data-testid="stMetric"] { padding: 1rem 1.1rem !important; }
    [data-testid="stMetricLabel"] { font-size: .56rem !important; }
    [data-testid="stMetricValue"] { font-size: 1.3rem !important; }
    .stTabs [data-baseweb="tab"] { font-size: .72rem !important; padding: .5rem .8rem !important; }
    .stChatInput > div { border-radius: 12px !important; }
}
@media (max-width: 480px) {
    html { font-size: 14px; }
    .block-container { padding-left: .5rem; padding-right: .5rem; }
    .ciq-hero h1 { font-size: 1.7rem; }
    [data-testid="stMetricValue"] { font-size: 1.1rem !important; }
    .stTabs [data-baseweb="tab"] { font-size: .68rem !important; padding: .45rem .6rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ── Load Data ────────────────────────────────────────────────────────────────
# ── Team Name Normalization ──────────────────────────────────────────────────
TEAM_MAPPING = {
    "Deccan Chargers": "Sunrisers Hyderabad",
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Rising Pune Supergiant": "Rising Pune Supergiants",
}

ACTIVE_TEAMS = [
    "Chennai Super Kings",
    "Delhi Capitals",
    "Kolkata Knight Riders",
    "Mumbai Indians",
    "Punjab Kings",
    "Rajasthan Royals",
    "Royal Challengers Bangalore",
    "Sunrisers Hyderabad",
]

@st.cache_data
def load_data():
    try:
        m = pd.read_csv("matches.csv")
        d = pd.read_csv("deliveries.csv")
        # Normalize team names to modern equivalents
        for col in ['team1', 'team2', 'winner']:
            m[col] = m[col].replace(TEAM_MAPPING)
        for col in ['batting_team', 'bowling_team']:
            d[col] = d[col].replace(TEAM_MAPPING)
        return m, d, True
    except:
        return None, None, False

matches, deliveries, data_ok = load_data()

# Resolve key from .env
API_KEY = os.getenv("GEMINI_API_KEY", "")

# ── Hero Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="ciq-hero">
    <h1>CricketIQ</h1>
    <div class="tagline">AI-Powered IPL Intelligence Engine (2008 - 2020)</div>
</div>
""", unsafe_allow_html=True)

col_h1, col_h2, col_h3, col_h4, col_h5 = st.columns(5)
if data_ok:
    with col_h1:
        st.markdown('<div class="metric-blue">', unsafe_allow_html=True)
        st.metric("🏏 Matches", len(matches))
        st.markdown('</div>', unsafe_allow_html=True)
    with col_h2:
        st.markdown('<div class="metric-purple">', unsafe_allow_html=True)
        st.metric("👤 Players", deliveries['batsman'].nunique())
        st.markdown('</div>', unsafe_allow_html=True)
    with col_h3:
        st.markdown('<div class="metric-orange">', unsafe_allow_html=True)
        st.metric("📅 Seasons", matches['season'].nunique())
        st.markdown('</div>', unsafe_allow_html=True)
    teams_active = [t for t in set(matches['team1']) | set(matches['team2']) if t in ACTIVE_TEAMS]
    with col_h4:
        st.markdown('<div class="metric-green">', unsafe_allow_html=True)
        st.metric("🏟️ Active Teams", len(teams_active))
        st.markdown('</div>', unsafe_allow_html=True)
    with col_h5:
        st.markdown('<div class="metric-red">', unsafe_allow_html=True)
        st.metric("⚾ Deliveries", f"{len(deliveries):,}")
        st.markdown('</div>', unsafe_allow_html=True)

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🤖  AI Chat",
    "🔮  Smart Match Insights",
    "🏏  Player Stats",
    "🏆  Leaderboards"
])

# ═══════════════════════════════════════════════════════
# TAB 1 — AI CHAT
# ═══════════════════════════════════════════════════════
with tab1:
    if not API_KEY:
        st.warning("⚠️ Please set your GEMINI_API_KEY in the .env file")
    else:
        # Tools
        def get_player_stats(player_name: str) -> str:
            if not data_ok: return "Data not loaded."
            bat = deliveries[deliveries['batsman'] == player_name]
            if bat.empty: return f"No data for {player_name}"
            runs     = int(bat['batsman_runs'].sum())
            matches_ = bat['match_id'].nunique()
            avg      = round(runs / matches_, 2)
            highest  = int(bat.groupby('match_id')['batsman_runs'].sum().max())
            return f"🏏 {player_name} | Runs: {runs} | Matches: {matches_} | Avg: {avg} | Highest: {highest}"

        def predict_match(team1: str, team2: str) -> str:
            if not data_ok: return "Data not loaded."
            t1 = matches[matches['winner'] == team1].shape[0]
            t2 = matches[matches['winner'] == team2].shape[0]
            total = max(t1 + t2, 1)
            p1 = round((t1 / total) * 100, 1)
            p2 = round((t2 / total) * 100, 1)
            winner = team1 if t1 >= t2 else team2
            return f"🔮 {team1} {p1}% vs {team2} {p2}% → 🏆 {winner}"

        def get_top_scorers() -> str:
            if not data_ok: return "Data not loaded."
            top = deliveries.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(5)
            result = "🏅 Top 5:\n"
            for i, (p, r) in enumerate(top.items(), 1):
                result += f"{i}. {p} — {int(r)} runs\n"
            return result

        def get_team_wins(team_name: str) -> str:
            if not data_ok: return "Data not loaded."
            wins  = matches[matches['winner'] == team_name].shape[0]
            total = matches[(matches['team1'] == team_name) | (matches['team2'] == team_name)].shape[0]
            rate  = round((wins / total) * 100, 1) if total else 0
            return f"🏆 {team_name} | Wins: {wins}/{total} | Win Rate: {rate}%"

        def get_bowling_stats(bowler_name: str) -> str:
            """Get bowling stats for any IPL bowler including wickets, matches, and economy rate."""
            if not data_ok: return "Data not loaded."
            bowl = deliveries[deliveries['bowler'] == bowler_name]
            if bowl.empty: return f"No data for {bowler_name}"
            wickets  = int(bowl['player_dismissed'].notna().sum())
            matches_ = bowl['match_id'].nunique()
            balls    = len(bowl[bowl['wide_runs'] == 0])  # exclude wides from ball count
            runs     = int(bowl['total_runs'].sum() - bowl['bye_runs'].sum() - bowl['legbye_runs'].sum())
            overs    = balls / 6
            economy  = round(runs / overs, 2) if overs > 0 else 0
            return f"🎳 {bowler_name} | Wickets: {wickets} | Matches: {matches_} | Economy: {economy}"

        # ── Manual Intent Router ─────────────────────────────────────────────
        def route_intent(question: str):
            """Manual tool routing before Gemini."""
            query = " ".join(question.lower().strip().split())
            
            # 5. OUT-OF-SCOPE HANDLING
            if any(k in query for k in ["who is", "father", "history", "meaning"]):
                return None, None, "This is outside IPL analytics scope. Please ask about IPL stats, players, or teams."

            # 2. PLAYER NAME DETECTION
            if data_ok:
                players = deliveries['batsman'].unique()
                for player in players:
                    if any(part in query for part in player.lower().split() if len(part) > 2):
                        confidence = "High" if player.lower() in query else "Medium"
                        return get_player_stats(player), confidence, None

            # 3. TEAM NAME DETECTION
            if data_ok:
                teams_all = set(matches['team1']) | set(matches['team2'])
                for team in teams_all:
                    if team.lower() in query:
                        return get_team_wins(team), "High", None

            # INTENT: TOP
            if any(k in query for k in ["top", "highest", "most"]):
                return get_top_scorers(), "High", None

            # INTENT: BOWLER
            if any(k in query for k in ["wicket", "bowler"]):
                if data_ok:
                    for b in deliveries['bowler'].unique():
                        if any(part in query for part in b.lower().split() if len(part) > 2):
                            confidence = "High" if b.lower() in query else "Medium"
                            return get_bowling_stats(b), confidence, None
                return None, None, "Data not loaded."

            # INTENT: MATCH
            if any(k in query for k in ["vs", "predict", "win"]):
                if data_ok:
                    teams_all = set(matches['team1']) | set(matches['team2'])
                    teams_sorted = sorted(teams_all, key=len, reverse=True)
                    team_names = [t for t in teams_sorted if t.lower() in query]
                    if len(team_names) >= 2:
                        return predict_match(team_names[0], team_names[1]), "High", None
                    elif len(team_names) == 1:
                        return get_team_wins(team_names[0]), "Medium", None

            # 6. SAFE FALLBACK
            return None, "Low", "I couldn't understand that clearly. Try asking about player stats, team performance, or top records."

        # ── Client & Chat Setup ──────────────────────────────────────────────
        client = genai.Client(api_key=API_KEY)

        config = types.GenerateContentConfig(
            tools=[get_player_stats, predict_match, get_top_scorers, get_team_wins, get_bowling_stats],
            system_instruction="""
            You are CricketIQ — sharp, expert cricket analyst.
            Use tools for real data. Keep answers short and punchy.
            Use cricket emojis. Be confident.
            Never over-explain.
            """
        )

        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "chat" not in st.session_state:
            st.session_state.chat = client.chats.create(model="gemini-2.0-flash", config=config)


        # ── AI Assistant Card ────────────────────────────────────────────
        is_empty = len(st.session_state.messages) == 0
        
        if is_empty:
            st.markdown("""
            <style>
            .chat-card {
                background: var(--card) !important;
                border: 1px solid var(--border-light) !important;
                border-bottom: none !important;
                border-bottom-left-radius: 0 !important;
                border-bottom-right-radius: 0 !important;
                margin-bottom: 0 !important;
                padding-bottom: 0.5rem !important;
                box-shadow: 0 -4px 24px rgba(0,0,0,.02) !important;
            }
            .stChatInput > div {
                border-top-left-radius: 0 !important;
                border-top-right-radius: 0 !important;
                border-top: none !important;
                margin-top: -1px !important;
                box-shadow: 0 8px 24px rgba(0,0,0,.05) !important;
            }
            </style>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="chat-card">
            <p class="chat-card-title">🤖 AI Assistant</p>
            <p class="chat-card-subtitle">Ask anything about IPL history, players, and records (2008 - 2020)</p>
        </div>
        """, unsafe_allow_html=True)

        chat_container = st.container()
        
        with chat_container:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

        if "quick" in st.session_state:
            question = st.session_state.pop("quick")
        else:
            question = st.chat_input("Ask about players, teams, records...")

        if question:
            with chat_container:
                st.session_state.messages.append({"role": "user", "content": question})
                with st.chat_message("user"):    st.write(question)
                with st.chat_message("assistant"):
                    with st.spinner("🧠 CricketIQ is analyzing..."):
                        raw_data, confidence, direct_response = route_intent(question)
                        
                        if direct_response:
                            final_text = direct_response
                        else:
                            formatting_prompt = f"""Format this IPL data into a clean response with:
* title
* bullet stats
* one short insight

DATA:
{raw_data}"""
                            try:
                                r = st.session_state.chat.send_message(formatting_prompt)
                                final_text = r.text.strip()
                            except Exception:
                                final_text = raw_data
                        
                        st.write(final_text)
                        st.session_state.messages.append({"role": "assistant", "content": final_text})

# ═══════════════════════════════════════════════════════
# TAB 2 — MATCH PREDICTOR
# ═══════════════════════════════════════════════════════
with tab2:
    st.markdown("<p class='section-label'>Select Teams</p>", unsafe_allow_html=True)

    if not data_ok:
        st.error("Load matches.csv to use this feature.")
    else:
        teams_all_sorted = sorted(set(matches['team1']) | set(matches['team2']))
        teams_active_sorted = sorted([t for t in teams_all_sorted if t in ACTIVE_TEAMS])

        show_historical = st.toggle("🕰️ Include historical teams", value=False)
        team_list = teams_all_sorted if show_historical else teams_active_sorted

        c1, c2 = st.columns(2)
        with c1:
            team1 = st.selectbox("Team 1", team_list, index=0)
        with c2:
            team2 = st.selectbox("Team 2", team_list, index=min(1, len(team_list)-1))

        st.markdown("")
        predict_btn = st.button("🔮  Analyze Historical Win Probability", use_container_width=True)

        if predict_btn:
            if team1 == team2:
                st.warning("Select two different teams.")
            else:
                t1_wins = matches[matches['winner'] == team1].shape[0]
                t2_wins = matches[matches['winner'] == team2].shape[0]
                total   = max(t1_wins + t2_wins, 1)
                p1 = round((t1_wins / total) * 100, 1)
                p2 = round((t2_wins / total) * 100, 1)
                winner = team1 if t1_wins >= t2_wins else team2

                st.markdown("---")

                # Confidence: how decisive the historical gap is (50% = coin flip → 0% confidence, 100% = dominant → 100%)
                confidence = round(abs(p1 - p2), 1)
                h2h_total = matches[
                    ((matches['team1']==team1)&(matches['team2']==team2))|
                    ((matches['team1']==team2)&(matches['team2']==team1))
                ].shape[0]
                loser = team2 if winner == team1 else team1
                winner_pct = p1 if winner == team1 else p2
                loser_pct  = p2 if winner == team1 else p1

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

                # Progress bar with team labels
                st.markdown(f"""
                <div style='display:flex;justify-content:space-between;margin-top:.6rem;margin-bottom:.2rem;'>
                    <span style='font-size:.7rem;font-weight:600;color:{"#4361ee" if winner==team1 else "#8892a8"};'>{team1} {p1}%</span>
                    <span style='font-size:.7rem;font-weight:600;color:{"#4361ee" if winner==team2 else "#8892a8"};'>{p2}% {team2}</span>
                </div>
                """, unsafe_allow_html=True)
                st.progress(int(p1))

                # Head to head chart
                h2h_df = pd.DataFrame({
                    'Team':  [team1, team2],
                    'Wins':  [t1_wins, t2_wins],
                    'Color': ['#4361ee', '#c7d0e0']
                })
                fig = px.bar(
                    h2h_df, x='Team', y='Wins', text='Wins',
                    color='Team',
                    color_discrete_map={team1: '#4361ee', team2: '#c7d0e0'},
                    title='Head-to-Head Wins'
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter', color='#5a6178'),
                    showlegend=False,
                    margin=dict(t=50, b=20, l=10, r=30),
                    xaxis=dict(gridcolor='#eef0f4', showgrid=False),
                    yaxis=dict(gridcolor='#eef0f4'),
                    title_font=dict(size=13, color='#8892a8')
                )
                fig.update_traces(textfont_color='#ffffff')
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ═══════════════════════════════════════════════════════
# TAB 3 — PLAYER STATS
# ═══════════════════════════════════════════════════════
with tab3:
    if not data_ok:
        st.error("Load deliveries.csv to use this feature.")
    else:
        st.markdown("<p class='section-label'>Search Player</p>", unsafe_allow_html=True)

        all_players = sorted(deliveries['batsman'].unique().tolist())
        player = st.selectbox("Select player", all_players,
                              label_visibility="collapsed")

        if player:
            bat = deliveries[deliveries['batsman'] == player]
            runs_per_match = bat.groupby('match_id')['batsman_runs'].sum()

            r1, r2, r3, r4 = st.columns(4)
            r1.metric("🔥 Total Runs",   int(bat['batsman_runs'].sum()))
            r2.metric("🏏 Matches",      bat['match_id'].nunique())
            r3.metric("📊 Average",      round(bat['batsman_runs'].sum() / max(bat['match_id'].nunique(),1), 1))
            r4.metric("🏅 Highest",      int(runs_per_match.max()))

            st.markdown("---")

            c_a, c_b = st.columns(2)

            with c_a:
                st.markdown("<p class='section-label'>Runs Per Match</p>", unsafe_allow_html=True)
                rpm_df = runs_per_match.reset_index()
                rpm_df.columns = ['match_id','runs']
                fig2 = px.line(rpm_df, x='match_id', y='runs', title='Match-by-Match Performance')
                fig2.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter', color='#5a6178'),
                    margin=dict(t=50,b=20,l=10,r=30),
                    xaxis=dict(gridcolor='#eef0f4', title='', showgrid=False),
                    yaxis=dict(gridcolor='#eef0f4', title='Runs'),
                    title_font=dict(size=13, color='#8892a8')
                )
                fig2.update_traces(line_color='#4361ee', line_width=1.5)
                st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

            with c_b:
                st.markdown("<p class='section-label'>Dismissal Types</p>", unsafe_allow_html=True)
                dismissals = deliveries[
                    (deliveries['player_dismissed'] == player) &
                    (deliveries['dismissal_kind'].notna())
                ]['dismissal_kind'].value_counts().reset_index()
                dismissals.columns = ['Type','Count']
                if not dismissals.empty:
                    fig3 = px.pie(dismissals, names='Type', values='Count',
                                  color_discrete_sequence=['#4361ee','#7b8cff','#a5b4fc','#c7d0e0','#dde1e7'],
                                  title='How They Got Out')
                    fig3.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='Inter', color='#5a6178'),
                        margin=dict(t=40,b=20,l=10,r=10),
                        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5, font=dict(color='#6b7489')),
                        title_font=dict(size=13, color='#8892a8')
                    )
                    st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.caption("No dismissal data.")

# ═══════════════════════════════════════════════════════
# TAB 4 — LEADERBOARDS
# ═══════════════════════════════════════════════════════
with tab4:
    if not data_ok:
        st.error("Load CSV files to use this feature.")
    else:
        l1, l2 = st.columns(2)

        with l1:
            st.markdown("<p class='section-label'>🏏 Top 10 Run Scorers</p>", unsafe_allow_html=True)
            top_bat = (deliveries.groupby('batsman')['batsman_runs']
                                 .sum()
                                 .sort_values(ascending=False)
                                 .head(10)
                                 .reset_index())
            top_bat.columns = ['Player','Runs']
            top_bat['Runs'] = top_bat['Runs'].astype(int)
            top_bat.index = top_bat.index + 1

            fig4 = px.bar(top_bat, x='Runs', y='Player',
                          orientation='h', text='Runs',
                          title='All-Time Run Leaders')
            fig4.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='#5a6178'),
                margin=dict(t=50,b=20,l=10,r=30),
                yaxis=dict(autorange='reversed', gridcolor='#eef0f4', title=''),
                xaxis=dict(gridcolor='#eef0f4', title='', showgrid=False),
                title_font=dict(size=13, color='#8892a8')
            )
            fig4.update_traces(marker_color='#4361ee', textfont_color='#ffffff')
            st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})

        with l2:
            st.markdown("<p class='section-label'>🏆 Team Win Count</p>", unsafe_allow_html=True)
            team_wins = (matches['winner'].value_counts()
                                         .head(10)
                                         .reset_index())
            team_wins.columns = ['Team','Wins']
            team_wins.index = team_wins.index + 1

            fig5 = px.bar(team_wins, x='Wins', y='Team',
                          orientation='h', text='Wins',
                          title='Most Successful Teams')
            fig5.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='#5a6178'),
                margin=dict(t=50,b=20,l=10,r=30),
                yaxis=dict(autorange='reversed', gridcolor='#eef0f4', title=''),
                xaxis=dict(gridcolor='#eef0f4', title='', showgrid=False),
                title_font=dict(size=13, color='#8892a8')
            )
            fig5.update_traces(marker_color='#eef0ff',
                               marker_line_color='#4361ee',
                               marker_line_width=1,
                               textfont_color='#4361ee')
            st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar': False})

        st.markdown("---")

        st.markdown("<p class='section-label'>📈 Season-wise Match Count</p>", unsafe_allow_html=True)
        season_df = (matches.groupby('season')
                            .agg(Matches=('id','count'))
                            .reset_index())
        fig6 = px.line(season_df, x='season', y='Matches',
                       markers=True, title='Matches Per Season')
        fig6.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', color='#5a6178'),
            margin=dict(t=50,b=20,l=10,r=30),
            xaxis=dict(gridcolor='#eef0f4', title='Season', showgrid=False),
            yaxis=dict(gridcolor='#eef0f4', title='Matches'),
            title_font=dict(size=13, color='#8892a8')
        )
        fig6.update_traces(line_color='#4361ee',
                           marker_color='#4361ee',
                           line_width=2)
        st.plotly_chart(fig6, use_container_width=True, config={'displayModeBar': False})

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown('<div class="ciq-footer">Built with CricketIQ Intelligence Engine</div>', unsafe_allow_html=True)
