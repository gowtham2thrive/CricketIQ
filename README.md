# 🏏 CricketIQ

**"AI-Powered IPL Analytics Engine"**

CricketIQ is an intelligent, data-driven dashboard that provides deep insights into historical IPL matches. Designed for cricket enthusiasts and analysts, it leverages advanced AI to deliver instant statistics, match predictions, and player performance metrics through an intuitive chat interface.

---

## 🚀 Overview

CricketIQ transforms raw IPL data into actionable intelligence. The platform features an AI chat assistant for natural language queries, a match prediction engine, a detailed player analytics dashboard, and comprehensive leaderboards. Whether you want to know the top run-scorers or the probability of a team winning, CricketIQ has you covered.

---

## ✨ Features

* 🤖 **AI Chat:** Get instant IPL insights through natural language queries.
* 📊 **Player Statistics:** View detailed metrics including runs, averages, and overall performance.
* 🔮 **Match Prediction:** Predict outcomes based on historical win probabilities and matchups.
* 🏆 **Leaderboards:** Discover top run-scorers, highest wicket-takers, and team win records.
* ⚡ **Fast & Responsive:** Real-time answers using optimized queries and Streamlit caching.
* 🎯 **Controlled AI:** Strict intent routing ensures accurate, deterministic, and hallucination-free answers.

---

## 🛠 Tech Stack

* **Python:** Core backend logic and data processing.
* **Streamlit:** Fast, interactive frontend dashboard framework.
* **Pandas:** Robust data manipulation and aggregation.
* **Plotly:** Interactive and dynamic data visualization.
* **Gemini API (Google GenAI):** Natural language processing and response formatting.

---

## 🧠 How It Works

1. **Query Input:** The user asks a question via the chat interface.
2. **Intent Detection:** The system analyzes the query to determine the intent (e.g., player stats, team stats, match prediction).
3. **Function Trigger:** The appropriate backend function is triggered based on the detected intent.
4. **Data Retrieval:** Precise data is fetched and aggregated from the historical IPL dataset.
5. **AI Formatting:** The raw data is passed to Gemini, which formats it into a clean, professional response.

---

## 📂 Dataset

* **Source:** Historical IPL dataset covering seasons from 2008 to 2019.
* **Scope:** Includes ball-by-ball delivery data and comprehensive match-level metadata.
* **Purpose:** Exclusively used for advanced analytics, insights, and historical probability models.

> **Note:** Designed for consistent historical analysis and backtesting.

---

## ⚙️ Setup & Installation

**1. Clone the repository:**
```bash
git clone https://github.com/gowtham2thrive/CricketIQ.git
cd cricketiq
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Configure Environment Variables:**
Create a `.env` file in the root directory and add your Gemini API key:
```env
GEMINI_API_KEY=your_api_key_here
```

**4. Run the application:**
```bash
streamlit run app.py
```

---

## 🎮 Usage

Here are some example queries you can ask the AI Assistant:

* "Show Virat Kohli stats"
* "Top run scorers"
* "MI vs CSK prediction"
* "Team win rate"

---

## 📁 Project Structure

```text
├── app.py              # Main Streamlit application
├── matches.csv         # Match-level historical dataset
├── deliveries.csv      # Ball-by-ball historical dataset
├── requirements.txt    # Python dependencies
└── .env                # Environment variables (API keys)
```

---

## ⚠️ Limitations

* **Historical Data Only:** Data is limited to the IPL 2008–2019 seasons.
* **Prediction Scope:** Match predictions are strictly based on historical head-to-head statistics, not real-time conditions.
* **No Live Updates:** The platform does not currently ingest real-time match data or live scores.

---

## 🚧 Future Scope

* **Real-time IPL Data Integration:** Fetching live match scores and stats via external APIs.
* **Advanced ML Models:** Transitioning from probability-based predictions to sophisticated machine learning models.
* **Player Comparison Engine:** Side-by-side analytical comparisons of player stats.
* **Full Web Application:** Scaling to a full-stack architecture (React frontend + REST API backend).
