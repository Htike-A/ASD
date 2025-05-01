#StudentName-Htike Hla Aung
#StduentID-23056129

# models/showtime_model.py
from models.database import get_connection

class ShowtimeModel:
    def add_show(self, screen_id, film_id, new_date, new_time, new_price):
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("""
            INSERT INTO shows (screen_id, film_id, show_time, show_date, price) VALUES (?, ?, ?, ?, ?)
        """, (screen_id, film_id, new_time, new_date, new_price))
        conn.commit()
        conn.close()


    def update_showtime(self, show_id, screen_id, film_id, new_date, new_time, new_price):
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("""
            UPDATE shows
               SET screen_id = ?, film_id =?, show_date = ?, show_time = ?, price = ?
             WHERE id = ?
        """, (screen_id, film_id, new_date, new_time, new_price, show_id))
        conn.commit()
        conn.close()
