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

	def save_payment(self):
		self.model.save_payment()