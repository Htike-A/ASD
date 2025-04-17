import tkinter as tk


class SeatView(tk.Toplevel):
	def __init__(self, master, controller, seats_data, show_id, movies):
		super().__init__(master)
		self.title("Select Your Seat")
		self.controller = controller
		self.seats_data = seats_data
		self.show_id = show_id
		self.selected_seats = []
		self.movies = movies
		self.draw_seats()
		print(seats_data)
	def draw_seats(self):
		seat_frame = tk.Frame(self)
		seat_frame.pack(padx=20, pady=20)
		row = 0
		col = 0
		
		# Dictionary to store buttons by seat code
		self.seat_buttons = {}

		for seat_id, screen_id, seat_code, section in self.seats_data:
			# Check if the seat is booked using the controller method

			is_booked = self.controller.check_seat(seat_id, self.show_id)
			print(seat_id, seat_code,is_booked)

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
