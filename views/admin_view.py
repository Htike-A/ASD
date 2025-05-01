#StudentName-Hein Zarni Naing
#StudentID-23005535

import tkinter as tk
from views.staff_view import StaffView

class AdminView(StaffView):
    def __init__(self, master, controller):
        super().__init__(master, controller)

        # Button bar for all admin actions
        frm = tk.Frame(self)
        frm.pack(pady=20)
        tk.Button(frm, text="Add Film",           command=self.open_add_film_form).pack(side="left", padx=5)
        tk.Button(frm, text="Add Show",    command=self.open_add_show_form).pack(side="left", padx=5)
        tk.Button(frm, text="Update Showtime",    command=self.open_update_show_form).pack(side="left", padx=5)
        tk.Button(frm, text="Remove Film",        command=self.open_remove_film_form).pack(side="left", padx=5)
        tk.Button(frm, text="Admin Report",       command=self.open_report).pack(side="left", padx=5)

    def open_add_film_form(self):
        dlg = tk.Toplevel(self)
        dlg.title("Add Film")
        dlg.transient(self); dlg.grab_set()

        labels = [
            ("Name:",       "film_name"),
            ("Description:","film_disc"),
            ("Age Limit:",  "film_age"),
            ("Rating:",     "film_rating"),
            ("Cast:",       "film_cast"),
            ("Duration:",   "duration"),
        ]
        vars = {}
        for i, (lbl, key) in enumerate(labels):
            tk.Label(dlg, text=lbl).grid(row=i, column=0, sticky="e", pady=2, padx=4)
            var = tk.StringVar()
            tk.Entry(dlg, textvariable=var).grid(row=i, column=1, pady=2, padx=4)
            vars[key] = var

        btns = tk.Frame(dlg)
        btns.grid(row=len(labels), column=0, columnspan=2, pady=(10,0))
        def on_save():
            try:
                data = {
                    "film_name":    vars["film_name"].get().strip(),
                    "film_disc":    vars["film_disc"].get().strip(),
                    "film_age":     int(vars["film_age"].get()),
                    "film_rating":  vars["film_rating"].get().strip(),
                    "film_cast":    vars["film_cast"].get().strip(),
                    "duration":     int(vars["duration"].get())
                }
            except ValueError:
                tk.messagebox.showerror("Error", "Age and duration must be integers")
                return
            if all(data.values()):
                self.ctrl.add_film(data)
                dlg.destroy()
            else:
                tk.messagebox.showerror("Error", "Please fill in all fields")

        tk.Button(btns, text="Save",   command=on_save).pack(side="left", padx=5)
        tk.Button(btns, text="Cancel", command=dlg.destroy).pack(side="left", padx=5)

    def open_add_show_form(self):
        dlg = tk.Toplevel(self)
        dlg.title("Update Showtime")
        dlg.transient(self); dlg.grab_set()

        fields = [
            ("Screen ID:", "scid",      tk.IntVar),
            ("Film ID:", "fid",      tk.IntVar),
            ("New Time (HH:MM):",      "time", tk.StringVar),
            ("New Date (Weekday DD/MM ):", "date", tk.StringVar),
            ("New Price:",             "price",tk.DoubleVar),
        ]
        vars = {}
        for i, (lbl, key, V) in enumerate(fields):
            tk.Label(dlg, text=lbl).grid(row=i, column=0, sticky="e", pady=2, padx=4)
            var = V()
            tk.Entry(dlg, textvariable=var).grid(row=i, column=1, pady=2, padx=4)
            vars[key] = var

        btns = tk.Frame(dlg)
        btns.grid(row=len(fields), column=0, columnspan=2, pady=(10,0))
        def on_update():
            scid   = vars["scid"].get()
            fid   = vars["fid"].get()
            date  = vars["date"].get().strip()
            time  = vars["time"].get().strip()
            price = vars["price"].get()
            if scid and fid and date and time and price is not None:
                self.ctrl.add_show(scid, fid, date, time, price)
                dlg.destroy()
            else:
                tk.messagebox.showerror("Error", "Please fill in all fields")
        tk.Button(btns, text="Save",   command=on_update).pack(side="left", padx=5)
        tk.Button(btns, text="Cancel", command=dlg.destroy).pack(side="left", padx=5)

    def open_update_show_form(self):
        dlg = tk.Toplevel(self)
        dlg.title("Update Showtime")
        dlg.transient(self); dlg.grab_set()

        fields = [
            ("Show ID:", "sid",      tk.IntVar),
            ("Screen ID:", "scid",      tk.IntVar),
            ("Film ID:", "fid",      tk.IntVar),
            ("New Time (HH:MM):",      "time", tk.StringVar),
            ("New Date (Weekday DD/MM ):", "date", tk.StringVar),
            ("New Price:",             "price",tk.DoubleVar),
        ]
        vars = {}
        for i, (lbl, key, V) in enumerate(fields):
            tk.Label(dlg, text=lbl).grid(row=i, column=0, sticky="e", pady=2, padx=4)
            var = V()
            tk.Entry(dlg, textvariable=var).grid(row=i, column=1, pady=2, padx=4)
            vars[key] = var

        btns = tk.Frame(dlg)
        btns.grid(row=len(fields), column=0, columnspan=2, pady=(10,0))
        def on_update():
            sid   = vars["sid"].get()
            scid   = vars["scid"].get()
            fid   = vars["fid"].get()
            date  = vars["date"].get().strip()
            time  = vars["time"].get().strip()
            price = vars["price"].get()
            if sid and scid and fid and date and time and price is not None:
                self.ctrl.update_showtime(sid, scid, fid, date, time, price)
                dlg.destroy()
            else:
                tk.messagebox.showerror("Error", "Please fill in all fields")
        tk.Button(btns, text="Save",   command=on_update).pack(side="left", padx=5)
        tk.Button(btns, text="Cancel", command=dlg.destroy).pack(side="left", padx=5)

    def open_remove_film_form(self):
        dlg = tk.Toplevel(self)
        dlg.title("Remove Film")
        dlg.transient(self); dlg.grab_set()

        tk.Label(dlg, text="Film Name:").grid(row=0, column=0, sticky="e", pady=2, padx=4)
        name_var = tk.StringVar()
        tk.Entry(dlg, textvariable=name_var).grid(row=0, column=1, pady=2, padx=4)

        tk.Label(dlg, text="Duration (min):").grid(row=1, column=0, sticky="e", pady=2, padx=4)
        dur_var = tk.IntVar()
        tk.Entry(dlg, textvariable=dur_var).grid(row=1, column=1, pady=2, padx=4)

        btns = tk.Frame(dlg)
        btns.grid(row=2, column=0, columnspan=2, pady=(10,0))
        def on_remove():
            name = name_var.get().strip()
            dur  = dur_var.get()
            if name and dur:
                self.ctrl.remove_film(name, dur)
                dlg.destroy()
            else:
                tk.messagebox.showerror("Error", "Please fill in both fields")
        tk.Button(btns, text="Remove", command=on_remove).pack(side="left", padx=5)
        tk.Button(btns, text="Cancel", command=dlg.destroy).pack(side="left", padx=5)

    def open_report(self):
        from views.report_view import ReportView
        ReportView(self, self.ctrl)

