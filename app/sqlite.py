import sqlite3


class SQLiteDB:
    def __init__(self, dbfile: str):
        self.db_conn = sqlite3.connect(dbfile)
        self.db_cur = self.db_conn.cursor()

    def create_table_if_not_exists(self):
        self.db_cur.execute("create table if not exists hashes (hash varchar)")

    def get_completed_hashes_from_db(self) -> list:
        completed_hashes_cur = self.db_cur.execute("select hash from hashes")
        completed_hashes = completed_hashes_cur.fetchall()
        completed_hashes = [x[0] for x in completed_hashes]
        return completed_hashes

    def insert_hash(self, t_hash: str):
        self.db_cur.execute(f"insert into hashes (hash) VALUES (\"{t_hash}\")")

    def close(self):
        self.db_conn.commit()
        self.db_cur.close()
        self.db_conn.close()
