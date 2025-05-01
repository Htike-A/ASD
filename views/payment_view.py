#author - Win Moe Aung

import tkinter as tk
from tkinter import messagebox
import re

class PaymentView(tk.Toplevel):
    def __init__(self, master, controller, data, price_per_seat=6.00):
        super().__init__(master)
        self.controller = controller
        self.data = data
        self.selected_seats = self.data["Selected_Seats"]

        self.total_price = self.data["Payment"]

        self.title("Payment")
        self.geometry("400x500")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.go_back)
        self.create_widgets()
        
    def go_back(self):
        self.controller.go_back()
        self.destroy()

    def validate_card_input(self, new_value):
        return (new_value.isdigit() or new_value == "") and len(new_value) <= 16

    def validate_cvc_input(self, new_value):
        return (new_value.isdigit() or new_value == "") and len(new_value) <= 3

    def validate_expiry_format(self, expiry):
        # Validates MM/YY format and month between 01–12
        match = re.fullmatch(r"(0[1-9]|1[0-2])/\d{2}", expiry)
        return bool(match)

    def create_widgets(self):
        tk.Label(self, text="Payment", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self, text=f"Selected Seats: {', '.join(self.selected_seats)}").pack(pady=5)
        tk.Label(self, text=f"Total Amount: £{self.total_price:.2f}", font=("Arial", 12)).pack(pady=5)

        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Full Name").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Email").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.email_entry = tk.Entry(form_frame)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)


        tk.Label(form_frame, text="Card Number").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        vcmd_card = (self.register(self.validate_card_input), '%P')
        self.card_entry = tk.Entry(form_frame, validate='key', validatecommand=vcmd_card)
        self.card_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="CVC").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        vcmd_cvc = (self.register(self.validate_cvc_input), '%P')
        self.cvc_entry = tk.Entry(form_frame, validate='key', validatecommand=vcmd_cvc)
        self.cvc_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Expiry (MM/YY)").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        vcmd_expiry = (self.register(lambda val: len(val) <= 5), '%P')
        self.expiry_entry = tk.Entry(form_frame, validate='key', validatecommand=vcmd_expiry)
        self.expiry_entry.insert(0, "04/28")  # placeholder
        self.expiry_entry.grid(row=4, column=1, padx=5, pady=5)
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(padx=20, pady=20)
        back_btn = tk.Button(btn_frame, text="Go back", fg="black", command=self.go_back)
        back_btn.grid(row=0, column=0, padx=5, pady=5)
        confirm_btn = tk.Button(btn_frame, text="Confirm Payment", fg="black", command=self.confirm_payment)
        confirm_btn.grid(row=0, column=1, padx=5, pady=5)

    def confirm_payment(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        card = self.card_entry.get()
        last_four = card[-4:]
        cvc = self.cvc_entry.get()
        expiry = self.expiry_entry.get()

        if not name or not email or not card or not cvc or not expiry:
            messagebox.showerror("Missing Info", "Please fill in all payment details.", parent=self)
            return
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.", parent=self)
            return

        if len(card) != 16:
            messagebox.showerror("Invalid Card", "Card number must be 16 digits.", parent=self)
            return
        if len(cvc) != 3:
            messagebox.showerror("Invalid CVC", "CVC must be 3 digits.", parent=self)
            return

        if not self.validate_expiry_format(expiry):
            messagebox.showerror("Invalid Expiry", "Expiry must be in MM/YY format.", parent=self)
            return

        self.controller.save_payment(name, email, last_four)
        self.show_receipt()
        
    def show_receipt(self):
        details = self.controller.get_receipt()
        booking_ref = details[0]
        film_name = details[1]
        show_date = details[2]
        show_time = details[3]
        screen = details[4]
        num_of_tickets = details[5]
        total_cost = details[7]
        booking_date = details[8]

        receipt_text = (
        f"Booking Receipt!\n"
        f"Ref: {booking_ref}\n"
        f"Film Name: {film_name}\n"
        f"Film Date: {show_date}\n"
        f"Show time: {show_time}\n"
        f"Screen: {screen}\n"
        f"Number of tickets: {num_of_tickets}\n"
        f"Seat numbers: {', '.join(self.selected_seats)}\n"
        f"Total booking Cost: £{total_cost:.2f}\n"
        f"Booking Date: {booking_date}"
    )

        messagebox.showinfo("Payment Success", receipt_text)
        file_name = f"{booking_ref}.pdf"
        self.controller.save_pdf(file_name, receipt_text)
        self.destroy()
        self.controller.redirect()