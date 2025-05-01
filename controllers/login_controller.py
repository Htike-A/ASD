#author - Hein Zarni Naing

# controllers/login_controller.py
import tkinter as tk
from tkinter import messagebox
from views.login_view import LoginView
from models.auth_model import AuthModel

class LoginController:
    def __init__(self, master, app_manager, data):
        self.master = master
        self.app     = app_manager
        self.model   = AuthModel()
        self.data = data
        self.view    = LoginView(master, self)


    def show(self):
        self.view.pack(fill="both", expand=True)

    def hide(self):
        self.view.pack_forget()

    def attempt_login(self):
        email    = self.view.email_var.get().strip()
        password = self.view.pw_var.get()
        user     = self.model.login(email, password)

        if not user:
            self.view.error_lbl.config(text="Invalid credentials")
            return
        
        self.view.error_lbl.config(text="")
        self.hide()
        role = user["userRole"]
        self.app.update_data(UserID=user["userId"], UserName=user["userName"], UserRole=role)
        print(self.app.data)
        if role == "Booking Staff":
            self.app.show_frame("StaffController")
        elif role == "Admin":
            self.app.show_frame("AdminController")
        elif role == "Manager":
            self.app.show_frame("ManagerController")
        else:
            messagebox.showerror("Login", f"Unknown role: {role}")
            
    def logout(self):
        self.app.show_frame("LoginController")
        self.view.clear()
