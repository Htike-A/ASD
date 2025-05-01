#StudentName-Win Moe Aung
#StduentID-23041896

import os
import sqlite3


def get_connection():
	return sqlite3.connect("movies.db")
