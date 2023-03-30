import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry


root = tk.Tk()

root.config(width=300, height=300)

style = ttk.Style()
style.theme_use('clam')
style.configure(
    'custom.DateEntry', 
    fieldbackground='#131912',
    foreground='#df5705',
    # border=0,
    arrowcolor='#000',
    insertcolor='#bbbcbf'
)

# create dateEntry using the custom style
dateEntry = DateEntry(
    root,
    disabledbackground='red',
    borderwidth=2,
    bordercolor='#131912',
    headersbackground='#131912',
    headersforeground='#df5705',
    weekendbackground='#bd5d2d', 
    weekendforeground='#000',
    font=('Prestige Elite Std', 12, 'bold'),
    background='#000',
    othermonthforeground='#444444',
    normalforeground='#000',
    tooltipforeground='red',
    foreground='#df5705',
    style='custom.DateEntry',
) 



dateEntry.pack()

# print(help(dateEntry.configure))
keys = dateEntry.keys()

for key in keys:
    print(key)


root.mainloop()
