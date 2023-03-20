from random import randint
import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation


class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # create a label to display the video feed
        self.video_label = tk.Label(self)
        self.video_label.pack()
        
        
        # button to switch to page 2
        button = tk.Button(self, text="Go to Page 2",
                           command=lambda: controller.show_frame(Page2))
        button.pack()

        # start the video feed
        self.video_feed = cv2.VideoCapture(0)
        self.update_video_feed()
    
    def update_video_feed(self):
        # read a frame from the video feed
        ret, frame = self.video_feed.read()
        
        if ret:
            # convert the frame to tkinter-compatible format and display it
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = np.rot90(img)
            img = np.flipud(img)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(image=img)
            self.video_label.configure(image=img)
            self.video_label.image = img
        
        # schedule the next update
        self.after(10, self.update_video_feed)

class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
          # create a figure and axis for the plot
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.x=[0]
        self.y=[0]        
        # create a canvas to display the plot
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # create a button to switch back to the camera page
        button = tk.Button(self, text="Go to Camera Page",
                           command=lambda: controller.show_frame(Page1))
        button.pack(pady=10)
        
        # start the animation loop
        self.anim = animation.FuncAnimation(self.fig, self.animate, interval=100)
    
    def animate(self, i):
        # update the data for the plot
        self.x.append(i)
        self.y.append(randint(25,200))
        self.ax.clear()
        self.ax.plot(self.x,self.y)
  
        
class MainApplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        # create a container to hold all the frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        # add each page to the container
        for F in (Page1, Page2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(Page1)
        
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

app = MainApplication()
app.mainloop()
