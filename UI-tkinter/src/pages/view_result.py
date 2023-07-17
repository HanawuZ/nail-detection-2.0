import tkinter as tk
import ttkbootstrap as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.animation as animation
import numpy as np
style.use("ggplot")

class ViewResult(tk.Frame):
    def animate(self, i):   
        self.x.append(i) 
        self.y.append(self.sample_data[i])

        self.ax.clear()
        self.ax.plot(self.x,self.y)
        self.ax.set_ylim([0,110])

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.x = []
        self.y = []
        self.sample_data = [40,41,41,40,41,40,42,41,40,41,40,50,60,65,70,80,94,102,101,95,84,74,70,71,64,74,65,61,65,64,56,55,51,40,40,41,41,40,41,40,42,41,40]
        
        # Define a text to show that x axis is Time(in second)
        graph_label = tk.Label(self, text="Graph", font=("Helvetica", 26))
        graph_label.grid(row=1)

        # Define figure for graph with size of (5.5,4)
        self.fig = Figure(figsize=(5.5, 4), dpi=100, facecolor="#FFFFFF")
        self.ax = self.fig.add_subplot(1, 1, 1)

        # Define graph section
        graph_row = tk.Frame(self)
        graph_row.grid(row=2)

        # create a canvas to display the plot
        canvas = FigureCanvasTkAgg(self.fig, master=graph_row)
        canvas.draw()
        canvas.get_tk_widget().pack(anchor=tk.CENTER, fill=tk.BOTH)
        
        self.anim = animation.FuncAnimation(self.fig, self.animate, interval=500)
