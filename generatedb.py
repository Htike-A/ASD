import sqlite3
import random

# Connect to the database
conn = sqlite3.connect("movies.db")
cur = conn.cursor()

# --- Data ---
cities = ["Bristol", "Birmingham", "Cardiff", "London"]
films = [
    ("Interstellar", "A team of explorers travel through a wormhole in space.", 13, "PG-13", "Matthew McConaughey, Anne Hathaway", 169),
    ("Inception", "A thief who steals corporate secrets through dream-sharing.", 13, "PG-13", "Leonardo DiCaprio, Joseph Gordon-Levitt", 148),
    ("The Matrix", "A hacker learns about the true nature of his reality.", 16, "R", "Keanu Reeves, Laurence Fishburne", 136),
    ("Spirited Away", "A girl enters a world of spirits and must find her way back.", 10, "PG", "Rumi Hiiragi, Miyu Irino", 125),
    ("The Dark Knight", "Batman faces the Joker, a criminal mastermind.", 14, "PG-13", "Christian Bale, Heath Ledger", 152)
]

show_times = ["9:00 AM", "12:00 PM", "3:00 PM", "6:00 PM", "9:00 PM"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# --- Insert Films ---
cur.executemany("""
INSERT INTO films (film_name, film_disc, film_age, film_rating, film_cast, duration)
VALUES (?, ?, ?, ?, ?, ?)
""", films)

# --- Insert Cinemas & Screens ---
cinema_ids = []

for city in cities:
    cur.execute("INSERT INTO cinemas (cinema_name, city) VALUES (?, ?)", (city, city))
    cinema_id = cur.lastrowid
    cinema_ids.append(cinema_id)

    num_screens = random.randint(4, 6)
    for i in range(num_screens):
        screen_name = f"{city[:2]}_Screen_{i+1}"
        capacity = random.randint(60, 120)
        cur.execute("INSERT INTO screens (cinema_id, screen_name, capacity) VALUES (?, ?, ?)", (cinema_id, screen_name, capacity))

# --- Insert Shows ---
cur.execute("SELECT id FROM screens")
screen_ids = [row[0] for row in cur.fetchall()]

cur.execute("SELECT id FROM films")
film_ids = [row[0] for row in cur.fetchall()]

show_id_counter = 1
for screen_id in screen_ids:
    num_shows = random.randint(1, 3)
    selected_times = random.sample(show_times, num_shows)
    for time in selected_times:
        film_id = random.choice(film_ids)
        day = random.choice(days)
        price = random.choice([6.0, 7.5, 9.0])
        cur.execute("""
            INSERT INTO shows (screen_id, film_id, show_time, show_date, price)
            VALUES (?, ?, ?, ?, ?)
        """, (screen_id, film_id, time, day, price))
        show_id = cur.lastrowid

        # --- Insert Seats ---
        lower_seats = [f"LA{n}" for n in range(1, random.randint(20, 40))]
        upper_seats = [f"UB{n}" for n in range(1, random.randint(20, 40))]

        for seat in lower_seats:
            cur.execute("INSERT INTO seats (show_id, seat_code, section, is_booked) VALUES (?, ?, ?, ?)", (show_id, seat, "Lower Hall", 0))
        for seat in upper_seats:
            cur.execute("INSERT INTO seats (show_id, seat_code, section, is_booked) VALUES (?, ?, ?, ?)", (show_id, seat, "Upper Gallery", 0))

# --- Finalize ---
conn.commit()
conn.close()

print("Database populated successfully.")
