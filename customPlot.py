import tkinter as tk
import numpy as np
from handy import *


class CustomPlot(tk.Canvas):

    def __init__(self, master, width, height):
        # Background colour of the canvas
        self.bg = '#131912'

        super().__init__(master=master, width=width, height=height, bg=self.bg)

        # Geometrical parameters of the canvas
        self.width = width
        self.height = height

        # The space between the end of an axes and a border of the canvas in pixels
        self.pad = 10

        # The coordinates of the origin
        self.zeroX = 45
        self.zeroY = self.height - 20

        # x- and y-axes lenghts
        self.yAxesLength = self.zeroY-self.pad
        self.xAxesLength = self.width-self.pad-self.zeroX

        # The space between the end of y-axes and its the greates tick in pixels
        self.yAxPad = 15

        # The width of a bar
        self.barWidth = 10

        self.axesWidth = 4

        self.axesColour = "#dc6601"
        self.textColour = '#df5705'
        self.barsColour = '#f36b19'
        self.barsOtline = '#131912'

        self.textFont = ('Prestige Elite Std', 10)
        
        
    def create_axes(self):
        # x-axes
        self.create_line(
            self.zeroX, self.zeroY,
            self.width-self.pad, self.zeroY,
            fill=self.axesColour, capstyle='round',
            width=self.axesWidth,
        )

        # y-axes
        self.create_line(
            self.zeroX, self.zeroY,
            self.zeroX, self.pad,
            fill=self.axesColour, capstyle='round',
            width=self.axesWidth,
        )


    def draw_data(self, data:dict):
        # Draw axes
        self.create_axes()

        X = data.keys()
        Y = data.values()
        nXTicks = len(data)
        xStep = self.get_xTicks(nXTicks)
        maxValue = max(Y)

        self.draw_xdata(X, xStep)
        self.draw_ydata(maxValue)
        self.draw_rects(
            Y, 
            self.get_coef(maxValue), 
            self.zeroY-self.axesWidth,
            xStep
        )

    
    def draw_xdata(self, data, xStep):

        textPad = 10
        yTextCoord = self.zeroY+textPad
        for index, xData in enumerate(data):
            xTextCoord = self.zeroX+xStep*(index+1)
            
            # Draw ticks
            self.create_line(
                xTextCoord, self.zeroY-self.axesWidth/2, 
                xTextCoord, self.zeroY+self.axesWidth/2,
                width=4,
            )
            
            # Draw labels
            self.create_text(
                xTextCoord, yTextCoord, 
                text=xData, fill=self.textColour,
                font=self.textFont,
            )


    def draw_ydata(self, maxValue, roundDigits=2):
        nOfTicks = 4

        yStep = int(round((self.yAxesLength-self.yAxPad)/nOfTicks))
        
        yTick = round(maxValue/nOfTicks, roundDigits)
        textPad = 25

        xTextCoord = self.zeroX-textPad
        for index in range(nOfTicks):
             
            yTextCoord = self.zeroY-yStep*(index+1)
            
            yText = yTick*(index+1)

            # Create ticks
            self.create_line(
                self.zeroX+self.axesWidth/2, yTextCoord, 
                self.zeroX-self.axesWidth/2, yTextCoord,
                width=4
            )

            # Create values
            self.create_text(
                xTextCoord, yTextCoord, 
                text=str(yText), fill=self.textColour,
                font=self.textFont
            )

        
    def draw_rects(self, data, coef, bottomY, xStep):
        
        barShift = int(self.barWidth/2)
        for index, value in enumerate(data):
            barHeight = int(coef*value)
            
            xRectCoord = self.zeroX+xStep*(index+1)

            self.create_rectangle(
                xRectCoord-barShift, bottomY-barHeight, 
                xRectCoord+barShift, bottomY, 
                fill=self.barsColour, outline=self.barsOtline,
                width=2
            )


    def get_max_bar(self, data:list):
        
        if data:
            totals = np.zeros(len(data[0]))
        else:
            print('Empty dictionary')
            return None
        
        
        for dataList in data:
            totals += dataList

        maxTotal = np.max(totals)

        return maxTotal


    def get_coef(self, maxValue):
        return (self.yAxesLength - self.yAxPad)/maxValue
    
    
    def get_xTicks(self, nOfTicks):
        return int(self.xAxesLength/(nOfTicks+1))
    

    def form_bottoms_tops(self, data:list):
    
        h = (len(data))
        w = len(data[0])

        if data:
            tops = np.zeros((h, w))
            bottoms = np.zeros((h, w))
        else:
            print('No data')
            return None
        
        term = np.zeros(w)
        for index, dataList in enumerate(data):
            bottoms[index] += term
            term += dataList
            tops[index] += term

        maxValue = self.get_max_bar(data)
        k = self.get_coef(maxValue)

        return (np.around(k*bottoms), np.around(k*tops))
        

    def draw_mult_rects(self, xStep, zeroLevel, bottoms, tops):

        h, w = np.shape(bottoms)
        barShift = int(self.barWidth/2)
        greenIncr = 30
        blueIncr = 30
        for row in range(h):
            xCoord = 0
            barColour = change_color(self.barsColour, (0, greenIncr*(row+1), blueIncr*row))
            for col in range(w):
                xCoord = self.zeroX+xStep*(col+1)

                self.create_rectangle(
                    xCoord-barShift, zeroLevel-tops[row][col], 
                    xCoord+barShift, zeroLevel-bottoms[row][col], 
                    fill=barColour, outline=self.barsOtline,
                    width=2
                )
    

    def draw_mult_bars(self, datesList:list, data:dict):
        self.delete('all')

        # Draw axes
        self.create_axes()

        nXTicks = len(data)
        xStep = self.get_xTicks(nXTicks)
        maxValue = self.get_max_bar(list(data.values()))
        bottoms, tops = self.form_bottoms_tops(list(data.values()))

        self.draw_xdata(datesList, xStep)
        self.draw_ydata(maxValue)

        self.draw_mult_rects(
            xStep, 
            self.zeroY-self.axesWidth,
            bottoms,
            tops,
            )
        