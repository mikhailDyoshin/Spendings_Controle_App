import tkinter as tk
from DaysCounter import DaysCounter


root = tk.Tk()

root.config(width=300, height=300)

weeksCounterFrame = tk.Frame(root, background='black')
weeksCounterFrame.pack(padx=10, pady=10)

existingDates = ['2023-04-01', '2022-12-03', '2023-04-03']

canvas = DaysCounter(weeksCounterFrame, width=1105, existingDates=existingDates)
canvas.pack(padx=1, pady=1)




root.mainloop()
