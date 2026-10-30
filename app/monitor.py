"""Monitoring. Every request becomes one row in a local SQLite file."""
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_DB = Path(__file__).resolve().parent.parent / "data" / "pageforge.db"


def _db_path() -> Path:
    return Path(os.getenv("PAGEFORGE_DB", DEFAULT_DB))


def _connect() -> sqlite3.Connection:
    path = _db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT, source TEXT, prompt_version TEXT, prompt_sha TEXT, model TEXT,
            user_request TEXT, success INTEGER, attempts INTEGER, latency_s REAL,
            prompt_tokens INTEGER, completion_tokens INTEGER, error TEXT
        )""")
    return conn


def log_request(**fields) -> None:
    fields.setdefault("ts", datetime.now(timezone.utc).isoformat())
    cols = ", ".join(fields)
    marks = ", ".join("?" for _ in fields)
    with _connect() as conn:
        conn.execute(f"INSERT INTO requests ({cols}) VALUES ({marks})", list(fields.values()))


def fetch_requests() -> list[dict]:
    with _connect() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM requests ORDER BY id").fetchall()
    return [dict(r) for r in rows]