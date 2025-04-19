# models/cinema_model.py
from models.database import get_connection

class CinemaModel:
    def list_all(self):
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("SELECT id, cinema_name, city FROM cinemas")
        rows = cur.fetchall()
        conn.close()
        return rows

    def create_cinema(self, name, city):
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("INSERT INTO cinemas (cinema_name, city) VALUES (?, ?)", (name, city))
        conn.commit()
        cid = cur.lastrowid
        conn.close()
        return cid

    def update_cinema(self, cinema_id, new_name, new_city):
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("""
            UPDATE cinemas
               SET cinema_name = ?, city = ?
             WHERE id = ?
        """, (new_name, new_city, cinema_id))
        conn.commit()
        conn.close()

    def create_screen(self, cinema_id, capacity):
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("""
            INSERT INTO screens (cinema_id, screen_name, capacity)
            VALUES (?, ?, ?)
        """, (cinema_id, f"Screen {cinema_id}", capacity))
        conn.commit()
        conn.close()
