#author - Hein Zarni Naing

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

    # existing:
    def create_cinema(self, name, city, screens):
        cid = self.cinema_model.create_cinema(name, city)
        for s in screens:
            self.cinema_model.create_screen_with_name(cid, s["name"], s["capacity"])
        self.view.status_lbl.config(text="Cinema + screens created", fg="green")

    # new:
    def remove_cinema(self, cinema_id):
        self.cinema_model.delete_cinema(cinema_id)
        self.view.status_lbl.config(text="Cinema removed and its associated seats and screens", fg="green")

    def list_cinemas(self):
        """
        returns list of (id, name, city, num_screens, total_capacity, total_seats)
        """
        return self.cinema_model.list_all_details()
    
    def list_users(self):
        """
        returns list of (id, firstName, lastName, email, role)
        """
        return self.user_model.list_users()
    
    def add_user(self, data):
        self.user_model.create_user(**data)
        self.view.status_lbl.config(text="User added.", fg="green")

    def remove_user(self, email, role):
        """
        Deletes a user matching email and role, updates status label.
        """
        count = self.user_model.delete_user_by_email_and_role(email, role)
        if count:
            self.view.status_lbl.config(text="User removed", fg="green")
        else:
            self.view.status_lbl.config(text="No matching user found", fg="red")

