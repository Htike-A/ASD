# views/manager_view.py
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from views.admin_view import AdminView
from models.auth_model import AuthModel
from collections import defaultdict

class ManagerView(AdminView):
    def __init__(self, master, controller):
        super().__init__(master, controller)

        # ---- cinema button bar ----
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Create Cinema",
                  command=self.open_cinema_dialog).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Remove Cinema",
                  command=self.open_remove_cinema_dialog).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Search Cinemas",
                  command=self.open_search_cinemas_dialog).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Manage Cinemas",
                  command=self.open_manage_cinema_dialog).pack(side="left", padx=5)

        # ---- user management button bar ----
        user_btn_frame = tk.Frame(self)
        user_btn_frame.pack(pady=20)

        tk.Button(user_btn_frame, text="Add User",
                  command=self.open_user_dialog).pack(side="left", padx=5)
        tk.Button(user_btn_frame, text="List Users",
                  command=self.open_list_users_dialog).pack(side="left", padx=5)
        tk.Button(user_btn_frame, text="Remove User",
                  command=self.open_remove_user_dialog).pack(side="left", padx=5)

        # status area
        self.status_lbl = tk.Label(self, text="", fg="green", font=("Arial", 11))
        self.status_lbl.pack(pady=(10,0))


    # --------------------
    # 1) CREATE CINEMA
    # --------------------
    def open_cinema_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title("Create Cinema")
        dlg.transient(self); dlg.grab_set()

        # Step 1: basic info + #screens
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

        capacities = []  # will hold IntVar per screen

        def show_capacity_fields():
            try:
                n = int(num_var.get())
            except ValueError:
                messagebox.showerror("Error","Invalid number of screens")
                return
            if n < 1:
                messagebox.showerror("Error","Must be at least one screen")
                return

            # clear old widgets
            for w in dlg.grid_slaves():
                if int(w.grid_info()["row"]) <= 3:
                    w.grid_forget()

            # build a capacity entry for each screen
            for i in range(n):
                row = 3 + i
                tk.Label(dlg, text=f"Screen {i+1} Capacity:").grid(row=row, column=0, sticky="e")
                cv = tk.IntVar(value=60)
                tk.Entry(dlg, textvariable=cv).grid(row=row, column=1, pady=2)
                capacities.append(cv)

            # Save & Cancel
            btn_frame = tk.Frame(dlg)
            btn_frame.grid(row=3+n, column=0, columnspan=2, pady=10)

            def save_all():
                cinema_name = name_var.get().strip()
                cinema_city = city_var.get().strip()
                # build screens list
                screens = []
                prefix = (cinema_name[:2] or cinema_name).capitalize()
                for idx, cv in enumerate(capacities, start=1):
                    cap = cv.get()
                    if cap < 1:
                        messagebox.showerror("Error",f"Invalid capacity for screen {idx}")
                        return
                    screen_name = f"{prefix}_screen_{idx}"
                    screens.append({"name": screen_name, "capacity": cap})

                if not cinema_name or not cinema_city:
                    messagebox.showerror("Error","Name & city required")
                    return

                # call into controller
                self.ctrl.create_cinema(cinema_name, cinema_city, screens)
                dlg.destroy()

            tk.Button(btn_frame, text="Save",   command=save_all).pack(side="left", padx=5)
            tk.Button(btn_frame, text="Cancel", command=dlg.destroy).pack(side="left", padx=5)

        next_btn.config(command=show_capacity_fields)


    # --------------------
    # 2) REMOVE CINEMA
    # --------------------
    def open_remove_cinema_dialog(self):
        rows = self.ctrl.list_cinemas()
        if not rows:
            messagebox.showinfo("Remove Cinema", "No cinemas defined yet.")
            return

        dlg = tk.Toplevel(self)
        dlg.title("Remove Cinema")
        dlg.transient(self); dlg.grab_set()

        choices = [f"{name} ({city})" for (_id,name,city,_,_,_) in rows]
        id_map  = {choices[i]: rows[i][0] for i in range(len(rows))}

        tk.Label(dlg, text="Select Cinema:").grid(row=0, column=0, sticky="e")
        sel_var = tk.StringVar(value=choices[0])
        ttk.Combobox(dlg, values=choices, textvariable=sel_var, state="readonly")\
           .grid(row=0, column=1, padx=5, pady=5)

        def do_remove():
            display = sel_var.get()
            cid = id_map[display]
            if messagebox.askyesno("Confirm", f"Are you sure you want to remove {display}?"):
                self.ctrl.remove_cinema(cid)
                dlg.destroy()

        btns = tk.Frame(dlg)
        btns.grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(btns, text="Delete",  command=do_remove).pack(side="left", padx=5)
        tk.Button(btns, text="Cancel",  command=dlg.destroy).pack(side="left", padx=5)


    # --------------------
    # 3) SEARCH CINEMAS
    # --------------------
    def open_search_cinemas_dialog(self):
        rows = self.ctrl.list_cinemas()
        if not rows:
            messagebox.showinfo("Search Cinemas", "No cinemas defined yet.")
            return

        dlg = tk.Toplevel(self)
        dlg.title("All Cinemas")
        dlg.transient(self); dlg.grab_set()

        tree = ttk.Treeview(dlg,
                            columns=("city","screens","capacity","seats"),
                            show="headings")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        tree.heading("city",     text="City")
        tree.heading("screens",  text="# Screens")
        tree.heading("capacity", text="Total Cap.")
        tree.heading("seats",    text="# Seats")

        for cid, name, city, num_s, cap, seats in rows:
            tree.insert("", "end",
                        text=name,
                        values=(city, num_s, cap, seats))


    # --------------------
    # 4) MANAGE CINEMAS (UPDATE)
    # --------------------
    def open_manage_cinema_dialog(self):
        cinemas = self.ctrl.cinema_model.list_all()
        if not cinemas:
            self.status_lbl.config(text="No cinemas to manage", fg="red")
            return

        dlg = tk.Toplevel(self); dlg.title("Update Cinema")
        dlg.transient(self); dlg.grab_set()

        choices = [f"{name} ({city})" for (_id,name,city) in cinemas]
        id_map  = {choices[i]: cinemas[i][0] for i in range(len(cinemas))}

        tk.Label(dlg, text="Select Cinema:").grid(row=0, column=0, sticky="e")
        sel_var = tk.StringVar(value=choices[0])
        combo = ttk.Combobox(dlg, values=choices, textvariable=sel_var, state="readonly")
        combo.grid(row=0, column=1)

        tk.Label(dlg, text="New Name:").grid(row=1, column=0, sticky="e")
        name_var = tk.StringVar()
        tk.Entry(dlg, textvariable=name_var).grid(row=1, column=1)

        tk.Label(dlg, text="New City:").grid(row=2, column=0, sticky="e")
        city_var = tk.StringVar()
        tk.Entry(dlg, textvariable=city_var).grid(row=2, column=1)

        def on_select(evt=None):
            sel = sel_var.get()
            cid, nm, ct = next((i,n,c) for (i,n,c) in cinemas if f"{n} ({c})"==sel)
            name_var.set(nm); city_var.set(ct)
        combo.bind("<<ComboboxSelected>>", on_select)
        on_select()

        def save_update():
            sel = sel_var.get()
            cid = id_map[sel]
            nm = name_var.get().strip(); ct = city_var.get().strip()
            if nm and ct:
                self.ctrl.cinema_model.update_cinema(cid, nm, ct)
                self.status_lbl.config(text="Cinema updated.", fg="green")
                dlg.destroy()

        btns = tk.Frame(dlg)
        btns.grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(btns, text="Save",   command=save_update).pack(side="left", padx=5)
        tk.Button(btns, text="Cancel", command=dlg.destroy).pack(side="left", padx=5)


    # --------------------
    # 5) ADD USER
    # --------------------
    def open_user_dialog(self):
        dlg = tk.Toplevel(self); dlg.title("Add User")
        dlg.transient(self); dlg.grab_set()

        fields = [("First Name:",0),("Last Name:",1),
                  ("Email:",2),("Password:",3),("Role:",4)]
        vars   = []
        for label, row in fields:
            tk.Label(dlg, text=label).grid(row=row, column=0, sticky="e", pady=5)
            v = tk.StringVar()
            ent = tk.Entry(dlg, textvariable=v)
            if label=="Password:":
                ent.config(show="●")
            ent.grid(row=row, column=1, pady=5)
            vars.append(v)
        fn_var, ln_var, email_var, pw_var, role_var = vars

        btns = tk.Frame(dlg)
        btns.grid(row=5, column=0, columnspan=2, pady=10)

        def on_save_user():
            fn, ln, em, pw, role = [v.get().strip() for v in vars]
            if not (fn and ln and em and pw and role):
                messagebox.showerror("Error","All fields required.")
                return
            hashed = AuthModel.hash_password(pw)
            self.ctrl.add_user({
                "user_FirstName": fn,
                "user_LastName":  ln,
                "user_email":     em,
                "user_password":  hashed,
                "user_role":      role
            })
            dlg.destroy()

        tk.Button(btns, text="Save",   command=on_save_user).pack(side="left", padx=5)
        tk.Button(btns, text="Cancel", command=dlg.destroy).pack(side="left", padx=5)
        
    def open_list_users_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title("List Users")

        rows = self.ctrl.list_users()
        columns = ("ID", "First Name", "Last Name", "Email", "Role")
        tree = ttk.Treeview(dlg, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        for row in rows:
            tree.insert("", "end", values=row)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Button(dlg, text="Close", command=dlg.destroy).pack(pady=5)


    # --------------------
    # 7) REMOVE USER
    # --------------------
    def open_remove_user_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title("Remove User")

        tk.Label(dlg, text="Email:").grid(row=0, column=0, sticky="e")
        email_var = tk.StringVar()
        tk.Entry(dlg, textvariable=email_var).grid(row=0, column=1, pady=2)

        tk.Label(dlg, text="Role:").grid(row=1, column=0, sticky="e")
        role_var = tk.StringVar()
        tk.Entry(dlg, textvariable=role_var).grid(row=1, column=1, pady=2)

        def on_remove_user():
            em = email_var.get().strip()
            rl = role_var.get().strip()
            if not em or not rl:
                messagebox.showerror("Error", "Both fields required.")
                return
            self.ctrl.remove_user(em, rl)
            dlg.destroy()

        btns = tk.Frame(dlg)
        btns.grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(btns, text="Remove", command=on_remove_user).pack(side="left", padx=5)
        tk.Button(btns, text="Cancel", command=dlg.destroy).pack(side="left", padx=5)