#author - Hein Zarni Naing

# controllers/admin_controller.py
from controllers.staff_controller import StaffController
from views.admin_view        import AdminView
from models.movie_model       import MovieModel
from models.showtime_model   import ShowtimeModel
from models.report_model import ReportModel


class AdminController(StaffController):
    def __init__(self, master, app, data):
        super().__init__(master, app, data)
        self.film_model     = MovieModel()
        self.showtime_model = ShowtimeModel()
        self.report_model = ReportModel()
        self.view           = AdminView(master, self)

    def show(self):
        super().show()

    def add_film(self, data):
        self.film_model.create_film(**data)
        self.view.status_lbl.config(text="Film added.", fg="green")

    def remove_film(self, film_name, duration):
        self.film_model.delete_film(film_name, duration)
        self.view.status_lbl.config(text="Film removed.", fg="green")

    def add_show(self, screen_id, film_id, date, time, price): # #author - Htike Hla Aung
        self.showtime_model.add_show(screen_id, film_id, date, time, price)
        self.view.status_lbl.config(text="Showtime updated.", fg="green")

    def update_showtime(self, show_id, screen_id, film_id, date, time, price): #author - Htike Hla Aung
        self.showtime_model.update_showtime(show_id, film_id, screen_id, date, time, price)
        self.view.status_lbl.config(text="Showtime updated.", fg="green")

    def open_admin_report(self):
        self.view.status_lbl.config(text="Report view not yet implemented", fg="blue")
