import sqlite3
from typing import Optional

class Storage:
    def __init__(self, db_path: str = "text_analyzer.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS analysis_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save_text(self, text: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM analysis_history")
            conn.execute("INSERT INTO analysis_history (text) VALUES (?)", (text,))
            conn.commit()

    def get_last_text(self) -> Optional[str]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT text FROM analysis_history ORDER BY timestamp DESC LIMIT 1")
            result = cursor.fetchone()
            return result[0] if result else None