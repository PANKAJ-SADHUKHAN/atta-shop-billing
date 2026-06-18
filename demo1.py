import sqlite3

conn = sqlite3.connect("bills.db")

rows = conn.execute(
    "SELECT * FROM bills"
).fetchall()

print(rows)