# views/login_view.py
import tkinter as tk

class LoginView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, width=400, height=300)
        self.ctrl = controller
        self.pack_propagate(False)

        self.container = tk.Frame(self)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.container, text="Horizon Cinemas", font=("Arial", 16))\
            .pack(pady=(0, 20))

        tk.Label(self.container, text="Email:").pack(anchor="w")
        self.email_var   = tk.StringVar()
        self.email_entry = tk.Entry(self.container, textvariable=self.email_var, width=30)
        self.email_entry.pack()    
       
        tk.Label(self.container, text="Password:").pack(anchor="w", pady=(10, 0))
        self.pw_var    = tk.StringVar()
        self.pw_entry  = tk.Entry(self.container, textvariable=self.pw_var, show="●", width=30)
        self.pw_entry.pack()       

        self.login_btn = tk.Button(self.container, text="Login",
                                   command=self.ctrl.attempt_login)
        self.login_btn.pack(pady=15)

        self.error_lbl = tk.Label(self.container, text="", fg="red")
        self.error_lbl.pack()

        self.email_entry.bind("<Return>", lambda evt: self.ctrl.attempt_login())
        self.pw_entry  .bind("<Return>", lambda evt: self.ctrl.attempt_login())
    def clear(self):
        """Reset the two entry boxes (and clear any error text)."""
        self.email_var.set("")
        self.pw_var.set("")
        self.error_lbl.config(text="")
    
