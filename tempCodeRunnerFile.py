cur.executemany("""
INSERT INTO films (film_name, film_disc, film_age, film_rating, film_cast, duration)
VALUES (?, ?, ?, ?, ?, ?)
""", films)