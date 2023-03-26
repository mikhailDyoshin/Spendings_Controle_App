import tkinter as tk
from customPlot import CustomPlot


app = tk.Tk()

canvW = 800
canvH = 500

d = {'May': 2000, 'June': 3000, 'July': 4000, 'Aug': 4543, 'Sep.': 12073, 'Oct.': 10047, 'Nov': 9765.41}
# d = {'May': 200, 'June': 300, 'July': 400, 'Aug': 443,}
canvas = CustomPlot(app, width=canvW, height=canvH)
canvas.pack()
# canvas.draw_data(d)

d1 = {'One': [1, 2, 3, 2, 3], 'Two': [1, 2, 3, 1, 3], 'Three': [1, 2, 3, 1, 3],}

# canvas.mult_bars(d1)

# canvas.draw_mult_bars(['21.03.2023', '22.03.2023', '23.03.2023'], d1)

canvas.draw_mult_bars_plot(['21.03.2023', '22.03.2023', '23.03.2023', '26.03.2023', '25.03.2023'], d1, drawAllValues=True)

# canvas.drawLegend(['food', 'shopping', 'transport'])

tk.mainloop()
