import tkinter as tk
import datetime
import numpy as np


class DaysCounter(tk.Canvas):

    """
        The class is the tkinter.Canvas widget. 
        The widget draws 368 rectangles 
        that represent each day from today's day 
        to the day that was 368 days ago.
    """

    def __init__(self, master, width, existingDates):

        N = 368

        self.strN = 4
        
        self.colN = int(N/self.strN)

        self.rectWidth = width/(2*self.colN+1)

        self.k = (2*self.strN+1)/(2*self.colN+1)

        height = int(self.k*width)

        super().__init__(master=master, width=width, height=height)

        self.W = width
        self.H = height

        self.dates = self.dates_list_former()

        self.create_rects(self.form_coords())

        self.existingDates = existingDates

        self.paint_rects()

    
    def form_coords(self):

        """
            Forms 4 vectors of x0, y0, x1, y1 coordinates 
            for each rectangle to display.
        """
        

        x1CoordsArray = np.zeros(self.colN)
        y1CoordsArray = np.zeros(self.strN)

        for index, coord in enumerate(y1CoordsArray):
            y1CoordsArray[index] += self.rectWidth*(index+1)+self.rectWidth*index

        for index, coord in enumerate(x1CoordsArray):
            x1CoordsArray[index] += self.rectWidth*(index+1)+self.rectWidth*index

        x2CoordsArray = x1CoordsArray + self.rectWidth
        y2CoordsArray = y1CoordsArray + self.rectWidth

        return [(x1CoordsArray, y1CoordsArray), (x2CoordsArray, y2CoordsArray)]
    

    def dates_list_former(self):

        """
            The method forms a list of dates from today
            to the day that was 368 days ago.
        """

        # Today's date
        today = datetime.date.today()

        # Number of dates to create
        Ndays = 368

        # 368 days delta
        delta = datetime.timedelta(days=Ndays)

        # One day delta 
        dateIncrement = datetime.timedelta(days=1)

        # 368 days ago date
        yearAgo = today - delta

        # Empty list to store dates
        dates = []

        # The first element in the list
        date = yearAgo

        # Forms the dates list
        for i in range(Ndays):
            date += dateIncrement
            dates.append(str(date))

        return dates


    def create_rects(self, coords):

        """
            Takes the coordinates for rectangles 
            and displays them on the canvas.
        """

        x1 = coords[0][0]
        y1 = coords[0][1]
        x2 = coords[1][0]
        y2 = coords[1][1]

        self.rects = []

        number = 0
        for yIndex, yCoord in enumerate(y1):
            for xIndex, xCoord in enumerate(x1):
                
                self.create_rectangle(
                    xCoord, yCoord,
                    x2[xIndex], y2[yIndex],
                    tags=self.dates[number]
                )
                number+=1


    def paint_rects(self):

        """
            Paints rectangles that represent dates 
            existing in self.existingDates variable
        """

        for date in self.existingDates:
            self.itemconfig(self.find_withtag(date), fill='green')
