import tkinter as tk
from tkinter import ttk
import datetime

class DateScrollbar:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Date Selector")
        self.root.geometry("500x120")
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create canvas with scrollbar
        self.canvas = tk.Canvas(main_frame, height=50)
        scrollbar = ttk.Scrollbar(main_frame, orient="horizontal", command=self.canvas.xview)
        
        # Position scrollbar and canvas
        self.canvas.pack(side="top", fill="x")
        scrollbar.pack(side="bottom", fill="x")
        
        # Connect scrollbar to canvas
        self.canvas.configure(xscrollcommand=scrollbar.set)
        
        # Create a frame inside the canvas for buttons
        self.days_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.days_frame, anchor="nw")
        
        # Create date buttons
        self.create_date_buttons(14)
        
        # Setup is complete, now configure scrolling
        self.root.update_idletasks()  # Force geometry update
        self.update_scroll_region()   # Set initial scroll region
        
        # Bind events for dynamic updates
        self.days_frame.bind("<Configure>", self.update_scroll_region)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Enable mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind_all("<Button-4>", self.on_mousewheel)
        self.canvas.bind_all("<Button-5>", self.on_mousewheel)
    
    def update_scroll_region(self, event=None):
        # Update the scrollregion to the full size of the frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        # Update the width of the frame to fill the canvas
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def on_mousewheel(self, event):
        # Handle mouse wheel scrolling
        try:
            if event.num == 4 or event.delta > 0:
                self.canvas.xview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                self.canvas.xview_scroll(1, "units")
            else:
                self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        except:
            # Fallback for platforms with different event structure
            if event.delta > 0:
                self.canvas.xview_scroll(-1, "units")
            else:
                self.canvas.xview_scroll(1, "units")
    
    def create_date_buttons(self, num_days):
        # Get today's date
        today = datetime.datetime.now()
        
        # Create buttons for the specified number of days
        for i in range(num_days):
            current_date = today + datetime.timedelta(days=i)
            day_str = current_date.strftime("%a %d/%m")  # Format: Mon 01/04
            
            btn = ttk.Button(
                self.days_frame,
                text=day_str,
                command=lambda d=current_date: self.select_date(d),
                width=10
            )
            btn.pack(side="left", padx=3, pady=5)
    
    def select_date(self, date):
        print(f"Selected date: {date.strftime('%A, %d/%m/%Y')}")
        # Your code to handle the selected date

# Create and run the application
if __name__ == "__main__":
    app = DateScrollbar()
    app.root.mainloop()