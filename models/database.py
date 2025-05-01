#author - Win Moe Aung

import os
import sqlite3


def get_connection():
	return sqlite3.connect("movies.db")
