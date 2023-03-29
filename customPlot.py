import tkinter as tk
import numpy as np
from handy import *


class CustomPlot(tk.Canvas):

    def __init__(self, master, width, height):
        # Background Color of the canvas
        self.bg = '#131912'

        super().__init__(master=master, width=width, height=height, bg=self.bg)

        # Geometrical parameters of the canvas
        self.width = width
        self.height = height

        # The space between the end of an axes and a border of the canvas in pixels
        self.pad = 10

        self.padY = 40

        # The coordinates of the origin
        self.zeroX = 45
        self.zeroY = self.height - 20

        # x- and y-axes lenghts
        self.yAxesLength = self.zeroY-self.padY
        self.xAxesLength = self.width-self.pad-self.zeroX

        # The space between the end of y-axes and its the greatest tick in pixels
        self.yAxPad = 15

        # The width of a bar
        self.barWidth = 10

        self.axesWidth = 4

        # The width of the legend
        self.legendWidth = 0

        self.axesColor = "#dc6601"
        self.textColor = '#df5705'
        self.barsColor = '#f36b19'
        self.barsOtline = '#131912'

        self.textFont = ('Prestige Elite Std', 10)

        # Cached data
        self.datesList = None
        self.data = None

        # Bars' colors
        self.barsColors = []
        
        
    def create_axes(self):
        # x-axes
        self.create_line(
            self.zeroX, self.zeroY,
            self.zeroX + self.xAxesLength, self.zeroY,
            fill=self.axesColor, capstyle='round',
            width=self.axesWidth,
        )

        # y-axes
        self.create_line(
            self.zeroX, self.zeroY,
            self.zeroX, self.zeroY-self.yAxesLength,
            fill=self.axesColor, capstyle='round',
            width=self.axesWidth,
        )


    # def draw_data(self, data:dict):
    #     # Draw axes
    #     self.create_axes()

    #     X = data.keys()
    #     Y = data.values()
    #     nXTicks = len(data)
    #     xStep = self.get_xTicks(nXTicks)
    #     maxValue = max(Y)

    #     self.draw_xdata(X, xStep)
    #     self.draw_ydata(maxValue)
    #     self.draw_rects(
    #         Y, 
    #         self.get_coef(maxValue), 
    #         self.zeroY-self.axesWidth,
    #         xStep
    #     )

    
    def draw_xdata(self, data, xStep, drawAllValues):

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
            
            if drawAllValues:
                self.create_text(
                    xTextCoord, yTextCoord, 
                    text=xData, fill=self.textColor,
                    font=self.textFont,
                )
            else:
                if index==0 or index==(len(data)-1):
                    # Draw labels
                    self.create_text(
                        xTextCoord, yTextCoord, 
                        text=xData, fill=self.textColor,
                        font=self.textFont,
                    )


    def draw_ydata(self, maxValue, roundDigits=2):
        nOfTicks = 4

        if bool(maxValue):
            pass
        else:
            maxValue = 10.0
        

        yStep = int(round((self.yAxesLength-self.yAxPad)/nOfTicks))
        
        yTick = maxValue/nOfTicks
        textPad = 25

        xTextCoord = self.zeroX-textPad
        for index in range(nOfTicks):
             
            yTextCoord = self.zeroY-yStep*(index+1)
            
            yText = round(yTick*(index+1), roundDigits)

            # Create ticks
            self.create_line(
                self.zeroX+self.axesWidth/2, yTextCoord, 
                self.zeroX-self.axesWidth/2, yTextCoord,
                width=4
            )

            # Create values
            self.create_text(
                xTextCoord, yTextCoord, 
                text=str(yText), fill=self.textColor,
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
                fill=self.barsColor, outline=self.barsOtline,
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
        if maxValue:
            return (self.yAxesLength - self.yAxPad)/maxValue
        return 0
    
    
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
            barColor = change_color(self.barsColor, (0, greenIncr*(row+1), blueIncr*row))
            self.barsColors.insert(0, barColor)
            for col in range(w):
                xCoord = self.zeroX+xStep*(col+1)

                self.create_rectangle(
                    xCoord-barShift, zeroLevel-tops[row][col], 
                    xCoord+barShift, zeroLevel-bottoms[row][col], 
                    fill=barColor, outline=self.barsOtline,
                    width=2
                )
    

    def draw_mult_bars_plot(self, datesList:list, data:dict, drawAllValues:bool=False):
        self.delete('all')

        self.datesList = datesList
        self.data = data

        # Draw axes
        self.create_axes()

        nXTicks = len(datesList)
        xStep = self.get_xTicks(nXTicks)

        maxValue = self.get_max_bar(list(data.values()))
        maxValue, exponent = get_exp_notation(maxValue)
        maxValue = float(maxValue)
        exponentSymbol = draw_power_symbol(exponent)

        self.draw_exponent(exponentSymbol)

        bottoms, tops = self.form_bottoms_tops(list(data.values()))

        self.draw_xdata(datesList, xStep, drawAllValues)
        self.draw_ydata(maxValue)


        self.draw_mult_rects(
            xStep, 
            self.zeroY-self.axesWidth,
            bottoms,
            tops,
            )
        

    def change_coords(self, legendWidth, barWidth):
        self.legendWidth = legendWidth

        self.xAxesLength = self.width-self.pad-self.zeroX-self.legendWidth

        self.barWidth = barWidth

    
    def draw_devider(self):

        a = self.create_line(
            self.width-self.legendWidth, 0,
            self.width-self.legendWidth, self.height,
            fill=self.axesColor, capstyle='round',
            width=2,
        )


    def draw_legends_content(self, keys:list):
        d = 16
        padX = 10
        padY = 20
        ovalSpace = d+15
        xInit = self.width-self.legendWidth+padX
        yInit = padY
        yStep = 30
        for index, key in enumerate(keys):
            self.create_oval(
                xInit, yInit+yStep*index,
                xInit+d, (yInit+d)+yStep*index,
                fill=self.barsColors[index])
            
            self.create_text(
                xInit+ovalSpace, yInit+yStep*index,
                anchor='nw',
                fill=self.textColor, text=key,
                font=self.textFont,
            )
        

    def draw_legend(self, keys:list, legendWidth:int=150, barWidth:int=10):
        self.change_coords(legendWidth, barWidth)

        self.draw_mult_bars_plot(self.datesList, self.data)

        self.draw_devider()

        self.draw_legends_content(keys)


    def draw_exponent(self, exponent:str):
        marginBottom = 10
        x = self.zeroX
        y = self.zeroY-self.yAxesLength - marginBottom
        self.create_text(x, y, text = exponent, fill=self.textColor, font=self.textFont, anchor='s')
