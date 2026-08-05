import sqlite3
from pathlib import Path


class Database:
    def __init__(self, db_path: str | Path | None = None) -> None:
        if isinstance(db_path, str):
            self.db_path = Path(db_path)
        else:
            self.db_path = (
                db_path or Path(__file__).parent.parent / "data" / "pynoto.db"
            )
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: sqlite3.Connection | None = None

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        return self._conn

    def init_db(self):
        self.conn.execute("""
             CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                priority INTEGER DEFAULT 1,
                status INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                stop_at TIMESTAMP
            )
        """)
        self.conn.commit()

    def save(self, todo):
        cur = self.conn.execute(
            "INSERT INTO todos (text, priority, status) VALUES (?, ?, ?)",
            (todo.text, todo.priority.value, todo.status),
        )

        self.conn.commit()
        todo.id = cur.lastrowid

    def list_todos(self, order_by="priority DESC, created_at ASC"):
        rows = self.conn.execute(f"SELECT * FROM todos ORDER BY {order_by}").fetchall()

        return [dict(r) for r in rows]

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
