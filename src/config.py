"""
CricketIQ — Configuration & Constants
======================================
Central configuration for team mappings, player aliases, and application constants.
"""

import os
from pathlib import Path

# ── Path Configuration ───────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MATCHES_CSV = DATA_DIR / "matches.csv"
DELIVERIES_CSV = DATA_DIR / "deliveries.csv"

# ── Team Name Normalization ──────────────────────────────────────────────────
# Maps defunct/renamed franchises to their current names
TEAM_MAPPING = {
    "Deccan Chargers": "Sunrisers Hyderabad",
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Rising Pune Supergiant": "Rising Pune Supergiants",
}

# Currently active IPL franchises
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

# ── Player Aliases ───────────────────────────────────────────────────────────
# Maps common/shorthand names to dataset player identifiers
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
    "pant": "RR Pant",
}

# ── Team Aliases ─────────────────────────────────────────────────────────────
# Maps common abbreviations to full team names
TEAM_ALIASES = {
    "mi": "Mumbai Indians",
    "csk": "Chennai Super Kings",
    "rcb": "Royal Challengers Bangalore",
    "srh": "Sunrisers Hyderabad",
    "dc": "Delhi Capitals",
    "pbks": "Punjab Kings",
    "rr": "Rajasthan Royals",
    "kkr": "Kolkata Knight Riders",
    "lsg": "Lucknow Super Giants",
    "gt": "Gujarat Titans",
}
