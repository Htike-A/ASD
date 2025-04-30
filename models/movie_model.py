from models.database import get_connection
import uuid

class MovieModel:	
	def get_location(self):
		self.conn = get_connection()
		self.cur = self.conn.cursor()
		self.cur.execute("SELECT city from cinemas")
		result = self.cur.fetchall()
		self.close_conn()
		return result
	def close_conn(self):
		self.conn.close()
	def get_movies(self, loc, date):
		self.conn = get_connection()
		self.cur = self.conn.cursor()
		query = """
		SELECT 
			f.film_name, 
			f.film_disc, 
			f.film_age, 
			f.film_rating, 
			f.film_cast, 
			f.duration,
			s.id,
			s.show_time,
			s.show_date,
			s.price,
			sc.id,
			sc.screen_name,
			c.cinema_name,
			c.city
		FROM shows s
		JOIN screens sc ON s.screen_id = sc.id
		JOIN cinemas c ON sc.cinema_id = c.id
		JOIN films f ON s.film_id = f.id
		WHERE c.city = ? AND s.show_date = ?
		ORDER BY s.show_time;
		"""
		self.cur.execute(query, (loc, date))
		result = self.cur.fetchall()

		return result

	def get_seats(self, show_id):
		conn = get_connection()
		cur = conn.cursor()

		query = """
		SELECT s.*
		FROM seats s
		JOIN shows sh ON s.screen_id = sh.screen_id
		WHERE sh.id = ?
		"""

		cur.execute(query, (show_id,))
		seats = cur.fetchall()
		conn.close()
		return seats

	def check_seat(self, seat_id, show_id):
		conn = get_connection()
		cur = conn.cursor()
		query = """
		SELECT 1
		FROM booking_seat bs
		JOIN bookings b ON bs.booking_id = b.id
		WHERE bs.seat_id = ?
		AND b.show_id = ?
		AND b.booking_status = 'confirmed';

		"""
		cur.execute(query, (seat_id, show_id)) 
		result = cur.fetchone() is not None  # returns True if a seat is booked, False otherwise
		cur.close()
		conn.close()
		return result
	
	def create_film(self, film_name, film_disc, film_age, film_rating, film_cast, duration):
		conn = get_connection()
		cur  = conn.cursor()
		cur.execute("""
            INSERT INTO films
              (film_name, film_disc, film_age, film_rating, film_cast, duration)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (film_name, film_disc, film_age, film_rating, film_cast, duration))
		conn.commit()
		fid = cur.lastrowid
		conn.close()
		return fid

	def delete_film(self, film_name, duration):
		conn = get_connection()
		cur  = conn.cursor()
		cur.execute("""
            DELETE FROM films
             WHERE film_name = ?
               AND duration  = ?
        """, (film_name, duration))
		conn.commit()
		conn.close()

	def list_all(self):
		conn = get_connection()
		cur  = conn.cursor()
		cur.execute("SELECT id, film_name, duration FROM films")
		rows = cur.fetchall()
		conn.close()
		return rows