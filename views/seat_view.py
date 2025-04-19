import tkinter as tk
from tkinter import messagebox

class SeatView(tk.Toplevel):
	def __init__(self, master, controller, seats_data, show_id, movie):
		super().__init__(master)
		self.title("Select Your Seat")
		self.controller = controller
		self.seats_data = seats_data
		self.show_id = show_id
		self.selected_seats = []
		self.movie = movie
		self.draw_seats()
		self.draw_payment_button()

	def draw_seats(self):
		seat_frame = tk.Frame(self)
		seat_frame.pack(padx=20, pady=20)
		row = 0
		col = 0
		
		# Dictionary to store buttons by seat code
		self.seat_buttons = {}

		for seat_id, screen_id, seat_code, section in self.seats_data:
			is_booked = self.controller.check_seat(seat_id, seat_code, self.show_id)
			color = "green" if not is_booked else "red"
			state = "normal" if not is_booked else "disabled"

			btn = tk.Button(
				seat_frame,
				text=seat_code,
				fg=color,
				state=state,
				width=5,
				command=lambda sc=seat_code: self.toggle_selection(sc)
			)
			
			# Store the button in the dictionary
			self.seat_buttons[seat_code] = btn

			btn.grid(row=row, column=col, padx=5, pady=5)

			col += 1
			if col == 10:  # new row after 10 seats
				col = 0
				row += 1


	def toggle_selection(self, seat_code):
    # Get the button from the dictionary
		btn = self.seat_buttons[seat_code]
		
		# Initialize selected_seats if it doesn't exist
		if not hasattr(self, 'selected_seats'):
			self.selected_seats = []
		
		# Toggle selection and update selected_seats list
		if btn['fg'] == 'green':
			btn['fg'] = 'blue'  # Selected
			if seat_code not in self.selected_seats:
				self.selected_seats.append(seat_code)
		elif btn['fg'] == 'blue':
			btn['fg'] = 'green'  # Unselected
			if seat_code in self.selected_seats:
				self.selected_seats.remove(seat_code)

	def get_selected_seats(self):
		return self.selected_seats
	
	def draw_payment_button(self):
		btn_frame = tk.Frame(self)
		btn_frame.pack(padx=20, pady=20)
		btn = tk.Button(btn_frame, text="Proceed to Payment", fg="blue", command=lambda m=self.movie, s = self.selected_seats : self.proceed_to_payment(m, s))
		btn.pack()

	def proceed_to_payment(self, movie, selected_seats):
		if selected_seats:
			self.controller.open_payment_view(movie, selected_seats)
		else:
			messagebox.showerror("Error", "Please select seats!")


		
