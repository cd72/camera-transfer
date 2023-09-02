import sqlite3


class HashStore(dict):
    def __init__(self, filename=None):
        self.conn = sqlite3.connect(filename)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS hash_store (hash text unique, image_file text)"
        )

    def close(self):
        self.conn.commit()
        self.conn.close()

    def __len__(self):
        rows = self.conn.execute("SELECT COUNT(*) FROM hash_store").fetchone()[0]
        return rows if rows is not None else 0

    def iterhashess(self):
        c = self.conn.cursor()
        for row in c.execute("SELECT hash FROM hash_store"):
            yield row[0]

    def iterimage_files(self):
        c = self.conn.cursor()
        for row in c.execute("SELECT image_file FROM hash_store"):
            yield row[0]

    def iteritems(self):
        c = self.conn.cursor()
        for row in c.execute("SELECT hash, image_file FROM hash_store"):
            yield row[0], row[1]

    def hashes(self):
        return list(self.iterhashes())

    def image_files(self):
        return list(self.iterimage_files())

    def items(self):
        return list(self.iteritems())

    def __contains__(self, hash):
        return (
            self.conn.execute(
                "SELECT 1 FROM hash_store WHERE hash = ?", (hash,)
            ).fetchone()
            is not None
        )

    def __getitem__(self, hash):
        item = self.conn.execute(
            "SELECT image_file FROM hash_store WHERE hash = ?", (hash,)
        ).fetchone()
        if item is None:
            raise KeyError(hash)
        return item[0]

    def __setitem__(self, hash, image_file):
        self.conn.execute(
            "REPLACE INTO hash_store (hash, image_file) VALUES (?,?)",
            (hash, image_file),
        )

    def __delitem__(self, hash):
        if hash not in self:
            raise KeyError(hash)
        self.conn.execute("DELETE FROM hash_store WHERE hash = ?", (hash,))

    def __iter__(self):
        return self.iterhashes()
