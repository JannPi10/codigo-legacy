from __future__ import annotations
import sqlite3

class SQLiteUnitOfWork:
    """Unit of Work para SQLite.
    Uso:
        with SQLiteUnitOfWork(conn) as uow:
            # operaciones
    Si ocurre excepción -> rollback, si no -> commit.
    """
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def __enter__(self):
        self.conn.execute("BEGIN")
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        return False
