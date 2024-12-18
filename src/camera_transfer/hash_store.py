import sqlite3
from pathlib import Path
from typing import Optional, Iterator
from dataclasses import dataclass, field
from contextlib import contextmanager


@dataclass
class HashStore:
    database_file: Optional[Path] = None
    dry_run: bool = False
    connection: sqlite3.Connection = field(init=False)

    def __post_init__(self) -> None:
        db_file_name = str(self.database_file) if self.database_file else ":memory:"
        if self.database_file:
            self.database_file.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(db_file_name)
        self.connection.row_factory = sqlite3.Row
        self._initialize_table()

    def _initialize_table(self) -> None:
        with self.connection:
            self.connection.execute(
                "CREATE TABLE IF NOT EXISTS hash_store (hash TEXT UNIQUE, image_file TEXT)"
            )

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        try:
            yield self.connection
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise

    def __setitem__(self, hash_value: str, image_file: str) -> None:
        if not self.dry_run:
            with self.transaction():
                self.connection.execute("INSERT OR REPLACE INTO hash_store VALUES (?, ?)", (hash_value, image_file))

    def __contains__(self, hash_value: str) -> bool:
        cursor = self.connection.execute("SELECT 1 FROM hash_store WHERE hash=?", (hash_value,))
        return cursor.fetchone() is not None

    def __getitem__(self, hash_value: str) -> Optional[str]:
        cursor = self.connection.execute("SELECT image_file FROM hash_store WHERE hash=?", (hash_value,))
        row = cursor.fetchone()
        return row["image_file"] if row else None

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "HashStore":
        return self

    def __exit__(self, exc_type: Optional[type], exc_value: Optional[BaseException], traceback: Optional[object]) -> None:
        self.close()