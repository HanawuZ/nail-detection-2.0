import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import animation, figure
from random import randint
import matplotlib.pyplot as plt
import numpy as np
import time
LARGEFONT =("Verdana", 35)
  
class tkinterApp(tk.Tk):
     
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {} 
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (CameraFrame, GraphFrame):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1,  respectively with
            # for loop
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(CameraFrame)
        
        self.mainloop()
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# first window frame startpage
class CameraFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
         
        # label of frame Layout 2
        label = ttk.Label(self, text ="Startpage", font = LARGEFONT)
        
        self.cap = cv2.VideoCapture(0)
        self.label1 = tk.Label(self)
        self.label1.grid(row=0, column=0)
        
        # putting the grid in its place by using
        # grid
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        button1 = ttk.Button(self, text ="Graph",
        command = lambda : controller.show_frame(GraphFrame))
     
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
        
        self.display_frames()
        
    def display_frames(self):
        # Get the latest frame and convert into Image
        cv2image= cv2.cvtColor(self.cap.read()[1],cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        # Convert image to PhotoImage
        imgtk = ImageTk.PhotoImage(image = img)
        self.label1.imgtk = imgtk
        self.label1.configure(image=imgtk)
        # Repeat after an interval to capture continiously
        self.label1.after(20, self.display_frames)
      
  
# second window frame page1
# Page for camera display
class GraphFrame(tk.Frame):
     
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Page 1", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
          
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="Camera",
                            command = lambda : controller.show_frame(CameraFrame))
        
        fig = figure.Figure()
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid(column=0, row=0)
        self.ax = fig.add_subplot(1, 1, 1)
        self.xs = []
        self.ys = []
        self.zs = []

        # putting the button in its place
        # by using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
        
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid(column=0, row=0)

        self.ani = animation.FuncAnimation(fig, self.animate, interval=5)
    def animate(self, event):
        self.xs.append(time.clock())
        self.ys.append(time.clock() + np.random.random())
        self.xs = self.xs[-100:]
        self.ys = self.ys[-100:]
        self.ax.clear()
        self.ax.plot(self.xs, self.ys)
if __name__ == "__main__":
    # Driver Code
    app = tkinterApp()