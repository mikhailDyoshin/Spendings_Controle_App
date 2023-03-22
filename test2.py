import tkinter as tk
from customPlot import CustomPlot


app = tk.Tk()

canvW = 500
canvH = 300

d = {'May': 2000, 'June': 3000, 'July': 4000, 'Aug': 4543, 'Sep.': 12073, 'Oct.': 10047, 'Nov': 9765.41}
# d = {'May': 200, 'June': 300, 'July': 400, 'Aug': 443,}
canvas = CustomPlot(app, width=canvW, height=canvH)
canvas.pack()
canvas.draw_data(d)

d1 = {'One': [1, 2, 3], 'Two': [1, 2, 3], 'Three': [1, 2, 3]}

# canvas.mult_bars(d1)

canvas.draw_mult_bars(d1)

# canvas.create_rectangle(10, 10, 20, 50, fill='yellow')

tk.mainloop()
