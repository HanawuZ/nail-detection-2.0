from tkinter import *
import cv2
from PIL import Image, ImageTk
import pathlib
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from time import sleep
import multiprocessing as mp
import matplotlib.animation as animation
import numpy as np
from gpiozero import Servo

#! BUG:
# Shortly after press `start` again, program suddenly terminate. Fix this!!


class View(Tk):
    def __init__(self):
        self.VIDEO_TEST_PATH = os.path.join(pathlib.Path(__file__).parent, "output6.mp4")
        
        # recording status
        self.recorder = False
        self.figure= plt.Figure(figsize=(10, 6), dpi=100)
        
        # creating a lock object
        self.lock = mp.Lock()
        self.plot_status = False
        
        # Creating array of x data and y data.
        self.list_x = [0]
        self.list_y = [0]
        
        # Create region of interest coordination
        """
          x   y
        (210,125)----------(425,125)
            |                  |
            |                  |
            |                  |
        (210,330)----------(425,330)
        """
        self.roi = np.array([[
            [210,125],
            [425,125],
            [425,330],
            [210,330]
        ]])
        
        self.valueOfXPlot = 0
        
        Tk.__init__(self)
        # self.cap = cv2.VideoCapture(self.VIDEO_TEST_PATH) # Demo Video
        self.cap = cv2.VideoCapture(0) # Webcam
        self.servo = Servo(17)
        self.servo.min()
        sleep(0.5)
        self.servo.detach()
        
        # self.geometry("800x600")
        # self.attributes("-fullscreen", True)
        self.geometry("%dx%d" % (self.winfo_screenwidth(), self.winfo_screenheight()))
        
        self.bind('<Escape>', lambda e: self.quit())
        self["background"] = "#e1e1e1"
        
        # self.mainWindows = T"k(screenName="New Windows")
        # self.mainWindows.geometry("800x600")

        self.camera = Label(self, borderwidth=0)
        self.camera.pack(padx=20, side=LEFT, anchor=CENTER)
            
        self.button = Button(self, text="Start", command=self.startRecord, height=5, width=20)
        self.button.pack(padx=20, side=RIGHT, anchor=CENTER)
        

    # Change state of variable to start functions
    def startRecord(self):
        
        # When starting record, press servo
        self.recorder = not self.recorder
        self.pressServo()

        # Delete instance of object VideoCapture to free camera holding
        del self.cap
        self.cap = cv2.VideoCapture(self.VIDEO_TEST_PATH)


    # Function to records or start save data (example start servo and record camera)
    def record(self):
        if(self.recorder):
            # print("record")
            pass
        # will recursive fnctions
    
    # Method for pressing Servo
    def pressServo(self):
    
        # REF : https://stackoverflow.com/questions/25149543/record-opencv-video-during-tkinter-mainloop
        def Normalize(deg):
            return ((deg ) / (90)) * (1 - (-1)) + (-1)
        
        if self.recorder:
            self.servo.value = Normalize(75)
        else:
            self.servo.min()
        sleep(0.5)
        self.servo.detach()

    def show_camera(self):
        
        status,frame = self.cap.read()
        
        # If there's no frame from video reading, then delete cap instance and recreate it for camera capture
        # After that, read camera frame
        if status == False:
            del self.cap
            self.cap = cv2.VideoCapture(0)
            self.recorder = False
            self.pressServo()
            self.plot_status = True
            status, frame = self.cap.read()

        
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Show recording status label
        # If video is recording, "Running" on current frame.
        if self.recorder :
            cv2.putText(cv2image,"Running",(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
            gray_frame = cv2.cvtColor(cv2image, cv2.COLOR_RGB2GRAY)
            contrast_frame = cv2.convertScaleAbs(gray_frame, alpha=3.0, beta=-200)
            in_roi_frame = contrast_frame[210:425,125:330]
            avg_intensity = np.mean(in_roi_frame)
            self.valueOfXPlot += 1
            self.lock.acquire()
            self.list_x.append(self.valueOfXPlot/30)
            self.list_y.append(avg_intensity)
            self.lock.release()

        # Else then show "Not Recording" on current frame.
        else :
            cv2.putText(cv2image,"Not Recording",(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
        
        if self.plot_status:
            self.plot()
    
        cv2.polylines(cv2image,self.roi,True,(0,255,255))

        convImg = Image.fromarray(cv2image)
        
        # Resize image from camera
        # Problem: resize image make ui slow
        # convImg = convImg.resize((int(self.winfo_screenheight()*(4/3) - 100), int(self.winfo_screenheight() - 100)))  
        imgTk = ImageTk.PhotoImage(convImg)
        self.camera.imgtk = imgTk
        self.camera.configure(image=imgTk)
        self.camera.after(2, self.record) # will call function record when show_camera run after 5 ms
        self.camera.after(2, self.show_camera) # will call recursive function whne pass to 5 ms
    
    # Method for embed plotting graph to UI
    def plot(self):
        
        # adding the subplot
        plot1 = self.figure.add_subplot(111)
        plot1.set_title("Sample Graph")

        # plotting the graph
        
        self.lock.acquire()
        plot1.plot(self.list_x, self.list_y)
        self.lock.release()
        
        bar1 = FigureCanvasTkAgg(self.figure, self)
        bar1.get_tk_widget().pack(side=RIGHT)

# *****************reading code satrt from this*****************
def main():
    test = View()
    test.show_camera()
    test.mainloop()


if __name__ == "__main__":
    main()
    # print()

