# models/cinema_model.py
import math, random
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

    def create_screen_with_name(self, cinema_id: int, screen_name: str, capacity: int) -> int:
        conn = get_connection()
        cur  = conn.cursor()

        # a) insert the screen record
        cur.execute(
            "INSERT INTO screens (cinema_id, screen_name, capacity) VALUES (?, ?, ?)",
            (cinema_id, screen_name, capacity)
        )
        screen_id = cur.lastrowid

        # b) figure out how many seats of each kind
        lower_count   = math.floor(capacity * 0.3)
        upper_total   = capacity - lower_count
        vip_count     = random.randint(7, min(10, upper_total))
        regular_upper = upper_total - vip_count

        # c) insert Lower Hall seats
        for i in range(1, lower_count + 1):
            cur.execute(
                "INSERT INTO seats (screen_id, seat_code, section) VALUES (?, ?, ?)",
                (screen_id, f"LA{i}", "Lower Hall")
            )

        # d) insert VIP seats
        for i in range(1, vip_count + 1):
            cur.execute(
                "INSERT INTO seats (screen_id, seat_code, section) VALUES (?, ?, ?)",
                (screen_id, f"VIP{i}", "VIP")
            )

        # e) insert remaining Upper Gallery seats
        for i in range(1, regular_upper + 1):
            cur.execute(
                "INSERT INTO seats (screen_id, seat_code, section) VALUES (?, ?, ?)",
                (screen_id, f"UB{i}", "Upper Gallery")
            )

        conn.commit()
        conn.close()
        return screen_id
