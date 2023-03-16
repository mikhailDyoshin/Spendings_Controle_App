import tkinter as tk


class CustomPlot(tk.Canvas):

    def __init__(self, master, width, height, data):
        # Background colour of the canvas
        self.bg = '#131912'

        super().__init__(master=master, width=width, height=height, bg=self.bg)

        # Geometrical parameters of the canvas
        self.width = width
        self.height = height

        self.pad = 10

        # The
        self.zeroX = 45
        self.zeroY = self.height - 20

        # x- and y-axes lenghts
        self.yAxesLength = self.zeroY-self.pad
        self.xAxesLength = self.width-self.pad-self.zeroX

        self.axesWidth = 4

        self.axesColour = "#dc6601"
        self.textColour = '#df5705'
        self.barsColour = '#f36b19'

        self.textFont = ('Prestige Elite Std', 10)
        
        # Data to display
        self.data = data

        # The number of x-ticks
        self.nXTicks = len(data)

        self.xStep = int(self.xAxesLength/(self.nXTicks+1))

        # Draw axes
        self.create_axes()

        # Draw data
        self.draw_data()


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



    def draw_data(self):
        self.draw_xdata()
        self.draw_ydata()

    
    def draw_xdata(self):

        textPad = 10
        yTextCoord = self.zeroY+textPad
        for index, xData in enumerate(self.data.keys()):
            xTextCoord = self.zeroX+self.xStep*(index+1)
            
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


    def draw_ydata(self):
        nOfTicks = 4
        maxValue = max(list(self.data.values()))

        yStep = int(round(0.9*self.yAxesLength/nOfTicks, -1))
        yTick = int(round(maxValue/nOfTicks, -1))

        textPad = 25

        xTextCoord = self.zeroX-textPad
        for index in range(nOfTicks):
             
            yTextCoord = self.zeroY-yStep*(index+1)
            
            yText = yTick*(index+1)

            self.create_line(
                self.zeroX+self.axesWidth/2, yTextCoord, 
                self.zeroX-self.axesWidth/2, yTextCoord,
                width=4
            )
            self.create_text(
                xTextCoord, yTextCoord, 
                text=str(yText), fill=self.textColour,
                font=self.textFont
            )

        k = (self.zeroY-yTextCoord)/yText

        barWidth = 10
        barShift = int(barWidth/2)
        for index, value in enumerate(self.data.values()):
            barHeight = int(k*value)
            
            xRectCoord = self.zeroX+self.xStep*(index+1)

            self.create_rectangle(
                xRectCoord-barShift, self.zeroY-barHeight, 
                xRectCoord+barShift, self.zeroY-self.axesWidth, 
                fill=self.barsColour, outline='#db5200',
                width=2
            )
