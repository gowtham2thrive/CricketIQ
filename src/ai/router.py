"""
CricketIQ — Intent Router
===========================
Rule-based intent detection and entity extraction for the AI chat system.
"""

import streamlit as st
from src.config import PLAYER_ALIASES, TEAM_ALIASES
from src.analytics.batting import get_player_stats, compare_players
from src.analytics.bowling import get_bowling_stats
from src.analytics.team import get_team_wins
from src.analytics.predictions import predict_match, get_top_scorers


def route_intent(question: str, matches, deliveries, data_ok: bool):
    """
    Analyze user query and route to the appropriate analytics function.

    Returns:
        tuple: (raw_data, confidence, direct_response)
    """
    query = question.lower().strip()
    q_words = query.split()

    # 1. OUT-OF-SCOPE HANDLING
    if any(k in query for k in ["who is", "father", "history", "meaning"]):
        return None, None, "This is outside IPL analytics scope. Please ask about IPL stats, players, or teams."

    intent = None
    entity = None

    # Identify intent
    if any(k in query for k in ["top", "highest", "most"]):
        intent = "top"
    elif any(k in query for k in ["vs", "predict", "win", "compare"]):
        intent = "compare_or_team"
    elif any(k in query for k in ["wicket", "bowler", "bowling"]):
        intent = "bowling"
    elif any(k in query for k in ["bat", "batting", "runs", "stats"]):
        intent = "batting"
    elif "what about" in query:
        intent = st.session_state.get("last_intent")

    # Identify entities
    if data_ok:
        teams_all = set(matches["team1"]) | set(matches["team2"])
        teams_sorted = sorted(teams_all, key=len, reverse=True)

        # Check for teams
        matched_teams = []
        for alias, full_name in TEAM_ALIASES.items():
            if alias in q_words and full_name not in matched_teams:
                matched_teams.append(full_name)
        for t in teams_sorted:
            if t.lower() in query and t not in matched_teams:
                matched_teams.append(t)

        # Check for players
        players = deliveries["batsman"].unique()
        matched_players = []
        for alias, full_name in PLAYER_ALIASES.items():
            if alias in q_words and full_name not in matched_players:
                matched_players.append(full_name)

        # Substring matching if alias didn't find enough players
        if not matched_players:
            for p in players:
                if any(part in query for part in p.lower().split() if len(part) > 2):
                    if p not in matched_players:
                        matched_players.append(p)

        # Assign entity
        entity_type = None
        if matched_teams and not matched_players:
            entity = matched_teams[0]
            entity_type = "team"
        elif matched_players:
            entity = matched_players[0]
            entity_type = "player"
        else:
            entity = st.session_state.get("last_entity")
            if entity is not None:
                entity_type = "player" if entity in players else "team" if entity in teams_all else None

        # Execute action based on entity and intent
        if "vs" in query or "compare" in query:
            if len(matched_teams) >= 2:
                st.session_state.last_intent = "compare_or_team"
                return predict_match(matched_teams[0], matched_teams[1], matches), "High", None
            if len(matched_players) >= 2:
                st.session_state.last_intent = "batting"
                return compare_players(matched_players[0], matched_players[1], deliveries), "High", None

        if intent == "top":
            st.session_state.last_intent = "top"
            return get_top_scorers(deliveries), "High", None

        if entity:
            st.session_state.last_entity = entity
            if entity_type == "team":
                st.session_state.last_intent = "team"
                return get_team_wins(entity, matches), "High", None
            elif entity_type == "player":
                if intent == "bowling":
                    st.session_state.last_intent = "bowling"
                    return get_bowling_stats(entity, deliveries), "High", None
                else:
                    st.session_state.last_intent = "batting"
                    return get_player_stats(entity, deliveries), "High", None

    # SAFE FALLBACK
    return None, "Low", "I couldn't understand that clearly. Try asking about player stats, team performance, or comparisons."
