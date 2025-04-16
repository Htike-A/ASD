from tkinter import Tk
from controllers.main_menu_controller import ManinMenuController

class AppManager:
	def __init__(self, root):
		self.root = root
		self.main_menu_controller = ManinMenuController(root, self)

		self.show_main_menu()

	def show_main_menu(self):
		self.main_menu_controller.show()