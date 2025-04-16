import sqlite3

conn = sqlite3.connect("movies.db")
cur = conn.cursor()

cur.execute('''
SELECT name FROM sqlite_master WHERE type='table' AND name='shows';

''')

conn.commit()
conn.close()
