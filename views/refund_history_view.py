#author - Win Moe Aung


import tkinter as tk
from tkinter import ttk
import sqlite3

class RefundHistoryView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Refund History")
        self.geometry("800x400")
        self.setup_ui()
        self.load_refund_history()

    def setup_ui(self):
        columns = ("id", "booking_id", "datetime", "fee")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        self.tree.heading("id", text="Cancellation ID")
        self.tree.heading("booking_id", text="Booking ID")
        self.tree.heading("datetime", text="Cancellation Time")
        self.tree.heading("fee", text="Cancellation Fee (£)")

        self.tree.column("id", width=100)
        self.tree.column("booking_id", width=100)
        self.tree.column("datetime", width=300)
        self.tree.column("fee", width=120)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        close_btn = tk.Button(self, text="Close", command=self.destroy)
        close_btn.pack(pady=10)

    def load_refund_history(self):
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect("movies.db")
        cur = conn.cursor()

        query = """
            SELECT id, booking_id, cancellation_DateTime, cancellation_fee
            FROM cancellation
            ORDER BY cancellation_DateTime DESC
        """

        for row in cur.execute(query):
            self.tree.insert("", tk.END, values=row)

        conn.close()
