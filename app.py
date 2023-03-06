from tkinter import *
from tkinter import messagebox
from handy import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from db import Database


class App(Tk):
    """
        This class describes the Spending-Control-App's funcionality.
    """
    def __init__(self):
        super().__init__()

        # Window title
        self.title("Spending-Control-App")

        # Database
        self.db = Database('storage.db')

        self.records = self.db.fetch()

        # Period of spending days to visualize on the plot
        self.period = 30

        # Data prepared to be plotted
        self.dataForPlot = self.prepare_plot_data() 

        # Selected item in the list box
        self.selected_item = None

        # Canvas to draw a plot
        self.canvas = None

        
        """ Frames """
        # Frame for inputs, buttons and the list box
        self.mainFrame = Frame(self, width=400, height=600)
        self.mainFrame.grid(row=0, column=0)

        # Frame for inputs
        self.inputsFrame = Frame(self.mainFrame, width=400, height=600, padx=5, pady=5)
        self.inputsFrame.grid(column=0, row=0)

        # Frame for buttons
        self.buttonsFrame = Frame(self.mainFrame, width=400, height=100, bg='grey')
        self.buttonsFrame.grid(row=1, column=0, padx=5,  pady=5)

        # Frame for list box
        self.listBoxFrame = Frame(self.mainFrame, width=400, height=600, bg='grey')
        self.listBoxFrame.grid(row=2, column=0, padx=5,  pady=5)

        # Frame for plot
        self.plotFrame = Frame(self,  width=400, height=500, bg='grey', padx=5, pady=5)
        self.plotFrame.grid(row=0,  column=1,  padx=10,  pady=5)

        self.plotButtonsFrame = Frame(self.plotFrame,  width=400, height=100, padx=5, pady=5)
        self.plotButtonsFrame.grid(row=0,  column=0)

        self.plotImageFrame = Frame(self.plotFrame,  width=400, height=400, padx=5, pady=5)
        self.plotImageFrame.grid(row=1,  column=0)

        """ ******************************** Widgets ******************************** """

        """ Date field """
        # Date label
        self.date_text = StringVar()
        self.date_label = Label(self.inputsFrame, text="Date", font=('bold', 14), pady=10, padx=5)
        self.date_label.grid(row=0, column=0, sticky=(N, W, E, S))
        # Date input
        self.date_entry = Entry(self.inputsFrame, textvariable=self.date_text)
        self.date_entry.grid(row=0, column=1, sticky=(W, E))

        """ Food spendings"""
        # Food label
        self.food_text = StringVar()
        self.food_label = Label(self.inputsFrame, text="Food", font=('bold', 14), pady=10, padx=5)
        self.food_label.grid(row=1, column=0, sticky=(N, W, E, S))
        # Food input
        self.food_entry = Entry(self.inputsFrame, textvariable=self.food_text, width=15)
        self.food_entry.grid(row=1, column=1, sticky=(W, E))

        """ Transport spendings """
        # Transport label
        self.transport_text = StringVar()
        self.transport_label = Label(self.inputsFrame, text="Transport", font=('bold', 14), pady=10, padx=5)
        self.transport_label.grid(row=2, column=0, sticky=(N, W, E, S))
        # Transport input
        self.transport_entry = Entry(self.inputsFrame, textvariable=self.transport_text, width=15)
        self.transport_entry.grid(row=2, column=1, sticky=(W, E))

        """ Shopping """
        # Shopping label
        self.shopping_text = StringVar()
        self.shopping_label = Label(self.inputsFrame, text="Shopping", font=('bold', 14), pady=10, padx=5)
        self.shopping_label.grid(row=3, column=0, sticky=(N, W, E, S))
        # Shopping input
        self.shopping_entry = Entry(self.inputsFrame, textvariable=self.shopping_text, width=15)
        self.shopping_entry.grid(row=3, column=1, sticky=(W, E))

        """ Spendings list """
        listPositionX = 0
        listPositionY = 0
        listColumnSpan = 3
        self.scrollbarPositionX = listPositionX + listColumnSpan + 1

        # Create list box
        self.records_list = Listbox(self.listBoxFrame, width=60, height=8, border=0)
        self.records_list.grid(row=listPositionY, column=listPositionX, rowspan=4, columnspan=listColumnSpan, padx=10, pady=10, sticky=(N, W, E, S))

        # Create scrollbar
        self.scrollbar = Scrollbar(self.listBoxFrame)
        self.scrollbar.grid(row=0, column=self.scrollbarPositionX, sticky=W)

        # Connect scrollbar to the listbox
        self.records_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.records_list.yview)


        """ Buttons """
        # Add button
        self.add_btn = Button(self.buttonsFrame, text="Add Report", padx=5, pady=5, command=self.add_item)
        self.add_btn.grid(row=0, column=0)

        # Remove button
        self.remove_btn = Button(self.buttonsFrame, text="Remove Report", padx=5, pady=5, command=self.remove_item)
        self.remove_btn.grid(row=0, column=1)

        # Update button
        self.update_btn = Button(self.buttonsFrame, text="Update Report", padx=5, pady=5, command=self.update_item)
        self.update_btn.grid(row=0, column=2)

        # Clear button
        self.clear_btn = Button(self.buttonsFrame, text="Clear Report", padx=5, pady=5, command=self.clear_text)
        self.clear_btn.grid(row=0, column=3)

        # Button that displays the plot
        self.plot_btn = Button(master = self.plotButtonsFrame,
                            command = self.showWeek,
                            height = 1,
                            width = 10,
                            text = "Week")
        self.plot_btn.grid(row = 0, column=0)

        # Button that hides the plot
        self.plot_btn = Button(master = self.plotButtonsFrame,
                            command = self.showMonth,
                            height = 1,
                            width = 10,
                            text = "Month")
        self.plot_btn.grid(row = 0, column=1)

        # Button that hides the plot
        self.plot_btn = Button(master = self.plotButtonsFrame,
                            command = self.showYear,
                            height = 1,
                            width = 10,
                            text = "Year")
        self.plot_btn.grid(row = 0, column=2)

        # Bind select
        self.records_list.bind('<<ListboxSelect>>', self.select_item)


    """ Methods """
    def add_item(self):
        """
            Adds new item: inserts it into database and updates the list box.
        """
        # Check empty input field
        if self.date_text.get() == '' or self.food_text.get() == '' or self.transport_text.get() == '' or self.shopping_text.get() == '':
            messagebox.showerror("Required Fields", "Please include all fields")
            return

        # Insert data in database
        self.db.insert(self.date_text.get(), self.food_text.get(), self.transport_text.get(), self.shopping_text.get()) 

        # Clear list box because it's not up to date
        self.records_list.delete(0, END) 
        # Insert new item into list box
        self.records_list.insert(END, (self.date_text.get(), self.food_text.get(), self.transport_text.get(), self.shopping_text.get()))

        # Clear all inputs
        self.clear_text()

        # Update all vusualized data in the app
        self.update_visual()


    def clear_text(self):
        """
            Clears all text inputs.
        """
        self.date_entry.delete(0, END)
        self.food_entry.delete(0, END)
        self.transport_entry.delete(0, END)
        self.shopping_entry.delete(0, END)


    def plot(self):
        """
            Displays the plot.
        """
        
        fig, ax = plt.subplots()
    
        # plotting the graph
        ax.bar(self.dataForPlot[0], [x/1000 for x in self.dataForPlot[1]])

        # X-ticks
        xTicks = [el if index == 0 or index == len(self.dataForPlot[0])-1 else '' for index, el in enumerate(self.dataForPlot[0])]

        # Draw x-ticks
        ax.axes.set_xticks(self.dataForPlot[0], xTicks)
    
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(
            fig,
            master = self.plotImageFrame)  

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().grid(row=0, column=0, sticky=(N, S, W, E))


    def populate(self):
        """
            Updates the list box:
                - Deletes all data from the list box;
                - Gets all data from the database and inserts it into list box;
        """
        self.records_list.delete(0, END)
        for row in sortByDate(self.records, reverse=True):
            self.records_list.insert(END, row)


    def prepare_plot_data(self):

        # Sorting fetched data by date
        rowsSorted = sortByDate(self.records)

        # All dates and all total spendings in each day
        dates, spendings = datesAndTotals(rowsSorted)
        
        # Returns the last days' spendings
        return lastDatesSpendings(dates, spendings, period=self.period)


    def remove_item(self):
        """
            Removes selected item: removes it from the database and updates the list box.
        """
        self.db.remove(self.selected_item[0])
        self.clear_text()
        self.update_visual()


    def select_item(self, event):
        """
            Inserts selected item's data into input fields.
        """
        index = self.records_list.curselection()
        if index:
            self.selected_item = self.records_list.get(index[0])

            self.date_entry.delete(0, END)
            self.date_entry.insert(END, self.selected_item[1])
            self.food_entry.delete(0, END)
            self.food_entry.insert(END, self.selected_item[2])
            self.transport_entry.delete(0, END)
            self.transport_entry.insert(END, self.selected_item[3])
            self.shopping_entry.delete(0, END)
            self.shopping_entry.insert(END, self.selected_item[4])


    def showWeek(self):
        """ 
            Displays on the plot the spendings made during the last week.
        """
        self.period = 7
        self.update_plot()


    def showMonth(self):
        """ 
            Displays on the plot the spendings made during the month week.
        """
        self.period = 30
        self.update_plot()


    def showYear(self):
        """ 
            Displays on the plot the spendings made during the last year.
        """
        self.period = 365
        self.update_plot()


    def update_item(self):
        """
            Updates edited item.
        """
        print('Update')
        self.db.update(self.selected_item[0], self.date_text.get(), self.food_text.get(), self.transport_text.get(), self.shopping_text.get())
        self.update_visual()


    def update_plot(self):
        """
            The function updates the plot.
        """
        self.dataForPlot = self.prepare_plot_data() 
        self.plot()


    def update_visual(self):
        """
            The function redownloads all data from the database 
            and then: 
                - prepares the data for the plot again;
                - updates the list-box;
                - updates the plot.
        """
        self.records = self.db.fetch()
        self.dataForPlot = self.prepare_plot_data() 
        self.populate()
        self.plot()
