import sqlite3

conn = sqlite3.connect("movies.db")
cur = conn.cursor()

cur.execute('''
SELECT 1 
			FROM bookings
			WHERE show_id = ? AND seat_id = ?
			LIMIT 1

''', (8, 1))
res = cur.fetchone() is not None
print(res)
conn.commit()
conn.close()
