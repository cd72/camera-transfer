import sqlite3
from pathlib import Path


class HashStore():
    def __init__(self, database_file: Path | None, dry_run: bool = False) -> None:
        if database_file is None:
            database_file_name = ""
        else:
            database_file.parent.mkdir(parents=True, exist_ok=True)
            database_file_name = str(database_file)

        self.conn = sqlite3.connect(database_file_name)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS hash_store (hash text unique, image_file text)"
        )
        self.dry_run = dry_run

    def __setitem__(self, hash: bytes, file_item: str) -> None:
        if not self.dry_run:
            self.conn.execute("INSERT OR REPLACE INTO hash_store VALUES (?, ?)", (hash, file_item))
            self.conn.commit()

    
    def __contains__(self, hash:bytes) -> bool:
        cursor = self.conn.execute("SELECT image_file FROM hash_store WHERE hash=?", (hash,))
        row = cursor.fetchone()
        return row is not None

    