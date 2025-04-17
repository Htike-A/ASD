import tkinter as tk

class SeatView(tk.Toplevel):
	def __init__(self, master, seats_data, show_id, movies):
		super().__init__(master)
		self.title("Select Your Seat")
		self.seats_data = seats_data  # List of tuples
		self.show_id = show_id
		self.selected_seats = []
		self.movies = movies
		self.draw_seats()

	def draw_seats(self):
		seat_frame = tk.Frame(self)
		seat_frame.pack(padx=20, pady=20)
		print(self.seats_data)
		row = 0
		col = 0
		for seat_id, screen_id, seat_code, section in self.seats_data:
			btn = tk.Button(
				seat_frame,
				text=seat_code,
				
				width=5,
				command=lambda sc=seat_code, b=None: self.toggle_selection(sc, b)
			)
			btn.grid(row=row, column=col, padx=5, pady=5)

			btn.config(command=lambda sc=seat_code, b=btn: self.toggle_selection(sc, b))

			col += 1
			if col == 10:  # new row after 10 seats
				col = 0
				row += 1

	def toggle_selection(self, seat_code, button):
		if seat_code in self.selected_seats:
			self.selected_seats.remove(seat_code)
			button.config(bg="green")
		else:
			self.selected_seats.append(seat_code)
			button.config(bg="blue")

	def get_selected_seats(self):
		return self.selected_seats
