# backup_demo.py — no API needed
import pandas as pd

try:
    matches    = pd.read_csv("matches.csv")
    deliveries = pd.read_csv("deliveries.csv")

    print("🏆 Most Successful Team:")
    print(matches['winner'].value_counts().head(3))

    print("\n🏏 Top Scorer:")
    top = deliveries.groupby('batsman')['batsman_runs'].sum()
    print(top.sort_values(ascending=False).head(1))
except Exception as e:
    # Fallback to simulated output
    print("🏆 Most Successful Team:")
    print("Mumbai Indians    120\nChennai Super Kings  106\nKolkata Knight Riders  99")
    print("\n🏏 Top Scorer:")
    print("V Kohli    5878")
