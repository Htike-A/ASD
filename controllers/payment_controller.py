from views.payment_view import PaymentView
from models.movie_model import MovieModel

class PaymentController():
	def __init__(self, master, controller, data):
		self.master = master
		self.controller = controller
		self.data = data
		self.model = MovieModel()
		self.view = None
		
	def show(self):
		if self.view is None or not self.view.winfo_exists():
			self.view = PaymentView(self.master, self, self.data)
		else:
			self.view.deiconify()  # Re-show if it was withdrawn

	def hide(self):
		if self.view and self.view.winfo_exists():
			self.view.withdraw()

	def save_payment(self, name, email, card):
		cost = self.data["Payment"]
		user_id = self.data["UserID"]
		show_id = self.data["ShowID"]
		seat_ids = self.data["Seat_Ids"]
		booking_id = self.model.save_payment(name, email, card, cost, user_id, show_id, seat_ids)
		self.controller.update_data(BookingId = booking_id)

	def get_receipt(self):
		bookingid = self.data["BookingId"]
		data = self.model.get_booking(bookingid)
		return data