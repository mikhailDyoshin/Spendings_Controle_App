import tkinter as tk


class MyCanvas(tk.Canvas):

    def __init__(self, master, width, height):

        super().__init__(master=master, width=width, height=height)

        rect1 = self.create_rectangle(50, 50, 150, 150, fill="blue", tags='2022-04-01')
        rect2 = self.create_rectangle(200, 50, 300, 150, fill="red", tags='2022-04-02')
        rect3 = self.create_rectangle(50, 200, 150, 300, fill="green", tags='2022-04-03')

        self.bind("<Motion>", self.show_info)

        self.currentId = None


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
            self.get_hovered_rectangle_coords()
            self.get_hovered_rectangle_date()
            self.draw_info_rect()

    
    def get_hovered_rectangle_coords(self):

        self.currentRectCoords = self.coords(self.currentId)


    def get_hovered_rectangle_date(self):
        self.currentRectDate = self.gettags(self.currentId)[0]

    
    def draw_info_rect(self):

        rectWidth = 60
        rectHeight = 15

        padBottom = 2

        x0 = self.currentRectCoords[0]
        y0 = self.currentRectCoords[1]
        x1 = self.currentRectCoords[2]

        selectedRectWidth = abs(x1-x0)

        self.create_rectangle(
            x0+selectedRectWidth/2-rectWidth/2, y0-padBottom,
            x0+selectedRectWidth/2+rectWidth/2, y0-rectHeight-padBottom,
            fill='#fff',
            tags='infoRect'
        )

        self.create_text(
            x0+selectedRectWidth/2, y0-padBottom,
            text=self.currentRectDate,
            anchor='s',
            tags='text'           
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




# create a tkinter window
root = tk.Tk()
    

# create a canvas
canvas = MyCanvas(root, width=400, height=400)
canvas.pack()
    
# start the tkinter event loop
root.mainloop()