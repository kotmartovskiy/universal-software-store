import sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DB=ROOT/'store.db'
SCHEMA=ROOT/'schema.sql'
def connect():
    con=sqlite3.connect(DB)
    con.row_factory=sqlite3.Row
    con.execute('PRAGMA foreign_keys=ON')
    return con
def init_db():
    with connect() as con: con.executescript(SCHEMA.read_text(encoding='utf-8'))
if __name__=='__main__': init_db(); print(DB)
