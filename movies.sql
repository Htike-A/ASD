CREATE TABLE IF NOT EXISTS cinemas (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	cinema_name TEXT NOT NULL,
	city TEXT
);


CREATE TABLE IF NOT EXISTS screens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cinema_id INTEGER,
    screen_name TEXT, 
    capacity INTEGER,
    FOREIGN KEY (cinema_id) REFERENCES cinemas(id)
);


CREATE TABLE IF NOT EXISTS films (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    film_name TEXT NOT NULL,
	film_disc TEXT NOT NULL,
	film_age INTEGER,
	film_rating TEXT,
	film_cast TEXT,
    duration INTEGER
);

CREATE TABLE IF NOT EXISTS shows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    screen_id INTEGER,
    film_id INTEGER,
    show_time TEXT, 
    show_date TEXT, 
    price REAL,
    FOREIGN KEY (screen_id) REFERENCES screens(id),
    FOREIGN KEY (film_id) REFERENCES films(id)
);

CREATE TABLE IF NOT EXISTS seats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    show_id INTEGER,
    seat_code TEXT,      -- "Br_screen_5"
    section TEXT,        -- "Lower Hall" or "Upper Gallery"
    is_booked BOOLEAN DEFAULT 0,
    FOREIGN KEY (show_id) REFERENCES shows(id),
    UNIQUE(show_id, seat_code)
);
