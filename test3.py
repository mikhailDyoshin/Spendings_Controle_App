import tkinter as tk
from DaysCounter import DaysCounter


root = tk.Tk()

root.config(width=300, height=300)

weeksCounterFrame = tk.Frame(root, background='#c47104')
weeksCounterFrame.pack(padx=5, pady=5)

existingDates = ['2023-04-01', '2022-12-03', '2023-04-03']

canvas = DaysCounter(weeksCounterFrame, existingDates=existingDates)
canvas.pack(padx=3, pady=3)

root.mainloop()
