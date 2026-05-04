"""
CricketIQ — AI Chat Tab
=========================
Tab 1: AI Chat interface with Gemini integration and intent routing.
"""

import streamlit as st
import time
import os
from google import genai
from google.genai import types
from src.ai.router import route_intent
from src.analytics.batting import get_player_stats
from src.analytics.bowling import get_bowling_stats
from src.analytics.team import get_team_wins
from src.analytics.predictions import predict_match, get_top_scorers


def render_chat_tab(matches, deliveries, data_ok):
    """Render the AI Chat tab."""
    API_KEY = os.getenv("GEMINI_API_KEY", "")

    if not API_KEY:
        st.warning("⚠️ Please set your GEMINI_API_KEY in the .env file")
        return

    # Context Memory Initialization
    if "last_intent" not in st.session_state:
        st.session_state.last_intent = None
    if "last_entity" not in st.session_state:
        st.session_state.last_entity = None

    # Gemini client & chat setup
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat" not in st.session_state:
        client = genai.Client(api_key=API_KEY)

        def _get_player_stats(player_name: str) -> str:
            return get_player_stats(player_name, deliveries)

        def _predict_match(team1: str, team2: str) -> str:
            return predict_match(team1, team2, matches)

        def _get_top_scorers() -> str:
            return get_top_scorers(deliveries)

        def _get_team_wins(team_name: str) -> str:
            return get_team_wins(team_name, matches)

        def _get_bowling_stats(bowler_name: str) -> str:
            return get_bowling_stats(bowler_name, deliveries)

        config = types.GenerateContentConfig(
            tools=[_get_player_stats, _predict_match, _get_top_scorers, _get_team_wins, _get_bowling_stats],
            system_instruction="""
            You are CricketIQ — sharp, expert cricket analyst.
            Use tools for real data. Keep answers short and punchy.
            Use cricket emojis. Be confident.
            Never over-explain.
            """
        )
        st.session_state.chat = client.chats.create(model="gemini-2.0-flash", config=config)

    # AI Assistant Card
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
            with st.chat_message("user"):
                st.write(question)
            with st.chat_message("assistant"):
                with st.status("🧠 Analyzing your query...", expanded=True) as status:
                    st.write("Extracting intent and entities...")
                    time.sleep(0.6)
                    st.write("Querying IPL database (2008-2020)...")
                    time.sleep(0.5)
                    raw_data, confidence, direct_response = route_intent(question, matches, deliveries, data_ok)
                    st.write("Formatting response...")
                    time.sleep(0.4)
                    status.update(label="Analysis complete!", state="complete", expanded=False)

                if direct_response:
                    final_text = direct_response
                else:
                    formatting_prompt = f"""Format this IPL data clearly with stats and one insight

DATA:
{raw_data}"""
                    try:
                        r = st.session_state.chat.send_message(formatting_prompt)
                        final_text = r.text.strip()
                    except Exception:
                        final_text = raw_data

                    # Append Smart Suggestions
                    final_text += "\n\n**Try asking:** Top scorers | Team wins | Player comparison"

                st.write(final_text)
                st.session_state.messages.append({"role": "assistant", "content": final_text})
