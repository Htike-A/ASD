import tkinter as tk
from views.admin_view import AdminView
from models.auth_model import AuthModel
from tkinter import simpledialog

class ManagerView(AdminView):
    def __init__(self, master, controller):
        super().__init__(master, controller)
        frm = tk.Frame(self)
        frm.pack(pady=20)
        tk.Button(frm, text="Create Cinema", command=self.open_create_cinema).pack(side="left", padx=5)
        tk.Button(frm, text="Add User",      command=self.open_add_user).pack(side="left", padx=5)

    def open_create_cinema(self):
        name = simpledialog.askstring("Cinema",  "Name:")
        city = simpledialog.askstring("Location","City:")
        cap  = simpledialog.askinteger("Cap",    "Screen cap:")
        if name and city and cap:
            self.ctrl.create_cinema(name, city, cap)

    def open_add_user(self):
        first = simpledialog.askstring("First Name", "First name:")
        last  = simpledialog.askstring("Last Name",  "Last name:")
        email = simpledialog.askstring("Email",      "Email:")
        pw    = simpledialog.askstring("Password",   "Password:")
        role  = simpledialog.askstring("Role",
                   "Role (Booking Staff / Admin / Manager):")

        if all((first, last, email, pw, role)):
            data = {
                "user_FirstName": first,
                "user_LastName":  last,
                "user_email":     email,
                "user_password":  AuthModel.hash_password(pw),
                "user_role":      role
            }
            self.ctrl.add_user(data)
