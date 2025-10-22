import sqlite3

conn = sqlite3.connect("progress.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM progress")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()