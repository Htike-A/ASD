from views.main_menu_view import MainMenuView
from models.movie_model import MovieModel
class ManinMenuController:
	def __init__(self, master, app):
		self.master = master
		self.app = app
		self.model = MovieModel()
		self.view = MainMenuView(master, self)

	def show(self):
		self.view.pack()

	def hide(self):
		self.view.pack_forget()

	def get_location(self):
		return self.model.get_location()
	def get_movies(self, location, day):
		return self.model.get_movies(location, day)


	def go_back():
		pass

	def go_next():
		pass