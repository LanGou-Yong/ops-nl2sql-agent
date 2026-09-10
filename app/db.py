# -*- coding: utf-8 -*-
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "ops.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
  id INTEGER PRIMARY KEY,
  day TEXT,
  category TEXT,
  amount REAL,
  warehouse TEXT
);
CREATE TABLE IF NOT EXISTS refunds (
  id INTEGER PRIMARY KEY,
  day TEXT,
  category TEXT,
  amount REAL,
  reason TEXT
);
"""


def connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = connect()
    conn.executescript(SCHEMA)
    if conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0:
        orders = []
        refunds = []
        cats = ["耳机", "键盘", "杯子"]
        for i, day in enumerate(["2026-09-01", "2026-09-02", "2026-09-03", "2026-09-04", "2026-09-05"]):
            for c in cats:
                orders.append((None, day, c, 1000 + i * 50, "华南仓" if i % 2 == 0 else "华东仓"))
                if c == "杯子" or i == 4:
                    refunds.append((None, day, c, 80 + i * 10, "破损" if c == "杯子" else "不喜欢"))
        conn.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", orders)
        conn.executemany("INSERT INTO refunds VALUES (?,?,?,?,?)", refunds)
    conn.commit()
    conn.close()
