import sqlite3


class HashStore():
    def __init__(self, filename: str) -> None:
        self.conn = sqlite3.connect(filename)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS hash_store (hash text unique, image_file text)"
        )

    def __setitem__(self, hash: bytes, file_item: str) -> None:
        self.conn.execute("INSERT OR REPLACE INTO hash_store VALUES (?, ?)", (hash, file_item))
        self.conn.commit()

    
    def __contains__(self, hash:bytes) -> bool:
        cursor = self.conn.execute("SELECT image_file FROM hash_store WHERE hash=?", (hash,))
        row = cursor.fetchone()
        if row is None:
            return False
        return True
    