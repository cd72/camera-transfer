import sqlite3
from pathlib import Path
from typing import Optional


class HashStore:
    def __init__(self, database_file: Optional[Path] = None, dry_run: bool = False) -> None:
        database_file_name = str(database_file) if database_file else ":memory:"
        if database_file:
            database_file.parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(database_file_name)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS hash_store (hash TEXT UNIQUE, image_file TEXT)"
        )
        self.dry_run = dry_run

    def __setitem__(self, hash: bytes, file_item: str) -> None:
        if not self.dry_run:
            with self.conn:
                self.conn.execute("INSERT OR REPLACE INTO hash_store VALUES (?, ?)", (hash, file_item))

    def __contains__(self, hash: bytes) -> bool:
        cursor = self.conn.execute("SELECT image_file FROM hash_store WHERE hash=?", (hash,))
        return cursor.fetchone() is not None
    