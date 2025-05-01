#author - Win Moe Aung


import tkinter as tk
from tkinter import ttk, messagebox

class ReportView(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.title("Admin Reports")
        self.controller   = controller
        self.model        = controller.report_model

        opts = [
            "Bookings per Listing",
            "Monthly Revenue per Cinema",
            "Top Revenue Films",
            "Staff Monthly Booking Counts",
        ]
        self.choice = tk.StringVar(value="Bookings per Listing")
        ttk.Combobox(self, values=opts, textvariable=self.choice, state="readonly")\
           .pack(padx=10, pady=(10,0))
        tk.Button(self, text="Run", command=self.run_report).pack(padx=10, pady=5)

        self.tree = ttk.Treeview(self, columns=("c1","c2","c3"), show="headings")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

    def run_report(self):
        kind = self.choice.get()
        for col in self.tree["columns"]:
            self.tree.heading(col, text="")
        self.tree.delete(*self.tree.get_children())

        if kind == "Bookings per Listing":
            rows = self.model.bookings_per_listing()
            self.tree["columns"] = ("film","count")
            self.tree.heading("film", text="Film")
            self.tree.heading("count", text="Bookings")

        elif kind == "Monthly Revenue per Cinema":
            rows = self.model.monthly_revenue_per_cinema()
            self.tree["columns"] = ("cinema","month","revenue")
            self.tree.heading("cinema", text="Cinema")
            self.tree.heading("month", text="Month")
            self.tree.heading("revenue", text="Revenue")

        elif kind == "Top Revenue Films":
            rows = self.model.top_revenue_films()
            self.tree["columns"] = ("film","revenue")
            self.tree.heading("film", text="Film")
            self.tree.heading("revenue", text="Revenue")

        elif kind == "Staff Monthly Booking Counts":
            rows = self.model.staff_monthly_booking_counts()
            self.tree["columns"] = ("staff","month","count")
            self.tree.heading("staff", text="Staff")
            self.tree.heading("month", text="Month")
            self.tree.heading("count", text="Bookings")

        else:
            messagebox.showerror("Error", "Please select a report")
            return

        for row in rows:
            self.tree.insert("", "end", values=row)
