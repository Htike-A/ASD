#StudentName-Hein Zarni Naing
#StudentID-23005535

# models/report_model.py
import sqlite3
from models.database import get_connection

class ReportModel:
    def bookings_per_listing(self):
        """
        Returns: list of (film_name, booking_count)
        """
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("""
            SELECT f.film_name,
                   COUNT(*) AS bookings
              FROM bookings b
              JOIN shows s   ON b.show_id = s.id
              JOIN films f   ON s.film_id     = f.id
             WHERE b.booking_status = 'confirmed'
             GROUP BY f.film_name
             ORDER BY bookings DESC;
        """)
        data = cur.fetchall()
        conn.close()
        return data

    def monthly_revenue_per_cinema(self, year_month=None):
        """
        year_month: "YYYY-MM" or None for all
        Returns: list of (cinema_name, month, revenue)
        """
        conn = get_connection()
        cur  = conn.cursor()
        base = """
            SELECT c.cinema_name,
                   strftime('%Y-%m', b.booking_DateTime) AS month,
                   SUM(b.total_cost) AS revenue
              FROM bookings b
              JOIN shows s      ON b.show_id = s.id
              JOIN screens sc   ON s.screen_id    = sc.id
              JOIN cinemas c    ON sc.cinema_id   = c.id
             WHERE b.booking_status = 'confirmed'
        """
        params = []
        if year_month:
            base += " AND strftime('%Y-%m', b.booking_DateTime) = ?"
            params.append(year_month)
        base += " GROUP BY c.cinema_name, month ORDER BY month, revenue DESC;"
        cur.execute(base, params)
        data = cur.fetchall()
        conn.close()
        return data

    def top_revenue_films(self, limit=5):
        """
        Returns the top N films by revenue.
        """
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(f"""
            SELECT f.film_name,
                   SUM(b.total_cost) AS revenue
              FROM bookings b
              JOIN shows s    ON b.show_id = s.id
              JOIN films f    ON s.film_id     = f.id
             WHERE b.booking_status = 'confirmed'
             GROUP BY f.film_name
             ORDER BY revenue DESC
             LIMIT {limit};
        """)
        data = cur.fetchall()
        conn.close()
        return data

    def staff_monthly_booking_counts(self, year_month=None):
        """
        Returns: list of (staff_name, month, bookings)
        """
        conn = get_connection()
        cur  = conn.cursor()
        base = """
            SELECT u.user_FirstName || ' ' || u.user_LastName AS staff,
                   strftime('%Y-%m', b.booking_DateTime)      AS month,
                   COUNT(*)                               AS bookings
              FROM bookings b
              JOIN users u    ON b.user_id = u.id
             WHERE u.user_role IN ('Booking Staff', 'Admin', 'Manager')

               AND b.booking_status = 'confirmed'
        """
        params = []
        if year_month:
            base += " AND month = ?"
            params.append(year_month)
        base += " GROUP BY staff, month ORDER BY month, bookings DESC;"
        cur.execute(base, params)
        data = cur.fetchall()
        conn.close()
        return data
