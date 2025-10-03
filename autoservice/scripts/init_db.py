from __future__ import annotations
import sqlite3
from autoservice.repositories.base import init_schema, with_fk

def main():
    conn = sqlite3.connect("autoservice_dev.db")
    with_fk(conn)
    init_schema(conn)
    print("DB creada: autoservice_dev.db")

if __name__ == "__main__":
    main()
