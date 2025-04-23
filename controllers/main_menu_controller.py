from views.main_menu_view import MainMenuView
from models.movie_model import MovieModel
from views.seat_view import SeatView
from views.payment_view import PaymentView

class MainMenuController:
	def __init__(self, master, app, data):
		self.master = master
		self.app = app
		self.data = data
		self.model = MovieModel()
		self.view = None

	def show(self):
		if self.view and self.view.winfo_exists():
			self.view.destroy()	
		self.view = MainMenuView(self.master, self, self.data)  


	""" def hide(self):
		if self.view and self.view.winfo_exists():
			self.view.withdraw() """
	def exit(self):
		self.app.exit_application()

	def get_location(self):
		return self.model.get_location()
	
	def get_movies(self, location, day):
		return self.model.get_movies(location, day)

	def get_seats(self, screen_id):
		return self.model.get_seats(screen_id)

	def show_seats(self, movie):
		show_id = movie[6]
		screen_id = movie[-4]
		seats = self.get_seats(screen_id)
		self.app.update_data(Movie = movie, Seats = seats, ShowID = show_id)
		self.app.show_frame("SeatController")

	def log_out(self):
		self.view.withdraw()
		self.app.show_frame("LoginController")

	def go_back():
		pass

	def go_next():
		pass
	
	
	