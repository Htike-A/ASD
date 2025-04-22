# controllers/admin_controller.py
from controllers.staff_controller import StaffController
from views.admin_view import AdminView
from models.movie_model     import MovieModel

class AdminController(StaffController):
    def __init__(self, master, app, data):
        super().__init__(master, app, data)
        self.Movie_model     = MovieModel()
        self.view           = AdminView(master, self)

    def show(self):
        super().show()

    def add_film(self, data):
        self.film_model.create_film(**data)
        self.view.status_lbl.config(text="Film added.", fg="green")

    def update_showtime(self, show_id, date, time, price):
        self.showtime_model.update_showtime(show_id, date, time, price)
        self.view.status_lbl.config(text="Showtime updated.", fg="green")
