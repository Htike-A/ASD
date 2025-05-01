import sqlite3
import random
import math
import hashlib
from datetime import date, timedelta


def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def get_time_slot(hhmm: str) -> str:
    """
    Bucket a time like '3:00 PM' correctly into morning/afternoon/evening
    by parsing the AM/PM suffix.
    """
    # Split into the clock part and the suffix
    time_part, suffix = hhmm.split()        # e.g. ("3:00", "PM")
    hour_str, _ = time_part.split(":")      # e.g. "3"
    h = int(hour_str)

    # Convert to 24h
    suffix = suffix.upper()
    if suffix == "PM" and h != 12:
        h += 12
    if suffix == "AM" and h == 12:
        h = 0

    # Now bucket
    if 8 <= h < 12:
        return "morning"
    if 12 <= h < 17:
        return "afternoon"
    return "evening"
PRICE_TABLE = {
    "Bristol":    {"morning": 6,  "afternoon": 7,  "evening": 8},
    "Birmingham": {"morning": 5,  "afternoon": 6,  "evening": 7},
    "Cardiff":    {"morning": 5,  "afternoon": 6,  "evening": 7},
    "London":     {"morning":10,  "afternoon":11,  "evening":12},
}


# Connect to the database
conn = sqlite3.connect("movies.db")
cur = conn.cursor()

users = [
    ("Staff" ,"Staff",  "staff@example.com",  hash_pw("staff123"), "Booking Staff"),
    ("Admin" , "Admin",    "admin@example.com",    hash_pw("admin123"),   "Admin"),
    ("Manager", "Manager","manager@gmail.com",    hash_pw("manager123"),"Manager")
]

cur.executemany("""
INSERT OR IGNORE INTO users 
  (user_FirstName,user_LastName, user_email, user_password, user_role) 
VALUES (?, ?, ?, ?, ?)
""", users)


PW = hash_pw("123")

cur.execute("""
INSERT INTO users 
  (user_FirstName,user_LastName, user_email, user_password, user_role) 
VALUES (?, ?, ?, ?, ?)
""", ('asdf', 'asdf', 'asdf', PW, 'Manager'))


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


days = ["Thu 01/05", "Fri 02/05", "Sat 03/05", "Sun 04/05", "Mon 05/05", "Tue 06/05", "Wed 07/05", "Thu 08/05", "Fri 09/05", "Sat 10/05", "Sun 11/05" , "Mon 12/05", "Tue 13/05", "Wed 14/05", "Thu 15/05", "Fri 16/05", "Sat 17/05", "Sun 18/05"]

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
cur.execute("""
SELECT s.id, s.capacity, c.city
  FROM screens s
  JOIN cinemas c ON s.cinema_id = c.id
""")

screens = cur.fetchall()
cur.execute("SELECT id FROM films")
film_ids = [row[0] for row in cur.fetchall()]


for screen_id, capacity, city in screens:
    for _ in range(random.randint(1, 3)):      
        show_time = random.choice(show_times)
        show_date = random.choice(days)
        film_id   = random.choice(film_ids)

        slot  = get_time_slot(show_time)
        price = PRICE_TABLE[city][slot]        
        cur.execute("""
            INSERT INTO shows (screen_id, film_id, show_time, show_date, price)
            VALUES (?, ?, ?, ?, ?)
        """, (screen_id, film_id, show_time, show_date, price))
        show_id = cur.lastrowid

        vip_cap = 10

        lower_hall_cap = math.floor(capacity * 0.3)
        upper_hall_cap = capacity - lower_hall_cap - vip_cap

        # --- Insert Seats ---
        lower_seats = [f"LH{n}" for n in range(1, lower_hall_cap + 1)]
        upper_seats = [f"UG{n}" for n in range(1, upper_hall_cap + 1)]
        vip_seats = [f"VIP{n}" for n in range(1, vip_cap + 1)]


        all_seats = [(show_id, seat, "Lower Hall") for seat in lower_seats] + \
            [(show_id, seat, "Upper Gallery") for seat in upper_seats] + \
            [(show_id, seat, "VIP") for seat in vip_seats]
        
        cur.executemany("""
    INSERT OR IGNORE INTO seats (screen_id, seat_code, section)
    VALUES (?, ?, ?)
""", all_seats)


conn.commit()
conn.close()

print("Database populated successfully.")