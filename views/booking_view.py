import tkinter as tk
from tkinter import ttk
import sqlite3
from views.cancel_seats_popup import CancelSeatsPopup

class BookingsView(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.title("All Bookings")
        self.geometry("1000x600")
        self.controller = controller
        self.setup_ui()
        self.load_bookings()

    def setup_ui(self):
        filter_frame = tk.Frame(self)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Filter by Status:").pack(side=tk.LEFT, padx=5)
        self.filter_var = tk.StringVar()
        self.filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, state="readonly", width=20)
        self.filter_combo['values'] = ("All", "confirmed", "cancelled")
        self.filter_combo.current(0)
        self.filter_combo.pack(side=tk.LEFT, padx=5)
        self.filter_combo.bind("<<ComboboxSelected>>", lambda e: self.load_bookings())

        columns = ("booking_id", "reference", "user", "show", "total", "status", "seats", "count", "action")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        self.tree.heading("booking_id", text="Booking ID")
        self.tree.heading("reference", text="Reference")
        self.tree.heading("user", text="User")
        self.tree.heading("show", text="Show")
        self.tree.heading("total", text="Total Cost")
        self.tree.heading("status", text="Status")
        self.tree.heading("seats", text="Seats")
        self.tree.heading("count", text="Count")
        self.tree.heading("action", text="Action")

        self.tree.column("booking_id", width=80)
        self.tree.column("reference", width=100)
        self.tree.column("user", width=100)
        self.tree.column("show", width=200)
        self.tree.column("total", width=80)
        self.tree.column("status", width=100)
        self.tree.column("seats", width=160)
        self.tree.column("count", width=60)
        self.tree.column("action", width=80)

        self.tree.bind("<ButtonRelease-1>", self.handle_click)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        back_btn = tk.Button(self, text="Back", command=self.go_back)
        back_btn.pack(pady=10)

    def load_bookings(self):
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect("movies.db")
        cur = conn.cursor()

        base_query = """
            SELECT 
                b.id, b.booking_ref, u.user_FirstName || ' ' || u.user_LastName AS full_name,
                f.film_name || ' at ' || s.show_time AS show_info,
                b.total_cost, b.booking_status,
                COALESCE(GROUP_CONCAT(se.seat_code), ''),
                COUNT(bs.seat_id)
            FROM (
                SELECT * FROM bookings
                WHERE booking_status LIKE ?
            ) b
            JOIN users u ON b.user_id = u.id
            JOIN shows s ON b.show_id = s.id
            JOIN films f ON s.film_id = f.id
            LEFT JOIN booking_seat bs ON b.id = bs.booking_id
            LEFT JOIN seats se ON bs.seat_id = se.id
            GROUP BY b.id
            ORDER BY b.id DESC
        """

        filter_status = self.filter_var.get()
        param = "%"
        if filter_status and filter_status != "All":
            param = filter_status

        for row in cur.execute(base_query, (param,)):
            action_text = "Cancel"
            row_with_action = row + (action_text,)
            self.tree.insert("", tk.END, values=row_with_action)

        conn.close()

    def handle_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            row_id = self.tree.identify_row(event.y)
            if column == "#9":
                item = self.tree.item(row_id)
                booking_id = item["values"][0]
                self.cancel_booking(booking_id)

    def cancel_booking(self, booking_id):
        CancelSeatsPopup(self, booking_id, self.load_bookings)

    def go_back(self):
        self.destroy()
        self.controller.app.show_frame("StaffController")
