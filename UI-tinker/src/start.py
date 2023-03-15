import tkinter as tk
import os
import cv2
import sys
from PIL import Image, ImageTk

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


cap = cv2.VideoCapture(0)

mainwindows = tk.Tk(screenName="Read-Nail-Lighting")
# mainwindows.geometry("680x800")
# mainwindows.resizable(width=True, height=True)
mainwindows.attributes("-fullscreen", True)
mainwindows.bind('<Escape>', lambda e: mainwindows.quit())

mainwindows['background'] = '#1f1f1f'

labelCamera = tk.Label(mainwindows, borderwidth=0)
labelCamera.pack(padx=20, side=tk.LEFT, anchor=tk.CENTER)

submitButton = tk.Button(mainwindows, text="test")
submitButton.pack()

data = {
    'country': ['A', 'B', 'C', 'D', 'E'],
    'gdp_per_capita': [45000, 42000, 52000, 49000, 47000]
}

df1 = pd.DataFrame(data)


def plot():
    global df1
    figure1 = plt.Figure(figsize=(5, 3), dpi=100)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, mainwindows)
    bar1.get_tk_widget().pack(side=tk.RIGHT,anchor=tk.NE,pady=50, padx=20)
    # df1 = df1[['country', 'gdp_per_capita']].groupby('country').sum()
    df1.plot(kind='line', legend=True, ax=ax1)
    ax1.set_title('Country Vs. GDP Per Capita')

plot()

def show_camera():
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    
    """
    In this case it a show Camera image to Tkinter UI and will recursive this function all time
    """
    convImg = Image.fromarray(cv2image)
    convImg = convImg.resize((int(mainwindows.winfo_screenheight(
    )*(4/3) - 100), int(mainwindows.winfo_screenheight() - 100)))  # Resize image from camera
    imgTk = ImageTk.PhotoImage(convImg)
    labelCamera.imgtk = imgTk
    labelCamera.configure(image=imgTk)
    labelCamera.after(5, show_camera)  # Recursive to read camera image


show_camera()
mainwindows.mainloop()
