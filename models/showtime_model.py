# models/showtime_model.py
from models.database import get_connection

class ShowtimeModel:
    def update_showtime(self, show_id, new_date, new_time, new_price):
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("""
            UPDATE shows
               SET show_date = ?, show_time = ?, price = ?
             WHERE id = ?
        """, (new_date, new_time, new_price, show_id))
        conn.commit()
        conn.close()
