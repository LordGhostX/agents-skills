import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "shop.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    product TEXT NOT NULL,
    amount REAL NOT NULL,
    region TEXT NOT NULL,
    total_usd REAL
);
"""


def connect(path=DB_PATH):
    conn = sqlite3.connect(path)
    conn.executescript(SCHEMA)
    return conn
