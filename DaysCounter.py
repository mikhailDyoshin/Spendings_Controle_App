import tkinter as tk
import datetime
import numpy as np
from handy import get_quotient_and_remainder, reverse_tuple


class DaysCounter(tk.Canvas):

    """
        The class is the tkinter.Canvas widget. 
        The widget draws 368 rectangles 
        that represent each day from today's day 
        to the day that was 368 days ago.
    """

    def __init__(self, master, existingDates):

        # The number of rectangles (days) to display
        self.N = 371

        # Number of strings to display
        self.strN = 7
        
        # Number of columns to display
        self.colN = int(self.N/self.strN)

        # The width of a rectangle
        self.rectWidth = 10

        self.padX = 37
        self.padY = 26

        self.margX = 5
        self.margY = 5

        width = 2*self.padX + self.colN*self.rectWidth + (self.colN-1)*self.margX
        height = 2*self.padY + self.strN*self.rectWidth + (self.strN-1)*self.margY

        background='#131912'

        super().__init__(master=master, width=width, height=height, background=background, borderwidth=0, highlightthickness=0)

        self.W = width
        self.H = height

        

        self.create_rects(self.form_coords())

        self.existingDates = existingDates

        self.paint_rects()

        self.bind("<Motion>", self.show_info)

        self.currentId = None

    
    def form_coords(self):

        """
            Forms 4 vectors of x0, y0, x1, y1 coordinates 
            for each rectangle to display.
        """
        

        x1CoordsArray = np.zeros(self.colN)
        y1CoordsArray = np.zeros(self.strN)

    
        for index, coord in enumerate(y1CoordsArray):
            if index == 0:
                y1CoordsArray[0] = self.padY
                continue

            y1CoordsArray[index] = y1CoordsArray[index-1] + self.rectWidth + self.margY

        for index, coord in enumerate(x1CoordsArray):
            if index == 0:
                x1CoordsArray[0] = self.padX
                continue

            x1CoordsArray[index] = x1CoordsArray[index-1] + self.rectWidth + self.margX

        x2CoordsArray = x1CoordsArray + self.rectWidth
        y2CoordsArray = y1CoordsArray + self.rectWidth

        return [(x1CoordsArray, y1CoordsArray), (x2CoordsArray, y2CoordsArray)]
    

    def dates_list_former(self):

        """
            The method forms a list of dates from today
            to the day that was self.N days ago.
        """

        # Today's date
        today = datetime.date.today()

        # Number of dates to create
        Ndays = self.N

        # self.N days delta
        delta = datetime.timedelta(days=Ndays)

        # One day delta 
        dateIncrement = datetime.timedelta(days=1)

        # self.N days ago date
        yearAgo = today - delta

        # Empty list to store dates
        dates = []

        # The first element in the list
        date = yearAgo

        # Forms the dates list
        for i in range(Ndays):
            date += dateIncrement
            dates.append(str(date))

        # Forms the list of tuples that store two numbers:
        # 1st is a serial number of a set that consists of 7 elements.
        # The dates-list virtually divided on sets of 7 elements
        # 2nd points to the index of an element in particular set

        datesTuples = [get_quotient_and_remainder(index, 7) for index, date in enumerate(dates)]

        datesTuplesDict = dict(zip(datesTuples, dates))

        return datesTuplesDict


    def create_rects(self, coords):

        """
            Takes the coordinates for rectangles 
            and displays them on the canvas.
        """

        dates = self.dates_list_former()

        x1 = coords[0][0]
        y1 = coords[0][1]
        x2 = coords[1][0]
        y2 = coords[1][1]

        self.rects = []

        number = 0
        for yIndex, yCoord in enumerate(y1):
            for xIndex, xCoord in enumerate(x1):
                rectTuple = reverse_tuple(get_quotient_and_remainder(number, 53))
                
                self.create_rectangle(
                    xCoord, yCoord,
                    x2[xIndex], y2[yIndex],
                    tags=dates[rectTuple],
                    fill='#262626',
                    outline='#c2bfbc'
                )
                number+=1


    def paint_rects(self):

        """
            Paints rectangles that represent dates 
            existing in self.existingDates variable
        """

        for date in self.existingDates:
            self.itemconfig(self.find_withtag(date), fill='#f79102', outline='#f79102')


    def show_info(self, event):
        # retrieve the id of the canvas item that the cursor is over

        cursorTuple = event.widget.find_withtag("current")

        # Check empty tuple of the cursor data
        if cursorTuple == ():
            itemId = None
            self.currentId = None
            self.hide_info_rect(event)
            return None
        
        # Get the hoverd object's ID
        itemId = cursorTuple[0]

        # Check if the hovered object is a rectangle
        if event.widget.type(itemId) != "rectangle" or self.gettags(itemId)[0] == 'infoRect':
            self.currentId = None
            self.hide_info_rect(event)
            return None
        
        # Check if the ID has been changed
        if itemId != self.currentId:
            self.currentId = itemId
            self.hide_info_rect(event)
            self.get_hovered_rectangle_coords()
            self.get_hovered_rectangle_date()
            self.draw_info_rect()

    
    def get_hovered_rectangle_coords(self):
        self.currentRectCoords = self.coords(self.currentId)


    def get_hovered_rectangle_date(self):
        self.currentRectDate = self.gettags(self.currentId)[0]

    
    def draw_info_rect(self):

        rectWidth = 84
        rectHeight = 20

        padBottom = 2

        x0 = self.currentRectCoords[0]
        y0 = self.currentRectCoords[1]
        x1 = self.currentRectCoords[2]

        selectedRectWidth = abs(x1-x0)

        self.create_rectangle(
            x0+selectedRectWidth/2-rectWidth/2-1, y0-padBottom,
            x0+selectedRectWidth/2+rectWidth/2, y0-rectHeight-padBottom,
            fill='#545351',
            tags='infoRect',
            outline='#c2bfbc',
        )

        self.create_text(
            x0+selectedRectWidth/2, y0-padBottom,
            text=self.currentRectDate,
            anchor='s',
            tags='text',
            font=('Prestige Elite Std', 12, 'bold'),
            fill='#c2bfbc'           
        )

    
    def hide_info_rect(self, event):
        cursorTuple = event.widget.find_withtag("text")
        if cursorTuple:
            textWidgetID = cursorTuple[0]
            self.delete(textWidgetID)

        cursorTuple = event.widget.find_withtag("infoRect")
        if cursorTuple:
            infoRectWidgetID = cursorTuple[0]
            self.delete(infoRectWidgetID)
