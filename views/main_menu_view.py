import tkinter as tk
from tkinter import ttk

class MainMenuView(tk.Frame):
	def __init__(self, master, controller):
		super().__init__(master)
		self.controller = controller


		self.label = tk.Label(self, text="Welcome")
		self.label.pack()

		self.selected_city = tk.StringVar(value="Bristol")
		self.selected_day = tk.StringVar(value="Monday")

		self.create_dropdown()
		self.create_day_buttons()
		self.create_movie_list_area()
		self.update_movie_list()

	def create_dropdown(self):
		frame = tk.Frame(self)
		frame.pack(pady=10)
		tk.Label(frame, text="Select City:").pack(side="left", padx=5)
		city_options = ttk.Combobox(frame, textvariable=self.selected_city, values=self.controller.get_location())
		city_options.pack(side="left")
		city_options.bind("<<ComboboxSelected>>", lambda e: self.update_movie_list())

	def create_day_buttons(self):
		days_frame = tk.Frame(self)
		days_frame.pack(side="top", fill="x", pady=10)

		for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
			btn = tk.Button(
				days_frame,
				text=day[:3],
				command=lambda d=day: self.select_day(d),
				width=6
			)
			btn.pack(side="left", padx=2)

	def create_movie_list_area(self):
		container = tk.Frame(self)
		container.pack(pady=10, fill="both", expand=True)

		# Create canvas and scrollbar
		canvas = tk.Canvas(container)
		scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
		canvas.configure(yscrollcommand=scrollbar.set)

		scrollbar.pack(side="right", fill="y")
		canvas.pack(side="left", fill="both", expand=True)

		# Create a frame inside the canvas
		self.movie_frame = tk.Frame(canvas)
		canvas.create_window((0, 0), window=self.movie_frame, anchor="nw")

		# Update scrollregion when content changes
		def on_configure(event):
			canvas.configure(scrollregion=canvas.bbox("all"))

		self.movie_frame.bind("<Configure>", on_configure)

    # Scroll with mousewheel
		def on_mousewheel(event):
			canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
		
		canvas.bind_all("<MouseWheel>", on_mousewheel)


	def select_day(self, day):
		self.selected_day.set(day)
		self.update_movie_list()


	def update_movie_list(self):
		# Clear current area
		for widget in self.movie_frame.winfo_children():
			widget.destroy()

		city = self.selected_city.get()
		day = self.selected_day.get()
		movies = self.controller.get_movies(city, day)
		
		if not movies:
			tk.Label(self.movie_frame, text=f"No movies for today.").pack()
			return

		for movie in movies:
			frame = tk.Frame(self.movie_frame, bd=1, relief="solid", padx=10, pady=5)
			frame.pack(padx=10, pady=5, fill="x")

			tk.Label(frame, text=movie[0], font=("Arial", 14, "bold")).pack(anchor="w") 
			tk.Label(frame, text=movie[4], font=("Arial", 12)).pack(anchor="w")          
			tk.Label(frame, text=movie[1], font=("Arial", 12)).pack(anchor="w")        
			tk.Label(frame, text="Screen: " + movie[-3], font=("Arial", 12)).pack(anchor="w")
			tk.Label(frame, text="Showtime: " + movie[6], font=("Arial", 12)).pack(anchor="w")

			book_button = tk.Button(
				frame,
				text="Book Now",
				command=lambda m=movie: self.proceed_to_booking(m),
				bg="black",
				activebackground="green",
				fg="blue",
				font=("Arial", 12),
				padx=10,
				pady=5
			)
			book_button.pack(anchor="w", pady=5)

	def proceed_to_booking(self, movie):
		print("Proceeding to book:", movie[0], "at", movie[6], "on", movie[7])

