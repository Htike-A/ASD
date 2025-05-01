#StudentName-Hein Zarni Naing
#StudentID-23005535

# controllers/staff_controller.py
import tkinter as tk
from views.staff_view import StaffView
from views.booking_view import BookingsView
from views.refund_history_view import RefundHistoryView

class StaffController:
    def __init__(self, master, app_manager, data):
        self.master = master
        self.app     = app_manager
        self.data    = data 
        self.view    = StaffView(master, self)

    def show(self):
        self.view.welcome_lbl.config(text=f"Welcome, {self.data['UserName']}")
        self.view.pack(fill="both", expand=True)

    def hide(self):
        self.view.pack_forget()

    def view_listings(self):
        self.hide()
        self.app.show_frame("MainMenuController")

    def cancel_booking(self, booking_ref):
        ok = self.model.cancel_booking(booking_ref)
        msg = "Cancelled" if ok else "Failed to cancel"
        self.view.status_lbl.config(text=msg, fg="green" if ok else "red")
    
    def open_bookings_view(self):
        BookingsView(self.master,self.app, self)

    def open_refund_history(self):
        RefundHistoryView(self.master)