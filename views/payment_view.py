import tkinter as tk
from tkinter import messagebox

class PaymentView(tk.Toplevel):
    def __init__(self, master, controller, movie, selected_seats, price_per_seat=6.00):
        super().__init__(master)
        self.controller = controller
        self.selected_seats = selected_seats
        self.total_price = len(selected_seats) * price_per_seat

        self.title("Payment")
        self.geometry("400x500")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Payment", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self, text=f"Selected Seats: {', '.join(self.selected_seats)}").pack(pady=5)
        tk.Label(self, text=f"Total Amount: £{self.total_price:.2f}", font=("Arial", 12)).pack(pady=5)

        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Full Name").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="email").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.email_entry = tk.Entry(form_frame)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)


        tk.Label(form_frame, text="Card Number").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.card_entry = tk.Entry(form_frame)
        self.card_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(self, text="Confirm Payment", fg="black", command=self.confirm_payment).pack(pady=15)

    def confirm_payment(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        card = self.card_entry.get()

        if not name or not email or not card:
            messagebox.showerror("Missing Info", "Please fill in all payment details.", parent=self)
            return

        # TODO: Add booking logic here (e.g., update DB)
        messagebox.showinfo("Success", f"Payment of £{self.total_price:.2f} successful!", parent=self)

        self.destroy()  # Close the payment window
