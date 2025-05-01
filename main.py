import tkinter as tk
from app import AppManager

if __name__ == "__main__":
	root = tk.Tk()
	root.title("HC Cinemas")
	root.geometry("900x600")
	app = AppManager(root)
	root.mainloop()