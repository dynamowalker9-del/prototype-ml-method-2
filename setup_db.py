import sqlite3

conn = sqlite3.connect("progress.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    topic TEXT,
    score INTEGER,
    timestamp TEXT
)
""")

conn.commit()
conn.close()