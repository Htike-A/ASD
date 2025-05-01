#author - Hein Zarni Naing

import sqlite3
from models.database import get_connection 

class UserModel:
    def __init__(self):
        self.conn = get_connection()
        self.cur  = self.conn.cursor()

    def find_by_email(self, email):
        self.cur.execute("""
            SELECT id, user_FirstName, user_LastName,
                   user_email, user_password, user_role
              FROM users
             WHERE user_email = ?
        """, (email,))
        row = self.cur.fetchone()
        if not row:
            return None

        return {
            "userId":        row[0],
            "userFirstName": row[1],
            "userLastName":  row[2],
            "userEmail":     row[3],
            "userPassword":  row[4],
            "userRole":      row[5],
        }

    def create_user(self, user_FirstName, user_LastName,
                    user_email, user_password, user_role):
        """Insert a new user into the users table."""
        self.cur.execute("""
            INSERT INTO users
              (user_FirstName, user_LastName,
               user_email,     user_password,
               user_role)
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_FirstName,
            user_LastName,
            user_email,
            user_password,
            user_role,
        ))
        self.conn.commit()
        return self.cur.lastrowid
    def list_users(self):
        """
        Retrieve all users as a list of tuples:
        (id, first name, last name, email, role)
        """
        self.cur.execute("""
            SELECT id, user_FirstName, user_LastName, user_email, user_role
              FROM users
        """)
        return self.cur.fetchall()

    def delete_user_by_email_and_role(self, email, role):
        """
        Delete the user record matching exactly this email & role.
        Returns the number of rows deleted (0 if none).
        """
        self.cur.execute("""
            DELETE FROM users
             WHERE user_email = ? AND user_role = ?
        """, (email, role))
        self.conn.commit()
        return self.cur.rowcount