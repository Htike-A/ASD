#StudentName-Win Moe Aung
#StduentID-23041896

import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime, date

class CancelSeatsPopup(tk.Toplevel):
    def __init__(self, master, booking_id, refresh_callback=None):
        super().__init__(master)
        self.title("Cancel Seats")
        self.booking_id = booking_id
        self.refresh_callback = refresh_callback
        self.selected_seats = []

        self.checkbuttons = {}
        self.load_seats()

    def load_seats(self):
        conn = sqlite3.connect("movies.db")
        cur = conn.cursor()

        query = """
            SELECT s.id, s.seat_code
            FROM booking_seat bs
            JOIN seats s ON bs.seat_id = s.id
            WHERE bs.booking_id = ?
        """
        cur.execute(query, (self.booking_id,))
        seats = cur.fetchall()
        conn.close()

        for i, (seat_id, seat_code) in enumerate(seats):
            var = tk.IntVar()
            chk = tk.Checkbutton(self, text=seat_code, variable=var)
            chk.grid(row=i, column=0, sticky="w", padx=10, pady=2)
            self.checkbuttons[seat_id] = var

        confirm_btn = tk.Button(self, text="Confirm Cancellation", command=self.confirm_cancellation)
        confirm_btn.grid(row=len(seats), column=0, pady=10)

    def confirm_cancellation(self):
        selected_ids = [sid for sid, var in self.checkbuttons.items() if var.get() == 1]
        if not selected_ids:
            messagebox.showwarning("No Selection", "Please select at least one seat to cancel.", parent=self)
            return

        conn = sqlite3.connect("movies.db")
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON")

        # Fetch show_date in format like "Wed 07/05"
        cur.execute("""
            SELECT s.show_date
            FROM bookings b
            JOIN shows s ON b.show_id = s.id
            WHERE b.id = ?
        """, (self.booking_id,))
        row = cur.fetchone()

        if not row or not row[0]:
            messagebox.showerror("Error", "Show date not found.", parent=self)
            conn.close()
            return

        try:
            show_date_str = row[0].strip()[-5:]  # Extract "07/05"
            show_date = datetime.strptime(show_date_str, "%d/%m").replace(year=date.today().year).date()
        except ValueError:
            messagebox.showerror("Error", "Invalid show date format.", parent=self)
            conn.close()
            return

        if show_date <= date.today():
            messagebox.showerror("Error", "Cannot cancel on or after the day of the show.", parent=self)
            conn.close()
            return

        cur.execute("SELECT total_cost FROM bookings WHERE id = ?", (self.booking_id,))
        total_cost = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM booking_seat WHERE booking_id = ?", (self.booking_id,))
        total_seats = cur.fetchone()[0]
        price_per_seat = total_cost / total_seats if total_seats else 0

        for sid in selected_ids:
            cur.execute("DELETE FROM booking_seat WHERE booking_id = ? AND seat_id = ?", (self.booking_id, sid))

        cur.execute("SELECT COUNT(*) FROM booking_seat WHERE booking_id = ?", (self.booking_id,))
        remaining = cur.fetchone()[0]

        if remaining == 0:
            cur.execute("UPDATE bookings SET booking_status = 'cancelled' WHERE id = ?", (self.booking_id,))

        refund_amount = price_per_seat * len(selected_ids) * 0.5
        cur.execute("INSERT INTO cancellation (cancellation_fee, booking_id) VALUES (?, ?)", (refund_amount, self.booking_id))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Selected seats cancelled.", parent=self)

        if self.refresh_callback:
            self.refresh_callback()

        self.destroy()
