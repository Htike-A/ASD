#StudentName-Hein Zarni Naing
#StudentID-23005535

import tkinter as tk
from tkinter import simpledialog

class StaffView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.ctrl = controller

        top = tk.Frame(self)
        top.pack(fill="x")
        self.welcome_lbl = tk.Label(top, text="Welcome,", font=("Arial", 14))
        self.welcome_lbl.pack(side="left", padx=20, pady=10)
        tk.Button(top, text="Logout", command=lambda: self.ctrl.app.show_frame("LoginController")).pack(side="right", padx=20)

        frm = tk.Frame(self)
        frm.pack(pady=30)
        tk.Button(frm, text="View Listings", width=20, command=self.ctrl.view_listings).pack(pady=5)
        tk.Button(frm, text="Bookings",width=20, command=self.ctrl.open_bookings_view).pack(pady=5)
        tk.Button(frm, text="Refund History", width=20, command=self.ctrl.open_refund_history).pack(pady=5)

        self.status_lbl = tk.Label(self, text="", font=("Arial", 12))
        self.status_lbl.pack(pady=20)
        
    def on_view_list(self):
        self.controller.on_view_list()
    

    def open_cancel_dialog(self):
        ref = simpledialog.askstring("Cancel", "Booking Ref:")
        if ref:
            self.ctrl.cancel_booking(ref)
