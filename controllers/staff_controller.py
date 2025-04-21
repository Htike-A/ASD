# controllers/staff_controller.py
import tkinter as tk
from views.staff_view import StaffView

class StaffController:
    def __init__(self, master, app_manager, data):
        self.master = master
        self.app     = app_manager
        self.data    = data            # set by app_manager on show
        self.view    = StaffView(master, self)

    def show(self):
        self.view.welcome_lbl.config(text=f"Welcome, {self.data['UserName']}")
        self.view.pack(fill="both", expand=True)

    def hide(self):
        self.view.pack_forget()

    def view_listings(self):
        self.app.show_frame("MainMenuController")

    def cancel_booking(self, booking_ref):
        ok = self.model.cancel_booking(booking_ref)
        msg = "Cancelled" if ok else "Failed to cancel"
        self.view.status_lbl.config(text=msg, fg="green" if ok else "red")
