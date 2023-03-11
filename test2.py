import tkinter as tk

root = tk.Tk()

w = tk.Label(root, text="red", bg="red", fg="white")
w.pack(padx=5, pady=10, side='left')
w = tk.Label(root, text="green", bg="green", fg="black")
w.pack(padx=5, pady=20, side='left')
w = tk.Label(root, text="blue", bg="blue", fg="white")
w.pack(padx=5, pady=20, side='left')
tk.mainloop()