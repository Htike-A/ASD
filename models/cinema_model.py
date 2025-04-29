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
    
    def delete_cinema(self, cinema_id: int):
        """
        Delete a cinema *and* all of its screens and seats.
        """
        conn = get_connection()
        cur  = conn.cursor()

        # 1) Delete all seats on any screens belonging to this cinema
        cur.execute("""
            DELETE FROM seats
             WHERE screen_id IN (
                 SELECT id FROM screens WHERE cinema_id = ?
             )
        """, (cinema_id,))

        # 2) Delete all screens for this cinema
        cur.execute("DELETE FROM screens WHERE cinema_id = ?", (cinema_id,))

        # 3) Finally delete the cinema itself
        cur.execute("DELETE FROM cinemas WHERE id = ?", (cinema_id,))

        conn.commit()
        conn.close()

    def list_all_details(self):
        """
        Returns a list of:
          (cinema_id, cinema_name, city, num_screens, total_capacity, total_seats)
        """
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("""
            SELECT
              c.id,
              c.cinema_name,
              c.city,
              COUNT(DISTINCT sc.id)        AS num_screens,
              COALESCE(SUM(sc.capacity),0) AS total_capacity,
              COUNT(s.id)                  AS total_seats
            FROM cinemas c
            LEFT JOIN screens sc 
              ON sc.cinema_id = c.id
            LEFT JOIN seats s
              ON s.screen_id = sc.id
            GROUP BY c.id, c.cinema_name, c.city
            ORDER BY c.cinema_name
        """)
        rows = cur.fetchall()
        conn.close()
        return rows
