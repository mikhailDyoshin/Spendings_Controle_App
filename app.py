from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import datetime
from handy import *
from db import Database
from data import Data
from myDateEntry import MyDateEntry
from customPlot import CustomPlot


class App(Tk):
    """
        This class describes the Spending-Control-App's funcionality.
    """
    def __init__(self):

        super().__init__()

        self.background = '#131912'

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
        self.data = Data(self.records, self.fields)

        # Initial dictionary where dates and data are stored
        self.initDict = self.data.initDict

        self.selectedID = None

        # The list of tuples that stores data to display on UI
        self.update_displayable_data()

        # Default plot's index in the list of plots
        self.activePlotIndex = 0

        # Updates active data to display on UI
        self.update_active_data()

        """ Frames """
        # Frame for inputs, buttons and the list box
        self.mainFrame = Frame(self, width=800, height=1000, background=self.background)
        self.mainFrame.grid(row=0, column=0)

        # Frame that stores all interactive objects (buttons, entries, listbox)
        self.interactiveFrame = Frame(
            self.mainFrame, 
            width=400, height=1000, 
            padx=5, pady=5, 
            background=self.background
        )
        self.interactiveFrame.grid(column=0, row=0)

        # Frame for inputs
        self.inputsFrame = Frame(
            self.interactiveFrame, 
            width=400, height=300, 
            background=self.background,
        )
        self.inputsFrame.grid(column=0, row=0)

        # Frame for buttons
        self.buttonsFrame = Frame(
            self.interactiveFrame, 
            width=400, height=100,
            pady=20,
            background=self.background,
        )
        self.buttonsFrame.grid(row=1, column=0)

        # Frame for list box
        self.listBoxFrame = Frame(
            self.interactiveFrame, 
            width=400, height=600,
            background=self.background,
        )
        self.listBoxFrame.grid(row=2, column=0)

        # Frame for the plot and buttons that controle it
        self.plotFrame = Frame(
            self.mainFrame, 
            width=400, height=1000, 
            padx=2, pady=2,
            background=self.background,
        )
        self.plotFrame.grid(row=0,  column=1)

        self.plotButtonsFrame = Frame(
            self.plotFrame, 
            width=400, height=100,
            background=self.background,
            )
        self.plotButtonsFrame.grid(row=0,  column=0, pady=2)

        self.plotImageFrame = Frame(
            self.plotFrame,  
            width=400, height=900,
        )
        self.plotImageFrame.grid(row=1,  column=0)

        self.plotLabelFrame = Frame(
            self.plotFrame,
            width=100, height=100,
            background=self.background,
        )
        self.plotLabelFrame.grid(row=2,  column=0)

        """ ******************************** Styles ******************************** """
        style = ttk.Style()

        style.theme_use('clam')

        # Plot buttons
        style.configure(
            "plot.TButton", 
            padding=6, 
            relief="solid",
            background='#131912',
            font=('Prestige Elite Std', 12, 'bold'),
            foreground='#df5705',
            borderwidth=2,
            bordercolor='#df5705',
            width=27,
            focuscolor='#df5705'
        )

        style.map("plot.TButton",
            foreground=[
                ('pressed', 'black'), 
                ('active', 'black'),
                ('focus', '#f96604'),
            ],
            background=[
                ('pressed', '!disabled', '#df6f05'), 
                ('active', '#df5705'),
                ('focus', '#1f251e')
            ],
            focuscolor=[
                ('pressed', '!disabled', '#df6f05'), 
                ('active', '#df5705'),
                ('focus', '#1f251e')
            ],
            )
        
        # Manage buttons
        style.configure(
            "manage.TButton", 
            padding=6, 
            relief="solid",
            background='#131912',
            font=('Prestige Elite Std', 12, 'bold'),
            foreground='#df5705',
            borderwidth=2,
            bordercolor='#df5705',
            width=15,
            focuscolor='#df5705'
        )

        style.map("manage.TButton",
            foreground=[
                ('pressed', 'black'), 
                ('active', 'black'),
                ('focus', '#f96604'),
            ],
            background=[
                ('pressed', '!disabled', '#df6f05'), 
                ('active', '#df5705'),
                ('focus', '#1f251e')
            ],
            focuscolor=[
                ('pressed', '!disabled', '#df6f05'), 
                ('active', '#df5705'),
                ('focus', '#1f251e')
            ],
            )
        
        # Labels
        style.configure(
            'field.TLabel', 
            foreground='#df5705', 
            background='#131912',
            font=('Prestige Elite Std', 14, 'bold'),
            anchor='w',
            width=12
        )

        # Plot-label
        style.configure(
            'plotLabel.TLabel', 
            foreground='#df5705', 
            background='#131912',
            font=('Prestige Elite Std', 14, 'bold'),
            anchor='center',
            width=80,
        )

        # DateEntry
        style.configure(
            'custom.DateEntry', 
            fieldbackground='#131912',
            foreground='#df5705',
            arrowcolor='#000',
            insertcolor='#bbbcbf'
        )

        # Scrollbar
        style.configure(
            'Custom.Vertical.TScrollbar', 
            gripcount=0, 
            background='#df5705', 
            darkcolor='#111111', lightcolor='#222222', troughcolor='#131912', 
            bordercolor='#444444', 
            arrowcolor='black', arrowsize=16
        )

        """ ******************************** Widgets ******************************** """

        """ Plot's canvas """
        # Canvas to draw a plot
        self.canvas = CustomPlot(
            master = self.plotImageFrame,
            width=800, height=500,
            )
        
        # placing the canvas on the Tkinter window
        self.canvas.grid(row=0, column=0, sticky=(N, S, W, E))

        # Draw the plot
        self.canvas.draw_mult_bars_plot(self.activeDatesList, self.activeData)

        # Display legend
        self.canvas.draw_legend(self.fields[:-1])

        """ Date field """
        # Date label
        self.date_label = ttk.Label(
            self.inputsFrame, 
            text="Date", 
            style='field.TLabel',
        )
        self.date_label.grid(row=0, column=0, sticky='w')
        
        # Date input
        self.date_entry = MyDateEntry(
            self.inputsFrame, 
            align='right', 
            width=14,
            disabledbackground='red',
            borderwidth=2,
            bordercolor='#131912',
            headersbackground='#131912',
            headersforeground='#df5705',
            weekendbackground='#bd5d2d', 
            weekendforeground='#000',
            font=('Prestige Elite Std', 12, 'bold'),
            background='#df5705',
            # othermonthforeground='#444444',
            normalforeground='#000',
            tooltipforeground='red',
            foreground='#000',
            style='custom.DateEntry',
        )
        self.date_entry.grid(row=0, column=1,)

        """ Food spendings"""
        # Food label
        self.food_text = StringVar()
        self.food_label = ttk.Label(
            self.inputsFrame, 
            text="Food", 
            style='field.TLabel',
        )
        self.food_label.grid(row=1, column=0, sticky='w')
        # Food input
        self.food_entry = Entry(
            self.inputsFrame, 
            textvariable=self.food_text, 
            width=15,
            highlightthickness=0,
            borderwidth=2,
            background='black',
            insertbackground='#bbbcbf',
            font=('Prestige Elite Std', 12, 'bold'),
            foreground='#df5705',
        )
        self.food_entry.grid(row=1, column=1, sticky='e')

        """ Transport spendings """
        # Transport label
        self.transport_text = StringVar()
        self.transport_label = ttk.Label(
            self.inputsFrame, 
            text="Transport",
            style='field.TLabel',
            
        )
        self.transport_label.grid(row=2, column=0, sticky='w')
        # Transport input
        self.transport_entry = Entry(
            self.inputsFrame,
            textvariable=self.transport_text, 
            width=15,
            highlightthickness=0,
            borderwidth=2,
            background='black',
            insertbackground='#bbbcbf',
            font=('Prestige Elite Std', 12, 'bold'),
            foreground='#df5705',    
        )
        self.transport_entry.grid(row=2, column=1, pady=4)

        """ Shopping """
        # Shopping label
        self.shopping_text = StringVar()
        self.shopping_label = ttk.Label(
            self.inputsFrame, 
            text="Shopping",
            style='field.TLabel',
        )
        self.shopping_label.grid(row=3, column=0, sticky='w')
        # Shopping input
        self.shopping_entry = Entry(
            self.inputsFrame, 
            textvariable=self.shopping_text, 
            width=15,
            highlightthickness=0,
            borderwidth=2,
            background='black',
            insertbackground='#bbbcbf',
            font=('Prestige Elite Std', 12, 'bold'),
            foreground='#df5705',    
        )
        self.shopping_entry.grid(row=3, column=1,)

        """ Spendings list """
        listPositionX = 0
        listPositionY = 0
        listColumnSpan = 3
        self.scrollbarPositionX = listPositionX + listColumnSpan + 1

        # Create list box
        self.records_list = Listbox(
            self.listBoxFrame, 
            # border=2, 
            width=40, height=10,
            background='#131912',
            foreground='#df5705',
            selectbackground='#df5705',
            selectforeground='#000000',
            font=('Prestige Elite Std', 12, 'bold'),
            justify='center',
            borderwidth=2, highlightthickness=2,
            highlightbackground = '#df5705',

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
        self.scrollbar = ttk.Scrollbar(self.listBoxFrame, style='Custom.Vertical.TScrollbar')
        self.scrollbar.grid(row=0, column=self.scrollbarPositionX, sticky=(N, W, E, S))

        # Connect scrollbar to the listbox
        self.records_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.records_list.yview)


        """ Buttons """
        buttonPadX = 10
        buttonMargX = 5
        buttonMargY = 5

        # Add button
        self.add_btn = ttk.Button(
            self.buttonsFrame, 
            text="Add Report",  
            command=self.add_item,
            style='manage.TButton',
        )
        self.add_btn.grid(
            row=0, column=0,
            padx=buttonMargX, pady=buttonMargY
        )

        # Remove button
        self.remove_btn = ttk.Button(
            self.buttonsFrame, 
            text="Remove Report",  
            command=self.remove_item,
            style='manage.TButton',
        )
        self.remove_btn.grid(
            row=0, column=1,
            padx=buttonMargX, pady=buttonMargY
            )

        # Update button
        self.update_btn = ttk.Button(
            self.buttonsFrame, 
            text="Update Report",  
            command=self.update_item,
            style='manage.TButton',
        )
        self.update_btn.grid(
            row=0, column=2,
            padx=buttonMargX, pady=buttonMargY
        )

        # Clear button
        self.clear_btn = ttk.Button(
            self.buttonsFrame, 
            text="Clear Report",  
            command=self.clear_text,
            style='manage.TButton',
        )
        self.clear_btn.grid(
            row=0, column=3,
            padx=buttonMargX, pady=buttonMargY
        )

        self.plotBtnsWidth = 21

        # Button shows the week-plot
        self.week_btn = ttk.Button(
            master = self.plotButtonsFrame,
            command = self.showWeekPlot,
            text = "Week",
            style='plot.TButton'
        )
        self.week_btn.grid(
            row = 0, column=0,
            padx=buttonMargX, pady=buttonMargY
        )

        # Button shows the month-plot
        self.month_btn = ttk.Button(
            master = self.plotButtonsFrame,
            command = self.showMonthPlot,
            text = "Month",
            style='plot.TButton'
        )
        self.month_btn.grid(
            row = 0, column=1, 
            padx=buttonMargX, pady=buttonMargY
        )

        # Button shows the year-plot
        self.year_btn = ttk.Button(
            master = self.plotButtonsFrame,
            command = self.showYearPlot,
            text = "Year",
            style='plot.TButton'
        )
        self.year_btn.grid(
            row = 0, column=2, 
            padx=buttonMargX, pady=buttonMargY
        )

        # Plot's label
        self.plotLabel = ttk.Label(
            self.plotLabelFrame, 
            text="Total",
            style='plotLabel.TLabel',
        )
        # self.plotLabel.grid(
        #     row=0, column=0,
        # )
        self.plotLabel.pack(pady=5)
        # Updates the text of the plot-label
        self.update_labels_text()
        

        # Bind select
        self.records_list.bind('<<ListboxSelect>>', self.select_item)

        """ Key bindings """
        self.bind('<Return>', self.add_item)

        
    """ Methods """
    def add_item(self, *event):
        """
            Adds new item: inserts it into database and updates the list box.
        """
        
        if self.check_valid_input():
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

    
    def check_valid_date(self):
        today = datetime.date.today()
        century = datetime.timedelta(days=365*100)
        centuryAgo = today - century

        inputDate = self.date_entry.get_date()

        if inputDate < centuryAgo or inputDate > today:
            messagebox.showerror("Invalid date", "The date can't lie in the future, or be later than century ago.")
            return True
        
        return False
        
        
    def check_valid_input(self):
        return self.check_empty_fields() or self.check_float_fields() or self.check_positive_input_number() or self.check_valid_date()


    def check_empty_fields(self):
        thereIsEmptyField = self.food_text.get() == '' or self.transport_text.get() == '' or self.shopping_text.get() == ''
        if thereIsEmptyField:
            messagebox.showerror("Required Fields", "Please include all fields")

        return thereIsEmptyField
    

    def check_float_fields(self):
        try:
            
            float(self.food_text.get())
            float(self.transport_text.get())
            float(self.shopping_text.get())
            
        except ValueError:
            messagebox.showerror("Float Fields", "Please enter a positive float or an integer number")
            return True


    def check_positive_input_number(self):
        inputNumbers = [
            float(self.food_text.get()),
            float(self.transport_text.get()),
            float(self.shopping_text.get()),
        ]

        for number in inputNumbers:
            if number < 0:
                messagebox.showerror("Float Fields", "Please enter a positive float or an integer number")
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
            self.records_list.insert(0, f'{dateDMY} Spent: {total} rubles')


    def remove_item(self):
        """
            Removes selected item: removes it from the database and updates the list box.
        """
        if self.selectedID:
        # Check if there is an empty input field
            if self.check_existed_while_deleting():
                return None
            
            
            self.db.remove(self.selectedID)
            self.clear_text()
            self.update_visual()
            return None

        messagebox.showerror("No record is selected", "You didn't select any record to delete.")
        return None


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

        self.update_active_data()
        
        self.update_plot()

        self.update_labels_text()


    def showMonthPlot(self):
        self.activePlotIndex = 1
        
        self.update_active_data()

        self.update_plot()

        self.update_labels_text()


    def showYearPlot(self):
        self.activePlotIndex = 2
        
        self.update_active_data()

        self.update_plot()

        self.update_labels_text()

    
    def update_active_data(self):
        self.activeDatesList = self.dataToDisplay[self.activePlotIndex][0]
        self.activeData = self.dataToDisplay[self.activePlotIndex][1]
        self.activeLabel = self.dataToDisplay[self.activePlotIndex][2]
        self.activePeriod = self.dataToDisplay[self.activePlotIndex][3]

    
    def update_displayable_data(self):
        self.dataToDisplay = [
            (
                self.data.lastWeekDatesSorted, 
                self.data.lastWeekhDictForPlot, 
                self.data.weekTotal,
                'week'
            ),
            (
                self.data.lastMonthDatesSorted, 
                self.data.lastMonthDictForPlot, 
                self.data.monthTotal,
                'month'
            ),    
            (
                self.data.monthsList, 
                self.data.lastYearDictForPlot, 
                self.data.yearTotal,
                'year',
            ),
        ]

    def update_labels_text(self):
        self.plotLabel.configure(
            text=f'Total spendings for the last {self.activePeriod}: {self.activeLabel} rub.')


    def update_item(self):
        """
            Updates edited item.
        """
        # Check valid inputs
        if self.check_valid_input():
            return None
        
        if self.check_existed_while_updatind():
            return None

        
        self.db.update(self.selectedID, self.date_entry.get_date(), self.food_text.get(), self.transport_text.get(), self.shopping_text.get())
        self.update_visual()


    def update_plot(self):
        """
            The function updates the plot.
        """
        # Canvas to draw a plot
        self.canvas.draw_mult_bars_plot(self.activeDatesList, self.activeData)
        self.canvas.draw_legend(self.fields[:-1])
        
        # placing the canvas on the Tkinter window
        self.canvas.grid(row=0, column=0, sticky=(N, S, W, E))


    def update_visual(self):
        """
            The function redownloads all data from the database 
            and then: 
                - prepares the data for the plot again;
                - updates the list-box;
                - updates the plot.
        """
        self.records = self.db.fetch() 
        self.data = Data(self.records, self.fields)
        self.initDict = self.data.initDict
        self.update_displayable_data()
        self.update_active_data()
        self.populate()
        self.update_plot()
        self.update_labels_text()


    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.quit()
            self.destroy()

