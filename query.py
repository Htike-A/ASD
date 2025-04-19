import sqlite3
import hashlib

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()
conn = sqlite3.connect("movies.db")
cur = conn.cursor()

PW = hash_pw("123")

cur.execute("""
INSERT INTO users 
  (user_FirstName,user_LastName, user_email, user_password, user_role) 
VALUES (?, ?, ?, ?, ?)
""", ('asdf', 'asdf', 'asdf', PW, 'Manager'))


conn.commit()
conn.close()
