import sqlite3
from decimal import Decimal
#conn = sqlite3.connect("essai.db")
with sqlite3.connect("essai.db") as conn:
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        nom   TEXT    NOT NULL,
        pays  TEXT    NOT NULL
    )
""")
    cur.execute("""
    INSERT INTO clients (
        nom, 
        pays
    ) VALUES (?, ?)
""",("Omar", "Egypte"))
    cur.execute("""
    INSERT INTO clients (
        nom, 
        pays
    ) VALUES (?, ?)
""",("www", "Egypte"))
    cur.execute("""
    INSERT INTO clients (
        nom, 
        pays
    ) VALUES (?, ?)
""",("bibo", "Egypte"))
    cur.executemany("""
    INSERT INTO clients (
        nom, 
        pays
    ) VALUES (?, ?)
""",[("mou", "Egypte"),("youssef", "Egypte"),("abdo", "Egypte")])
    cur.row_factory = sqlite3.Row
    for row in cur.execute("SELECT pays, COUNT(*) AS n FROM clients GROUP BY pays"):
        print(f" {row['pays']} : {row['n']}")


    conn.commit()
conn.close()