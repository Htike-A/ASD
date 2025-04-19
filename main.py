import tkinter as tk
from app import AppManager

if __name__ == "__main__":
	root = tk.Tk()
	root.title("HC Cinemas")
	root.geometry("800x500")
	
	app = AppManager(root)
	root.mainloop()	