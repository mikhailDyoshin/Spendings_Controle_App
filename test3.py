from tkinter import ttk
import tkinter

root = tkinter.Tk()

style = ttk.Style()

style.configure(
    "TButton", 
    padding=6, 
    relief="flat",
    background='#131912',
    font= ('Prestige Elite Std', 10, 'bold'),
    foreground='#df5705',
    borderwidth=0,
   )

style.map("TButton",
    foreground=[('pressed', 'black'), ('active', 'black')],
    background=[('pressed', '!disabled', '#df6f05'), ('active', '#df5705')]
    )

btn = ttk.Button(text="Sample")
btn.pack()


root.mainloop()
