import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime, date

class CancelSeatsPopup(tk.Toplevel):
    def __init__(self, master, booking_id, reload_callback):
        super().__init__(master)
        self.title("Cancel Seats")
        self.booking_id = booking_id
        self.reload_callback = reload_callback
        self.seat_vars = {}

        if not self.validate_show_date():
            return

        self.setup_ui()
        self.load_seats()

    def validate_show_date(self):
        conn = sqlite3.connect("movies.db")
        cur = conn.cursor()
        cur.execute("""
            SELECT s.show_day
            FROM bookings b
            JOIN shows s ON b.show_id = s.id
            WHERE b.id = ?
        """, (self.booking_id,))
        row = cur.fetchone()
        conn.close()

        if not row or not row[0]:
            messagebox.showerror("Error", "Show date not found.", parent=self)
            self.destroy()
            return False

        try:
            show_date = datetime.strptime(row[0], "%Y-%m-%d").date()
            today = date.today()

            if today >= show_date:
                messagebox.showerror("Error", "Cannot cancel on or after the show date.", parent=self)
                self.destroy()
                return False

            return True
        except Exception as e:
            messagebox.showerror("Error", f"Invalid date format: {e}", parent=self)
            self.destroy()
            return False

    def setup_ui(self):
        tk.Label(self, text="Select seats to cancel:", font=("Arial", 12)).pack(pady=10)
        self.seat_frame = tk.Frame(self)
        self.seat_frame.pack(padx=20, pady=10)

        self.confirm_btn = tk.Button(self, text="Confirm Cancellation", command=self.confirm_cancellation)
        self.confirm_btn.pack(pady=20)

    def load_seats(self):
        conn = sqlite3.connect("movies.db")
        cur = conn.cursor()
        cur.execute("""
            SELECT se.seat_code, bs.seat_id
            FROM booking_seat bs
            JOIN seats se ON bs.seat_id = se.id
            WHERE bs.booking_id = ?
        """, (self.booking_id,))
        rows = cur.fetchall()
        conn.close()

        for seat_code, seat_id in rows:
            var = tk.IntVar()
            cb = tk.Checkbutton(self.seat_frame, text=seat_code, variable=var)
            cb.pack(anchor="w")
            self.seat_vars[seat_id] = var

    def confirm_cancellation(self):
        seats_to_cancel = [seat_id for seat_id, var in self.seat_vars.items() if var.get() == 1]

        if not seats_to_cancel:
            messagebox.showerror("Error", "Please select at least one seat to cancel.", parent=self)
            return

        conn = sqlite3.connect("movies.db")
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON")

        total_seat_price = 0
        for seat_id in seats_to_cancel:
            cur.execute("""
                SELECT s.price
                FROM shows s
                JOIN bookings b ON s.id = b.show_id
                WHERE b.id = ?
            """, (self.booking_id,))
            seat_price = cur.fetchone()
            if seat_price:
                total_seat_price += seat_price[0]

        for seat_id in seats_to_cancel:
            cur.execute("DELETE FROM booking_seat WHERE booking_id = ? AND seat_id = ?", (self.booking_id, seat_id))

        cur.execute("SELECT COUNT(*) FROM booking_seat WHERE booking_id = ?", (self.booking_id,))
        remaining_seats = cur.fetchone()[0]

        if remaining_seats == 0:
            cur.execute("UPDATE bookings SET booking_status = 'cancelled' WHERE id = ?", (self.booking_id,))

        cancellation_fee = total_seat_price * 0.5
        cur.execute("""
            INSERT INTO cancellation (cancellation_fee, booking_id)
            VALUES (?, ?)
        """, (cancellation_fee, self.booking_id))

        conn.commit()
        conn.close()

        refund_amount = total_seat_price * 0.5
        messagebox.showinfo("Success", f"Selected seats cancelled.\nRefund Amount: £{refund_amount:.2f}", parent=self)
        self.reload_callback()
        self.destroy()
