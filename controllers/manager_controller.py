# controllers/manager_controller.py
from controllers.admin_controller import AdminController
from views.manager_view import ManagerView
from models.cinema_model import CinemaModel
from models.user_model   import UserModel

class ManagerController(AdminController):
    def __init__(self, master, app, data):
        super().__init__(master, app, data)
        self.cinema_model = CinemaModel()
        self.user_model   = UserModel()
        self.view         = ManagerView(master, self)

    def create_cinema(self, name, city, capacity):
        cid = self.cinema_model.create_cinema(name, city)
        self.cinema_model.create_screen(cid, capacity)
        self.view.status_lbl.config(text="Cinema created.", fg="green")

    def add_user(self, data):
        self.user_model.create_user(**data)
        self.view.status_lbl.config(text="User added.", fg="green")
