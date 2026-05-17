import sqlite3
import os

os.makedirs("../data", exist_ok=True)

DB_PATH = "../data/results.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            prediction TEXT,
            confidence REAL,
            media_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_result(filename, prediction, confidence, media_type):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO results
        (filename, prediction, confidence, media_type)
        VALUES (?, ?, ?, ?)
        """,
        (filename, prediction, confidence, media_type)
    )

    conn.commit()
    conn.close()