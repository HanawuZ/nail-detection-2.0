import tkinter as tk
import os
import cv2
import sys
from PIL import Image, ImageTk


cap = cv2.VideoCapture(0)

mainwindows = tk.Tk(screenName="Read-Nail-Lighting")
# mainwindows.geometry("680x800")
# mainwindows.resizable(width=True, height=True)
mainwindows.attributes("-fullscreen", True)
mainwindows.bind('<Escape>', lambda e: mainwindows.quit())

mainwindows['background']='#1f1f1f'

labelCamera = tk.Label(mainwindows, borderwidth=0)
labelCamera.pack(padx=20, side=tk.LEFT, anchor=tk.CENTER)



def show_camera():
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    convImg = Image.fromarray(cv2image)
    convImg = convImg.resize((int(mainwindows.winfo_screenheight()*(4/3) - 20 ), int(mainwindows.winfo_screenheight() - 20))) # Resize image from camera
    # size = convImg.size
    # print(size)
    imgTk = ImageTk.PhotoImage(convImg)
    labelCamera.imgtk = imgTk
    labelCamera.configure(image=imgTk)
    labelCamera.after(5, show_camera) # Recursive to read camera image

show_camera()
mainwindows.mainloop()
