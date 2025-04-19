from controllers.login_controller import LoginController
from controllers.staff_controller import StaffController
from controllers.admin_controller import AdminController
from controllers.manager_controller import ManagerController
from controllers.main_menu_controller import MainMenuController
from controllers.seat_controller import SeatController
from controllers.payment_controller import PaymentController

LOGIN = "LoginController"
STAFF = "StaffController"
ADMIN = "AdminController"
MANAGER = "ManagerController"
MAINMENU = "MainMenuController"
SEAT = "SeatController"
PAYMENT = "PaymentController"

class AppManager:
	def __init__(self, root):
		self.root = root
		self.data = {
			"UserID": None,
			"Movie": [],
			"Seat": [],
			"Payment": [],
		}
		self.frames = {}
		for C in (LoginController, StaffController, AdminController, ManagerController, MainMenuController, SeatController, PaymentController):
			controller = C(self.root, self, self.data)
			self.frames[C.__name__] = controller
		self.show_frame(LOGIN)

	def show_frame(self, name, data = None):
		# Hide all visible windows first
		self.hide_all_views()
		
		ctrl = self.frames.get(name)

		if name == LOGIN:
			ctrl.view.email_var.set("")
			ctrl.view.pw_var.set("")
			ctrl.view.error_lbl.config(text="")

		if ctrl:
			ctrl.show(data)
		else:
			print(f"No controller for {name}")

	def update_data(self, **kwargs):
		for key, value in kwargs.items():
			if key in self.data:
				self.data[key] = value
			else:
				print("Error in data passing")

	def exit_application(self):
		self.root.destroy()

	def hide_all_views(self):
		for ctrl in self.frames.values():
			if hasattr(ctrl, 'hide'):
				ctrl.hide()