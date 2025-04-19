import tkinter as tk

class AdminView():
	def __init__(self):
		pass# views/admin_view.py
import tkinter as tk
from tkinter import simpledialog
from views.staff_view import StaffView

class AdminView(StaffView):
    def __init__(self, master, controller):
        # correctly initialize StaffView
        super().__init__(master, controller)

        # now add your extra Admin buttons below the StaffView layout:
        frm = tk.Frame(self)
        frm.pack(pady=20)
        tk.Button(frm, text="Add Film",        command=self.open_add_film).pack(side="left", padx=5)
        tk.Button(frm, text="Update Showtime", command=self.open_update_show).pack(side="left", padx=5)

    def open_add_film(self):
        data = {
            "title":       simpledialog.askstring("Title",       "Film title:"),
            "description": simpledialog.askstring("Desc",        "Description:"),
            "genre":       simpledialog.askstring("Genre",       "Genre:"),
            "age_rating":  simpledialog.askstring("Age",         "Age rating:"),
            "actors":      simpledialog.askstring("Actors",      "Actors:"),
            "duration":    simpledialog.askinteger("Duration",   "Duration (min):")
        }
        if all(data.values()):
            self.ctrl.add_film(data)

    def open_update_show(self):
        sid   = simpledialog.askinteger("Show ID", "Which show ID?")
        date  = simpledialog.askstring("Date",    "New date (YYYY-MM-DD):")
        time  = simpledialog.askstring("Time",    "New time (HH:MM):")
        price = simpledialog.askfloat( "Price",   "New price:")
        if sid and date and time and price is not None:
            self.ctrl.update_showtime(sid, date, time, price)
