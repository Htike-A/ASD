from models.movie_model import MovieModel
from views.seat_view import SeatView

class SeatController():
	def __init__(self, master, app, data):
		self.master = master
		self.app = app
		self.data = data
		self.model = MovieModel()
		self.view = None

	def show(self):
		if self.view is None or not self.view.winfo_exists():
			self.view = SeatView(self.master, self, self.data)
		else:
			self.view.deiconify() 
	def hide(self):
		if self.view and self.view.winfo_exists():
			self.view.withdraw()
   
	def destroy(self):
		if self.view and self.view.winfo_exists():
			self.view.destroy()
	
	def check_seat(self, seat_id, show_id):
		return self.model.check_seat(seat_id, show_id)

	def open_payment_view(self, movie, selected_seats, seat_ids):
		price = movie[-5]
		total_price = 0
		for seat_code in selected_seats:
			if seat_code.startswith("LH"):
				price = price

			elif seat_code.startswith("UG"):
				price = price * 1.2

			elif seat_code.startswith("VIP"):
				price = price * 1.2 * 1.2
			else:
				print("Error")
			total_price += price


		self.app.update_data(Movie = movie, Selected_Seats = selected_seats, Payment = total_price, Seat_Ids = seat_ids)
		self.hide()
		self.app.show_frame("PaymentController")
  
	def go_back(self):
		self.app.update_data(Movie = None, Seats = None, ShowID = None)
		self.app.show_frame("MainMenuController")