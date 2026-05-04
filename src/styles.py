"""
CricketIQ — Global Styles
===========================
Premium glassmorphism CSS design system for the Streamlit dashboard.
"""

GLOBAL_CSS = """
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
"""
