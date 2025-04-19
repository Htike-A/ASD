CREATE TABLE IF NOT EXISTS users (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    user_FirstName TEXT    NOT NULL,
    user_LastName  TEXT    NOT NULL,
    user_email     TEXT    NOT NULL UNIQUE,
    user_password  TEXT    NOT NULL,
    user_role      TEXT    NOT NULL
                 CHECK(user_role IN ('Booking Staff','Admin','Manager'))
);



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
    screen_id INTEGER,
    seat_code TEXT,
    section TEXT,        -- "Lower Hall" or "Upper Gallery"
    FOREIGN KEY (screen_id) REFERENCES screens(id),
    UNIQUE(screen_id, seat_code)
);

CREATE TABLE IF NOT EXISTS bookings (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_ref       TEXT    NOT NULL UNIQUE,
    total_cost        REAL    NOT NULL,
    booking_DateTime  TEXT    DEFAULT CURRENT_TIMESTAMP,
    booking_status    TEXT    NOT NULL
                     CHECK(booking_status IN ('confirmed','cancelled')),
    user_id          INTEGER NOT NULL,
    show_id      INTEGER NOT NULL,
    FOREIGN KEY(user_id)     REFERENCES users(id),
    FOREIGN KEY(show_id) REFERENCES shows(id)
);

CREATE TABLE IF NOT EXISTS booking_seat (
    booking_id   INTEGER NOT NULL,
    seat_id      INTEGER NOT NULL,
    PRIMARY KEY (booking_id, seat_id),
    FOREIGN KEY (booking_id) REFERENCES bookings(id),
    FOREIGN KEY (seat_id)    REFERENCES seats(id)
);



CREATE TABLE IF NOT EXISTS cancellation (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    cancellation_DateTime TEXT    DEFAULT CURRENT_TIMESTAMP,
    cancellation_fee      REAL    NOT NULL,
    booking_id            INTEGER NOT NULL,

    FOREIGN KEY(booking_id) REFERENCES bookings(id)
);