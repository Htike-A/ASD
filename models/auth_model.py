# models/auth_model.py
import sqlite3
import hashlib
from models.database import get_connection

class AuthModel:
    @staticmethod
    def hash_password(pw: str) -> str:
        return hashlib.sha256(pw.encode()).hexdigest()

    def login(self, email: str, password: str):
        hashed = self.hash_password(password)
        conn   = get_connection()
        cur    = conn.cursor()

        # match your table columns exactly
        cur.execute("""
          SELECT 
            id, 
            user_FirstName, 
            user_LastName, 
            user_password, 
            user_role
          FROM users
          WHERE user_email = ?
        """, (email,))
        row = cur.fetchone()
        conn.close()

        # debugging output
        print("=== LOGIN DEBUG ===")
        print(" Email      :", email)
        print(" Entered PW :", password)
        print(" Hashed PW  :", hashed)
        if row:
            print(" DB id           :", row[0])
            print(" DB First Name   :", row[1])
            print(" DB Last  Name   :", row[2])
            print(" DB PW hash      :", row[3])
            print(" DB user_role    :", row[4])
        else:
            print(" NO user found for that email!")
        print("===================")

        # check both existence and correct hash
        if not row or row[3] != hashed:
            return None

        # build a nice display name
        full_name = f"{row[1]} {row[2]}"
        return {
            "userId":   row[0],
            "userName": full_name,
            "userRole": row[4],
        }
