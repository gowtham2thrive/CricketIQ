"""
CricketIQ — Intent Router
===========================
Rule-based intent detection and entity extraction for the AI chat system.
Uses fuzzy matching (difflib) to handle misspellings gracefully.
"""

import streamlit as st
from difflib import get_close_matches
from src.config import PLAYER_ALIASES, TEAM_ALIASES
from src.analytics.batting import get_player_stats, compare_players
from src.analytics.bowling import get_bowling_stats
from src.analytics.team import get_team_wins
from src.analytics.predictions import predict_match, get_top_scorers

# Common English words that should NEVER fuzzy-match to player/team names
_STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "shall",
    "should", "may", "might", "can", "could", "about", "above", "after",
    "again", "all", "also", "and", "any", "because", "before", "between",
    "both", "but", "by", "for", "from", "get", "give", "how", "if", "in",
    "into", "its", "just", "like", "make", "me", "most", "much", "my",
    "no", "nor", "not", "now", "of", "on", "only", "or", "other", "our",
    "out", "over", "own", "same", "she", "so", "some", "such", "than",
    "that", "their", "them", "then", "there", "these", "they", "this",
    "those", "through", "to", "too", "under", "until", "up", "very",
    "what", "when", "where", "which", "while", "who", "whom", "why",
    "with", "you", "your", "tell", "joke", "hello", "hi", "hey",
    # Cricket/query terms that aren't entities
    "stats", "stat", "runs", "run", "wins", "win", "loss", "lost",
    "batting", "bowling", "bowler", "batter", "wicket", "wickets",
    "match", "matches", "player", "team", "teams", "players",
    "top", "best", "highest", "most", "lowest", "worst", "average",
    "score", "scores", "scorer", "scorers", "compare", "comparison",
    "predict", "prediction", "versus", "against", "between",
    "history", "record", "records", "father", "meaning",
    "ipl", "cricket", "indian", "premier", "league",
    "ask", "show", "give", "find", "search", "look", "display",
}


def _fuzzy_match_alias(word: str, alias_dict: dict, cutoff: float = 0.65) -> str | None:
    """Return the best fuzzy match from alias keys for a given word."""
    if word in _STOPWORDS or len(word) < 3:
        return None
    matches = get_close_matches(word, alias_dict.keys(), n=1, cutoff=cutoff)
    return alias_dict[matches[0]] if matches else None


def _fuzzy_match_name(word: str, names: list[str], cutoff: float = 0.7) -> str | None:
    """Return the best fuzzy match from a list of full names (last-name matching)."""
    if word in _STOPWORDS or len(word) < 4:
        return None
    # Build a lookup: lowercase surname → full name (only surnames with 4+ chars)
    surname_map = {}
    for name in names:
        parts = name.lower().split()
        for part in parts:
            if len(part) >= 4 and part not in _STOPWORDS:
                surname_map[part] = name
    matches = get_close_matches(word, surname_map.keys(), n=1, cutoff=cutoff)
    return surname_map[matches[0]] if matches else None


def _fuzzy_match_team(word: str, team_names: list[str], cutoff: float = 0.65) -> str | None:
    """Fuzzy match a word against individual words in full team names."""
    if word in _STOPWORDS or len(word) < 4:
        return None
    # Build lookup: keyword → team name (e.g. "chennai" → "Chennai Super Kings")
    team_word_map = {}
    for team in team_names:
        for part in team.lower().split():
            if len(part) >= 4 and part not in _STOPWORDS:
                team_word_map[part] = team
    matches = get_close_matches(word, team_word_map.keys(), n=1, cutoff=cutoff)
    return team_word_map[matches[0]] if matches else None


def route_intent(question: str, matches, deliveries, data_ok: bool):
    """
    Analyze user query and route to the appropriate analytics function.

    Returns:
        tuple: (raw_data, confidence, direct_response)
    """
    query = question.lower().strip()
    q_words = query.split()

    # 1. OUT-OF-SCOPE HANDLING
    out_of_scope_keywords = ["who is", "father", "history of", "meaning of"]
    if any(k in query for k in out_of_scope_keywords):
        # Allow if a known player/team entity is also present (e.g. "who is kohli")
        has_entity = False
        for w in q_words:
            if w in _STOPWORDS:
                continue
            if w in PLAYER_ALIASES or w in TEAM_ALIASES:
                has_entity = True
                break
            if _fuzzy_match_alias(w, PLAYER_ALIASES):
                has_entity = True
                break
        if not has_entity:
            return None, None, (
                "🏏 That's outside my IPL analytics scope!\n\n"
                "I'm built to crunch **IPL stats from 2008–2020**. Try:\n"
                "- *\"Kohli vs Dhoni\"*\n"
                "- *\"Top scorers\"*\n"
                "- *\"CSK wins\"*"
            )

    intent = None

    # Identify intent — use WORD-LEVEL matching to avoid "ashwin" matching "win"
    if any(w in {"top", "highest", "most"} for w in q_words):
        intent = "top"
    elif any(w in {"vs", "versus", "predict", "compare"} for w in q_words):
        intent = "compare_or_team"
    elif any(w in {"wicket", "wickets", "bowler", "bowling", "economy"} for w in q_words):
        intent = "bowling"
    elif any(w in {"bat", "batting", "runs", "stats", "score"} for w in q_words):
        intent = "batting"
    elif any(w in {"win", "wins", "won", "losses", "lost"} for w in q_words):
        intent = "team_wins"
    elif "what about" in query:
        intent = st.session_state.get("last_intent")

    # Identify entities
    if data_ok:
        teams_all = set(matches["team1"]) | set(matches["team2"])
        teams_sorted = sorted(teams_all, key=len, reverse=True)
        players = list(deliveries["batsman"].unique())

        # ── Check for teams (exact alias → exact substring → fuzzy alias → fuzzy name) ──
        matched_teams = []
        # 1. Exact team alias
        for alias, full_name in TEAM_ALIASES.items():
            if alias in q_words and full_name not in matched_teams:
                matched_teams.append(full_name)
        # 2. Exact full team name in query
        for t in teams_sorted:
            if t.lower() in query and t not in matched_teams:
                matched_teams.append(t)
        # 3. Fuzzy team alias matching (e.g. "chsk" → "csk")
        if not matched_teams:
            for w in q_words:
                result = _fuzzy_match_alias(w, TEAM_ALIASES)
                if result and result not in matched_teams:
                    matched_teams.append(result)
        # 4. Fuzzy full team name word matching (e.g. "chenna" → "Chennai Super Kings")
        if not matched_teams:
            for w in q_words:
                result = _fuzzy_match_team(w, list(teams_all))
                if result and result not in matched_teams:
                    matched_teams.append(result)

        # ── Check for players (exact alias → fuzzy alias → substring → fuzzy name) ──
        matched_players = []
        # 1. Exact player alias
        for alias, full_name in PLAYER_ALIASES.items():
            if alias in q_words and full_name not in matched_players:
                matched_players.append(full_name)

        # 2. Fuzzy alias matching for misspelled names (kohili→kohli, donhi→dhoni)
        if not matched_players:
            for w in q_words:
                result = _fuzzy_match_alias(w, PLAYER_ALIASES)
                if result and result not in matched_players:
                    matched_players.append(result)

        # 3. Substring matching against dataset names (only words 4+ chars)
        if not matched_players:
            for p in players:
                parts = [part for part in p.lower().split() if len(part) >= 4 and part not in _STOPWORDS]
                if any(part in query for part in parts):
                    if p not in matched_players:
                        matched_players.append(p)

        # 4. Fuzzy matching directly against dataset player surnames
        if not matched_players:
            for w in q_words:
                result = _fuzzy_match_name(w, players)
                if result and result not in matched_players:
                    matched_players.append(result)

        # ── Assign entity with priority logic ──
        # If both teams and players matched, use context to decide
        entity = None
        entity_type = None

        if matched_teams and matched_players:
            # If intent is team-related, prefer teams
            if intent in ("team_wins", "compare_or_team") or len(matched_teams) >= 2:
                entity = matched_teams[0]
                entity_type = "team"
            else:
                entity = matched_players[0]
                entity_type = "player"
        elif matched_teams:
            entity = matched_teams[0]
            entity_type = "team"
        elif matched_players:
            entity = matched_players[0]
            entity_type = "player"
        else:
            entity = st.session_state.get("last_entity")
            if entity is not None:
                entity_type = (
                    "player" if entity in players
                    else "team" if entity in teams_all
                    else None
                )

        # ── Execute action ──

        # VS / Compare
        if "vs" in q_words or "compare" in q_words or "versus" in q_words:
            if len(matched_teams) >= 2:
                st.session_state.last_intent = "compare_or_team"
                return predict_match(matched_teams[0], matched_teams[1], matches), "High", None
            if len(matched_players) >= 2:
                st.session_state.last_intent = "batting"
                return compare_players(matched_players[0], matched_players[1], deliveries), "High", None

        # Top scorers
        if intent == "top":
            st.session_state.last_intent = "top"
            return get_top_scorers(deliveries), "High", None

        # Entity-based routing
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
    return None, "Low", (
        "🤔 I couldn't match that to any IPL player or team.\n\n"
        "**Tips:** Use names like *Kohli*, *Dhoni*, *CSK*, *MI*, or try *\"top scorers\"*."
    )
