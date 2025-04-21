import tkinter as tk
from tkinter import ttk
from views.admin_view import AdminView
from models.auth_model import AuthModel

class ManagerView(AdminView):
    def __init__(self, master, controller):
        super().__init__(master, controller)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Create Cinema",
                  command=self.open_cinema_dialog).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Manage Cinemas",
                  command=self.open_manage_cinema_dialog).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Add User",
                  command=self.open_user_dialog).pack(side="left", padx=5)

        self.status_lbl = tk.Label(self, text="", fg="green")
        self.status_lbl.pack(pady=(10,0))


    def open_cinema_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title("Create Cinema")
        dlg.transient(self); dlg.grab_set()

        # — Step 1: basic info + #screens —
        tk.Label(dlg, text="Cinema Name:").grid(row=0, column=0, sticky="e")
        name_var = tk.StringVar()
        tk.Entry(dlg, textvariable=name_var).grid(row=0, column=1, pady=2)

        tk.Label(dlg, text="Location:").grid(row=1, column=0, sticky="e")
        city_var = tk.StringVar()
        tk.Entry(dlg, textvariable=city_var).grid(row=1, column=1, pady=2)

        tk.Label(dlg, text="Number of Screens:").grid(row=2, column=0, sticky="e")
        num_var = tk.IntVar(value=1)
        tk.Entry(dlg, textvariable=num_var).grid(row=2, column=1, pady=2)

        next_btn = tk.Button(dlg, text="Next", width=10)
        next_btn.grid(row=3, column=0, columnspan=2, pady=10)

        capacities: list[tk.IntVar] = []

        def show_capacity_fields():
            try:
                n = int(num_var.get())
            except ValueError:
                return
            if n <= 0:
                return

            # clear rows 0–3
            for w in dlg.grid_slaves():
                if int(w.grid_info()["row"]) <= 3:
                    w.grid_forget()

            # build a capacity entry for each screen
            for i in range(n):
                row0 = 3 + i
                tk.Label(dlg, text=f"Screen {i+1} Capacity:").grid(row=row0, column=0, sticky="e")
                cv = tk.IntVar()
                tk.Entry(dlg, textvariable=cv).grid(row=row0, column=1, pady=2)
                capacities.append(cv)

            # Save & Cancel
            btn_frame = tk.Frame(dlg)
            btn_frame.grid(row=3 + n, column=0, columnspan=2, pady=10)

            def save_all():
                cinema_name = name_var.get().strip()
                cinema_city = city_var.get().strip()
                # first two letters, capitalized
                prefix = (cinema_city[:2] or cinema_city).capitalize()
                screens = []
                for idx, cv in enumerate(capacities, start=1):
                    cap = cv.get()
                    if cap > 0:
                        screen_name = f"{prefix}_screen_{idx}"
                        screens.append({"name": screen_name, "capacity": cap})
                if cinema_name and cinema_city and screens:
                    self.ctrl.create_cinema(cinema_name, cinema_city, screens)
                    dlg.destroy()

            tk.Button(btn_frame, text="Save",   command=save_all).pack(side="left", padx=5)
            tk.Button(btn_frame, text="Cancel", command=dlg.destroy).pack(side="left", padx=5)

        next_btn.config(command=show_capacity_fields)


    def open_manage_cinema_dialog(self):
        # fetch existing cinemas
        cinemas = self.ctrl.cinema_model.list_all()  
        if not cinemas:
            self.status_lbl.config(text="No cinemas to manage", fg="red")
            return

        dlg = tk.Toplevel(self); dlg.title("Update Cinema")
        dlg.transient(self); dlg.grab_set()

        # Map display string → id
        choices = [f"{name} ({city})" for (_id,name,city) in cinemas]
        id_map  = {choices[i]: cinemas[i][0] for i in range(len(cinemas))}

        tk.Label(dlg, text="Select Cinema:").grid(row=0, column=0, sticky="e")
        sel_var = tk.StringVar(value=choices[0])
        combo = ttk.Combobox(dlg, values=choices, textvariable=sel_var, state="readonly")
        combo.grid(row=0, column=1)

        # prefill form fields
        tk.Label(dlg, text="New Name:").grid(row=1, column=0, sticky="e")
        name_var = tk.StringVar()
        name_entry = tk.Entry(dlg, textvariable=name_var)
        name_entry.grid(row=1, column=1)

        tk.Label(dlg, text="New City:").grid(row=2, column=0, sticky="e")
        city_var = tk.StringVar()
        city_entry = tk.Entry(dlg, textvariable=city_var)
        city_entry.grid(row=2, column=1)

        def on_select(evt=None):
            display = sel_var.get()
            cid, nm, ct = next((id_,n,c) for (id_,n,c) in cinemas if f"{n} ({c})" == display)
            name_var.set(nm)
            city_var.set(ct)
        combo.bind("<<ComboboxSelected>>", on_select)
        on_select()

        btns = tk.Frame(dlg); btns.grid(row=3, column=0, columnspan=2, pady=10)
        def save_update():
            display = sel_var.get()
            cid = id_map[display]
            new_name, new_city = name_var.get().strip(), city_var.get().strip()
            if new_name and new_city:
                self.ctrl.cinema_model.update_cinema(cid, new_name, new_city)
                self.status_lbl.config(text="Cinema updated.", fg="green")
                dlg.destroy()
        tk.Button(btns, text="Save",   command=save_update).pack(side="left", padx=5)
        tk.Button(btns, text="Cancel", command=dlg.destroy).pack(side="left", padx=5)


    def open_user_dialog(self):
        dlg = tk.Toplevel(self); dlg.title("Add User")
        dlg.transient(self); dlg.grab_set()

        tk.Label(dlg, text="First Name:").grid(row=0, column=0, sticky="e")
        fn_var = tk.StringVar(); tk.Entry(dlg, textvariable=fn_var).grid(row=0, column=1)

        tk.Label(dlg, text="Last Name:").grid(row=1, column=0, sticky="e", pady=5)
        ln_var = tk.StringVar(); tk.Entry(dlg, textvariable=ln_var).grid(row=1, column=1)

        tk.Label(dlg, text="Email:").grid(row=2, column=0, sticky="e", pady=5)
        email_var = tk.StringVar(); tk.Entry(dlg, textvariable=email_var).grid(row=2, column=1)

        tk.Label(dlg, text="Password:").grid(row=3, column=0, sticky="e", pady=5)
        pw_var = tk.StringVar()
        tk.Entry(dlg, textvariable=pw_var, show="●").grid(row=3, column=1)

        tk.Label(dlg, text="Role:").grid(row=4, column=0, sticky="e", pady=5)
        role_var = tk.StringVar(); tk.Entry(dlg, textvariable=role_var).grid(row=4, column=1)

        btns = tk.Frame(dlg); btns.grid(row=5, column=0, columnspan=2, pady=10)
        def on_save_user():
            fn, ln, email, pw, role = (v.get().strip() for v in (fn_var,ln_var,email_var,pw_var,role_var))
            if fn and ln and email and pw and role:
                hashed = AuthModel.hash_password(pw)
                self.ctrl.add_user({
                    "user_FirstName": fn,
                    "user_LastName":  ln,
                    "user_email":     email,
                    "user_password":  hashed,
                    "user_role":      role
                })
                self.status_lbl.config(text="User added.", fg="green")
                dlg.destroy()
        tk.Button(btns, text="Save",   command=on_save_user).pack(side="left", padx=5)
        tk.Button(btns, text="Cancel", command=dlg.destroy).pack(side="left", padx=5)
