import os
from pathlib import Path
import sqlite3
from typing import List, Optional
from cli_taskmanager.model.task import Task

DB_ENV = "CLI_TASKMANAGER_DB"
DEFAULT_DB_PATH = Path.home() / ".cli_taskmanager.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

class SQLiteStorage:
    def __init__(self):
        db_path = Path(os.environ.get(DB_ENV, DEFAULT_DB_PATH))
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        with open(SCHEMA_PATH) as f:
            schema = f.read()
        self.conn.executescript(schema)
        self.conn.commit()

    def add_task(self, description: str) -> int:
        cur = self.conn.execute(
            "INSERT INTO tasks (description, done) VALUES (?, 0)", (description,)
        )
        self.conn.commit()
        return cur.lastrowid

    def mark_done(self, task_id: int):
        self.conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        self.conn.commit()

    def mark_undone(self, task_id: int):
        self.conn.execute("UPDATE tasks SET done = 0 WHERE id = ?", (task_id,))
        self.conn.commit()

    def delete_task(self, task_id: int):
        self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def clear_done(self):
        self.conn.execute("DELETE FROM tasks WHERE done = 1")
        self.conn.commit()

    def purge(self):
        self.conn.execute("DELETE FROM tasks")
        self.conn.commit()

    def update_task(self, task_id: int, description: str):
        self.conn.execute("UPDATE tasks SET description = ? WHERE id = ?", (description, task_id))
        self.conn.commit()

    def list_tasks(self, status: str = "all") -> List[Task]:
        query = "SELECT id, description, done FROM tasks"
        params = ()
        if status == "done":
            query += " WHERE done = 1"
        elif status == "todo":
            query += " WHERE done = 0"
        cur = self.conn.execute(query, params)
        return [Task(**dict(row)) for row in cur.fetchall()]

    def get_task(self, task_id: int) -> Optional[Task]:
        cur = self.conn.execute(
            "SELECT id, description, done FROM tasks WHERE id = ?", (task_id,)
        )
        row = cur.fetchone()
        return Task(**dict(row)) if row else None
