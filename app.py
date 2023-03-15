from tkinter import *
from tkinter import messagebox
import datetime
from handy import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db import Database
from data import Data
from YearlyGraph import YearlyGraph
from tkcalendar import DateEntry
from myDateEntry import MyDateEntry


class App(Tk):
    """
        This class describes the Spending-Control-App's funcionality.
    """
    def __init__(self):
        super().__init__()

        # The protocol defines what happens when the user closes a window
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Window title
        self.title("Spending-Control-App")

        # Database
        self.db = Database('storage.db')

        # Fields of the table in the database
        self.fields = ('food', 'transport', 'shopping', 'total')

        # All records fetched from the database
        self.records = self.db.fetch()

        # data-conveyer
        self.dataConv = Data(self.records, self.fields)

        # sorted list of data fetched from the database
        # from the most recent to the latest date
        self.dataSortedReverse = self.dataConv.dataSortedReverse

        # Initial dictionary
        self.initDict = self.dataConv.initDict

        # Plot of the last year spendings
        self.yearlyGraph = YearlyGraph(self.initDict)

        # The list of plots
        self.plotsList = [self.dataConv.lastWeekPlotFig, 
                          self.dataConv.lastMonthPlotFig,
                          self.yearlyGraph.yearlyPlot]
        # Default plot's index in the list of plots
        self.activePlotIndex = 0
        # Default plot to display
        self.activePlot = self.plotsList[self.activePlotIndex]

        
        """ Frames """
        # Frame for inputs, buttons and the list box
        self.mainFrame = Frame(self, width=800, height=1000)
        self.mainFrame.grid(row=0, column=0)

        # Frame that stores all interactive objects (buttons, entries, listbox)
        self.interactiveFrame = Frame(self.mainFrame, width=400, height=1000, padx=5, pady=5)
        self.interactiveFrame.grid(column=0, row=0)

        # Frame for inputs
        self.inputsFrame = Frame(self.interactiveFrame, width=400, height=300)
        self.inputsFrame.grid(column=0, row=0)

        # Frame for buttons
        self.buttonsFrame = Frame(self.interactiveFrame, width=400, height=100,)
        self.buttonsFrame.grid(row=1, column=0)

        # Frame for list box
        self.listBoxFrame = Frame(self.interactiveFrame, width=400, height=600,)
        self.listBoxFrame.grid(row=2, column=0, pady=20)

        # Frame for the plot and buttons that controle it
        self.plotFrame = Frame(self.mainFrame,  width=400, height=1000, padx=2, pady=2)
        self.plotFrame.grid(row=0,  column=1)

        self.plotButtonsFrame = Frame(self.plotFrame,  width=400, height=100)
        self.plotButtonsFrame.grid(row=0,  column=0, pady=2)

        self.plotImageFrame = Frame(self.plotFrame,  width=400, height=900)
        self.plotImageFrame.grid(row=1,  column=0)

        """ ******************************** Widgets ******************************** """

        """ Plot's canvas """
        # Canvas to draw a plot
        self.canvas = FigureCanvasTkAgg(
            self.activePlot,
            master = self.plotImageFrame)
        
        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(N, S, W, E))

        """ Date field """
        # Date label
        self.date_label = Label(
            self.inputsFrame, 
            text="Date", 
            font=('bold', 14), 
            pady=10, padx=5
        )
        self.date_label.grid(row=0, column=0,)
        # Date input
        self.date_entry = MyDateEntry(self.inputsFrame, align='right', width=14)
        self.date_entry.grid(row=0, column=1,)

        """ Food spendings"""
        # Food label
        self.food_text = StringVar()
        self.food_label = Label(self.inputsFrame, text="Food", font=('bold', 14), pady=10, padx=5)
        self.food_label.grid(row=1, column=0,)
        # Food input
        self.food_entry = Entry(self.inputsFrame, textvariable=self.food_text, width=15)
        self.food_entry.grid(row=1, column=1,)

        """ Transport spendings """
        # Transport label
        self.transport_text = StringVar()
        self.transport_label = Label(self.inputsFrame, text="Transport", font=('bold', 14), pady=10, padx=5)
        self.transport_label.grid(row=2, column=0,)
        # Transport input
        self.transport_entry = Entry(self.inputsFrame, textvariable=self.transport_text, width=15)
        self.transport_entry.grid(row=2, column=1,)

        """ Shopping """
        # Shopping label
        self.shopping_text = StringVar()
        self.shopping_label = Label(self.inputsFrame, text="Shopping", font=('bold', 14), pady=10, padx=5)
        self.shopping_label.grid(row=3, column=0,)
        # Shopping input
        self.shopping_entry = Entry(self.inputsFrame, textvariable=self.shopping_text, width=15)
        self.shopping_entry.grid(row=3, column=1,)

        """ Spendings list """
        listPositionX = 0
        listPositionY = 0
        listColumnSpan = 3
        self.scrollbarPositionX = listPositionX + listColumnSpan + 1

        # Create list box
        self.records_list = Listbox(
            self.listBoxFrame, 
            border=2, 
            width=50, height=10,
            font = "Helvetica",
            bg = "grey",
            fg = 'yellow',
            selectbackground = "black",
            selectforeground = "orange"
        )
        self.records_list.grid(
            row=listPositionY, 
            column=listPositionX, 
            rowspan=1, 
            columnspan=listColumnSpan,  
            sticky=(N, W, E, S),
            padx=10, pady=5,
        )

        # Create scrollbar
        self.scrollbar = Scrollbar(self.listBoxFrame)
        self.scrollbar.grid(row=0, column=self.scrollbarPositionX, sticky=(N, W, E, S))

        # Connect scrollbar to the listbox
        self.records_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.records_list.yview)


        """ Buttons """
        buttonPadX = 10
        buttonMargX = 5
        buttonMargY = 5

        # Add button
        self.add_btn = Button(
            self.buttonsFrame, 
            text="Add Report", 
            padx=buttonPadX, pady=5, 
            command=self.add_item
        )
        self.add_btn.grid(
            row=0, column=0,
            padx=buttonMargX, pady=buttonMargY
        )

        # Remove button
        self.remove_btn = Button(
            self.buttonsFrame, 
            text="Remove Report", 
            padx=buttonPadX, pady=5, 
            command=self.remove_item
        )
        self.remove_btn.grid(
            row=0, column=1,
            padx=buttonMargX, pady=buttonMargY
            )

        # Update button
        self.update_btn = Button(self.buttonsFrame, text="Update Report", padx=buttonPadX, pady=5, command=self.update_item)
        self.update_btn.grid(
            row=0, column=2,
            padx=buttonMargX, pady=buttonMargY
        )

        # Clear button
        self.clear_btn = Button(self.buttonsFrame, text="Clear Report", padx=buttonPadX, pady=5, command=self.clear_text)
        self.clear_btn.grid(
            row=0, column=3,
            padx=buttonMargX, pady=buttonMargY
        )

        self.plotBtnsWidth = 21

        # Button shows the week-plot
        self.plot_btn = Button(
            master = self.plotButtonsFrame,
            command = self.showWeekPlot,
            height = 1,
            width = self.plotBtnsWidth,
            text = "Week"
        )
        self.plot_btn.grid(
            row = 0, column=0,
            padx=buttonMargX, pady=buttonMargY
        )

        # Button shows the month-plot
        self.plot_btn = Button(
            master = self.plotButtonsFrame,
            command = self.showMonthPlot,
            height = 1,
            width = self.plotBtnsWidth,
            text = "Month"
        )
        self.plot_btn.grid(
            row = 0, column=1, 
            padx=buttonMargX, pady=buttonMargY
        )

        # Button shows the year-plot
        self.plot_btn = Button(
            master = self.plotButtonsFrame,
            command = self.showYearPlot,
            height = 1,
            width = self.plotBtnsWidth,
            text = "Year"
        )
        self.plot_btn.grid(
            row = 0, column=2, 
            padx=buttonMargX, pady=buttonMargY
        )

        # Bind select
        self.records_list.bind('<<ListboxSelect>>', self.select_item)

        """ Key bindings """
        self.bind('<Return>', self.add_item)

        
    """ Methods """
    def add_item(self, *event):
        """
            Adds new item: inserts it into database and updates the list box.
        """
        # Check if there is an empty input field
        if self.checkEmptyFields() or self.checkFloatFields():
            return None
        
        if self.check_exsisted_while_adding():
            return None

        # Insert data in database
        self.db.insert(
            self.date_entry.get_date(), 
            self.food_text.get(), 
            self.transport_text.get(), 
            self.shopping_text.get()
        ) 

        # Clear all inputs
        self.clear_text()

        # Update all vusualized data in the app
        self.update_visual()


    def clear_text(self):
        """
            Clears all text inputs.
        """
        self.food_entry.delete(0, END)
        self.transport_entry.delete(0, END)
        self.shopping_entry.delete(0, END)


    def checkEmptyFields(self):
        thereIsEmptyField = self.food_text.get() == '' or self.transport_text.get() == '' or self.shopping_text.get() == ''
        if thereIsEmptyField:
            messagebox.showerror("Required Fields", "Please include all fields")

        return thereIsEmptyField
    

    def checkFloatFields(self):
        try:
            float(self.food_text.get())
            float(self.transport_text.get())
            float(self.shopping_text.get())
            return False
        except ValueError:
            messagebox.showerror("Float Fields", "Please enter a float or an integer number")
            return True
        
    
    def check_exsisted_while_adding(self):
        datesExisted = self.initDict.keys()
        inputDate = date2str(self.date_entry.get_date())

        if inputDate in datesExisted:
            if messagebox.askokcancel("Record's already exist.", "The record's already exist. Do you want to update it?"):
                id = self.db.get_id(inputDate)
                self.db.update(
                    id, 
                    inputDate, 
                    self.food_text.get(), 
                    self.transport_text.get(), 
                    self.shopping_text.get()
                )
                self.update_visual()
                return True
            else:
                return True
        else:
            return False
        
    
    def check_existed_while_updatind(self):
        datesExisted = self.initDict.keys()
        inputDate = date2str(self.date_entry.get_date())

        if inputDate in datesExisted:
            return False
        else:
            if messagebox.askokcancel("No such record", "There is no record with given date. Do you want to create a new one?"):
                self.db.insert(
                    inputDate, 
                    self.food_text.get(), 
                    self.transport_text.get(), 
                    self.shopping_text.get()
                )
                self.update_visual()
                return True
            else:
                return True
            

    def check_existed_while_deleting(self):
        datesExisted = self.initDict.keys()
        inputDate = date2str(self.date_entry.get_date())

        if inputDate in datesExisted:
            return False
        else:
            messagebox.showerror("No such record", "There is no record with given date.")
            return True



    def populate(self):
        """
            Updates the list box:
                - Deletes all data from the list box;
                - Gets all data from the database and inserts it into list box;
        """
        self.records_list.delete(0, END)
        for date, data in self.initDict.items():
            total = data['total']
            dateDMY = isoform2dmY(date)
            self.records_list.insert(END, f'{dateDMY} Spent: {total} rubles')


    def remove_item(self):
        """
            Removes selected item: removes it from the database and updates the list box.
        """
        # Check if there is an empty input field
        if self.checkEmptyFields() or self.checkFloatFields():
            return None
        
        if self.check_existed_while_deleting():
            return None
        
        self.db.remove(self.selectedID)
        self.clear_text()
        self.update_visual()


    def select_item(self, event):
        """
            Inserts selected item's data into input fields, 
            gets the item's id.
        """
        index = self.records_list.curselection()
        if index:
            selected_item = self.records_list.get(index[0])
            
            date = selected_item[0:10]
            
            dateIsoformat = dmY2isoform(date)

            self.selectedID = self.db.get_id(dateIsoformat)

            data = self.initDict[dateIsoformat]

            self.date_entry.set_date(str2date(dateIsoformat))
            self.food_entry.delete(0, END)
            self.food_entry.insert(END, data['food'])
            self.transport_entry.delete(0, END)
            self.transport_entry.insert(END, data['transport'])
            self.shopping_entry.delete(0, END)
            self.shopping_entry.insert(END, data['shopping'])

    
    def showWeekPlot(self):
        self.activePlotIndex = 0
        
        self.activePlot = self.plotsList[self.activePlotIndex]

        self.update_plot()


    def showMonthPlot(self):
        self.activePlotIndex = 1
        
        self.activePlot = self.plotsList[self.activePlotIndex]

        self.update_plot()


    def showYearPlot(self):
        self.activePlotIndex = 2
        
        self.activePlot = self.plotsList[self.activePlotIndex]

        self.update_plot()


    def update_item(self):
        """
            Updates edited item.
        """
        # Check if there is an empty input field
        if self.checkEmptyFields() or self.checkFloatFields():
            return None
        
        # Check if the record's exist
        if self.check_existed_while_updatind():
            return None

        
        self.db.update(self.selectedID, self.date_entry.get_date(), self.food_text.get(), self.transport_text.get(), self.shopping_text.get())
        self.update_visual()


    def update_plot(self):
        """
            The function updates the plot.
        """
        # Canvas to draw a plot
        self.canvas = FigureCanvasTkAgg(
            self.activePlot,
            master = self.plotImageFrame)
        
        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(N, S, W, E))


    def update_visual(self):
        """
            The function redownloads all data from the database 
            and then: 
                - prepares the data for the plot again;
                - updates the list-box;
                - updates the plot.
        """
        self.records = self.db.fetch() 
        self.dataConv = Data(self.records, self.fields)
        self.initDict = self.dataConv.initDict
        self.yearlyGraph = YearlyGraph(self.initDict)
        self.plotsList = [self.dataConv.lastWeekPlotFig, 
                          self.dataConv.lastMonthPlotFig,
                          self.yearlyGraph.yearlyPlot]
        self.activePlot = self.plotsList[self.activePlotIndex]
        self.dataSortedReverse = self.dataConv.dataSortedReverse
        self.populate()
        self.update_plot()


    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.quit()
            self.destroy()

