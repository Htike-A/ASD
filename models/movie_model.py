from models.database import get_connection

class MovieModel:
	
	def get_movies(self):
		self.conn = get_connection()
		self.cur = self.conn.cursor()
		self.cur.execute("SELECT * FROM films")
		result = self.cur.fetchall()
		print(result)
		self.close_conn()
		return result

			
	def get_location(self):
		self.conn = get_connection()
		self.cur = self.conn.cursor()
		self.cur.execute("SELECT city from cinemas")
		result = self.cur.fetchall()
		self.close_conn()
		return result
	def close_conn(self):
		self.conn.close()
	def get_movies(self, loc, day):
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
			s.show_time,
			s.show_date,
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
		self.cur.execute(query, (loc, day))
		result = self.cur.fetchall()

		return result

	def get_movies_location_day(self, location, day):
		#return self.dummy_data.get(location, {}).get(day, [])
		pass
