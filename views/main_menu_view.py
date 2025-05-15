#StudentName-Htike Hla Aung
#StduentID-23056129

import tkinter as tk
from tkinter import ttk
import datetime

class MainMenuView(tk.Toplevel):
	def __init__(self, master, controller, data):
		super().__init__(master)
		self.controller = controller
		self.geometry("800x700")
		self.data = data
		user = self.data["UserName"]

		self.protocol("WM_DELETE_WINDOW", self.go_back)
  
		container = tk.Frame(self)
		container.pack(fill="x", padx=10, pady=5)

		self.label = tk.Label(container, text=f"Welcome, {user}")
		self.label.pack(side="left")

		button = tk.Button(container, text="Logout", command=self.log_out)
		button.pack(side="right")

		button = tk.Button(container, text="Go back", command=self.go_back)
		button.pack(side="right")

		self.selected_city = tk.StringVar(value="Bristol")
		self.selected_date = tk.StringVar(value="Thu 15/05")
		
		self.selected_button = None
		self.buttons = {}

		self.create_dropdown()
		self.create_day_buttons(8)
		self.create_movie_list_area()
		self.update_movie_list()
  
		self.protocol("WM_DELETE_WINDOW", self.controller.exit)

	def create_dropdown(self):
		frame = tk.Frame(self)
		frame.pack(pady=10)
		tk.Label(frame, text="Select City:").pack(side="left", padx=5)
		city_options = ttk.Combobox(frame, textvariable=self.selected_city, values=self.controller.get_location())
		city_options.pack(side="left")
		city_options.bind("<<ComboboxSelected>>", lambda e: self.update_movie_list())

	def create_day_buttons(self, num_days):
		container = tk.Frame(self)
		container.pack(fill="x", expand=False, padx=5, pady=5)

		canvas = tk.Canvas(container, height=25)
		day_scrollbar = ttk.Scrollbar(container, orient="horizontal", command=canvas.xview)
		canvas.configure(xscrollcommand=day_scrollbar.set)

		canvas.grid(row=0, column=0, sticky="ew") 
		day_scrollbar.grid(row=1, column=0, sticky="ew")
		container.columnconfigure(0, weight=1)

		days_frame = tk.Frame(canvas)
		canvas_window = canvas.create_window((0, 0), window=days_frame, anchor="nw")


		today = datetime.datetime.now()

		for i in range(num_days):
			current_date = today + datetime.timedelta(days=i)
			day_str = current_date.strftime("%a %d/%m") #Mon 01/04
			btn = tk.Button(
				days_frame,
				text=day_str,
				command=lambda d=day_str: self.select_day(d),
				width=10,
			)
			btn.pack(side="left", padx=2)
			self.buttons[day_str] = btn

		def update_scroll_region(event=None):
			canvas.configure(scrollregion=canvas.bbox("all"))

		def on_canvas_configure(event):
			canvas_width = event.width
			canvas.itemconfig(canvas_window, width=canvas_width)

		def on_mousewheel(event):
        # Handle mouse wheel scrolling
			try:
				if hasattr(event, 'num') and event.num == 4 or hasattr(event, 'delta') and event.delta > 0:
					canvas.xview_scroll(-1, "units")
				elif hasattr(event, 'num') and event.num == 5 or hasattr(event, 'delta') and event.delta < 0:
					canvas.xview_scroll(1, "units")
				else:
					canvas.xview_scroll(int(-1*(event.delta/120)), "units")
			except:
			    # Fallback for platforms with different event structure
				if hasattr(event, 'delta') and event.delta > 0:
					canvas.xview_scroll(-1, "units")
				else:
					canvas.xview_scroll(1, "units")

		self.update_idletasks()
		update_scroll_region()

		days_frame.bind("<Configure>", update_scroll_region)
		canvas.bind("<Configure>", on_canvas_configure)
        
        # Enable mouse wheel scrolling
		canvas.bind_all("<MouseWheel>", on_mousewheel)
		canvas.bind_all("<Button-4>", on_mousewheel)
		canvas.bind_all("<Button-5>", on_mousewheel)

	def select_day(self, date):
		if self.selected_button:
			self.selected_button.config(fg="black") 

		btn = self.buttons[date]
		btn.config(fg="lightblue")  

		self.selected_button = btn  
		self.selected_date.set(date)
		self.update_movie_list()

	def create_movie_list_area(self):
		container = tk.Frame(self)
		container.pack(pady=15, fill="both", expand=True)

		# Create canvas and movie_scrollbar
		movie_canvas = tk.Canvas(container)
		movie_scrollbar = ttk.Scrollbar(container, orient="vertical", command=movie_canvas.yview)
		movie_canvas.configure(yscrollcommand=movie_scrollbar.set)

		movie_scrollbar.pack(side="right", fill="y")
		movie_canvas.pack(side="left", fill="both", expand=True)

		# Create a frame inside the movie_canvas
		self.movie_frame = tk.Frame(movie_canvas)
		movie_canvas.create_window((0, 0), window=self.movie_frame, anchor="nw")

		# Update scrollregion when content changes
		def on_configure(event):
			movie_canvas.configure(scrollregion=movie_canvas.bbox("all"))

		self.movie_frame.bind("<Configure>", on_configure)

    # Scroll with mousewheel
		def on_mousewheel(event):
			movie_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
		
		movie_canvas.bind_all("<MouseWheel>", on_mousewheel)

	def update_movie_list(self):
		# Clear current area
		for widget in self.movie_frame.winfo_children():
			widget.destroy()

		city = self.selected_city.get()
		date = self.selected_date.get()
		movies = self.controller.get_movies(city, date)
		
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
			tk.Label(frame, text="Showtime: " + movie[7], font=("Arial", 12)).pack(anchor="w")

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
		self.controller.show_seats(movie)
  
	def log_out(self):
		self.controller.log_out()

	def go_back(self):
		self.controller.go_back()
		self.destroy()



