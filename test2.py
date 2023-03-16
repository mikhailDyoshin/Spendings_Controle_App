import tkinter as tk
from customPlot import CustomPlot


app = tk.Tk()

canvW = 500
canvH = 300

d = {'May': 2000, 'June': 3000, 'July': 4000, 'Aug': 4543, 'Sep.': 1273, 'Oct.': 10047}
# d = {'May': 200, 'June': 300, 'July': 400, 'Aug': 443,}
canvas = CustomPlot(app, width=canvW, height=canvH, data=d)
canvas.pack()

# canvas.create_rectangle(10, 10, 20, 50, fill='yellow')

tk.mainloop()
