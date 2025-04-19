from models.movie_model import MovieModel
from views.seat_view import SeatView

class SeatController():
	def __init__(self, master, app, data):
		self.master = master
		self.app = app
		self.data = data
		self.model = MovieModel()
		self.view = None

	def show(self, data):
		if self.view is None or not self.view.winfo_exists():
			self.view = SeatView(self.master, self, data)
		else:
			self.view.deiconify()  # Re-show if it was withdrawn

	def hide(self):
		if self.view and self.view.winfo_exists():
			self.view.withdraw()
	
	def check_seat(self, seat_id, seat_code, show_id):
		return self.model.check_seat(seat_id, seat_code, show_id)

	def open_payment_view(self, movie, selected_seats):
		self.app.update_data(Movie = movie, Selected_Seats = selected_seats)
		self.app.show_frame("PaymentController", self.app.data)