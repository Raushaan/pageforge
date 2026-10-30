"""Summarise logged requests by prompt version. Run: python -m scripts.summary"""
import sqlite3

from app.monitor import DEFAULT_DB

conn = sqlite3.connect(DEFAULT_DB)
rows = conn.execute("""
    SELECT prompt_version, COUNT(*), ROUND(AVG(success) * 100),
           ROUND(AVG(latency_s), 1), ROUND(AVG(attempts), 2)
    FROM requests
    WHERE source != 'test'
    GROUP BY prompt_version
""").fetchall()

print(f"{'version':<9}{'runs':>6}{'valid %':>10}{'avg sec':>10}{'attempts':>10}")
for version, runs, valid, latency, attempts in rows:
    print(f"{version:<9}{runs:>6}{valid:>10}{latency:>10}{attempts:>10}")