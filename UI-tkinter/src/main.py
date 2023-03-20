from tkinter import *
import cv2
from PIL import Image, ImageTk
import pathlib
import os
from gpiozero import Servo
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from random import randint
import numpy as np
import multiprocessing as mp

class View(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.box_centroid = np.array([(180+450)//2 , (80+400)//2])
        self.bounding_box = np.array([[
            [self.box_centroid[0],self.box_centroid[1]],
            [450,self.box_centroid[1]],
            [450,400-50],
            [self.box_centroid[0],400-50]
        ]])

        self.record_status = False
        
        # Initialize Servo
        self.servo = Servo(17)
        self.servo.min()
        time.sleep(0.5)
        self.servo.detach()
        
        # Create lock object for mutual exclusion lock
        self.lock = mp.Lock()
        
        # Setup camera
        self.cap = cv2.VideoCapture(0)
        
        # Set UI widthxheigth
        self.geometry("1900x600")
        
        # self.attributes("-fullscreen", True)
        self.bind('<Escape>', lambda e: self.quit())
        self["background"] = "#161616"

        
        self.camera = Label(self, borderwidth=0)
        self.camera.pack(padx=20, side=LEFT, anchor=CENTER)
        self.button = Button(self, text="Record", command=self.startRecord, height=5, width=20)
        self.button.pack(padx=20, side=RIGHT, anchor=CENTER)
        
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.x=[0]
        self.y=[0]        
        
        # create a canvas to display the plot
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=RIGHT, anchor=CENTER)
        
        self.anim = animation.FuncAnimation(self.fig, self.animate, interval=1000)

        self.show_camera()
        
        # Show UI
        self.mainloop()
    
    def animate(self, i):
        # update the data for the plot
        self.lock.acquire()
        
        xs = self.x[-40:]
        ys = self.y[-40:]
        self.ax.clear()
        self.ax.plot(xs,ys)
        self.lock.release()
        self.ax.set_ylim(0, 255)
        
    # Change state of variable to start functions
    def startRecord(self):
        self.record_status = not self.record_status
        
        # Create record process with attribute VideoCapture object
        if self.record_status == True:
            
            # Create record and servo process object
            self.record = Record(cap=self.cap)
            self.servo_process = ServoProcess(servo=self.servo)
            
            
            # Start record process
            self.record.start()
            self.servo_process.start()
        
        # Destroy record process object when stop recording
        else :
            self.record.terminate()
            self.servo_process.terminate()
            del self.record
            del self.servo_process
            self.servo.min()
            time.sleep(0.5)
            self.servo.detach()
        

    def show_camera(self):
        ret, self.frame = self.cap.read()
        if(ret):
            cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            """
            if self.record_status == True:
                cv2.putText(cv2image,"Running",(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
            else :
                cv2.putText(cv2image,"Not running",(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
            """
            gray_frame = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)
            contrast_frame = cv2.convertScaleAbs(gray_frame, alpha=3.0, beta=-200)      # Contrast values 3

            in_roi_frame = contrast_frame[self.box_centroid[0]:401, self.box_centroid[1]:401]

            # Draw bounding box on frame.
            cv2.polylines(cv2image,self.bounding_box,True,(0,255,255))
            
            # Store frame intensity value.
            avg_intensity = np.mean(in_roi_frame)
            
            self.lock.acquire()
            self.x.append(self.x[-1]+1)
            self.y.append(avg_intensity)
            self.lock.release()

            convImg = Image.fromarray(cv2image)
            convImg = convImg.resize((480, 640))
            imgTk = ImageTk.PhotoImage(convImg)
            self.camera.imgtk = imgTk
            self.camera.configure(image=imgTk)
            
            # will call function record when show_camera run after 5 ms
            # self.camera.after(5, self.record)
            # will call recursive function whne pass to 5 ms
            self.camera.after(10, self.show_camera)
        else:
            self.cap.release()
            self.camera.destroy()


# ***************** path to Multiprocessing (Recording) **********************
class Record(mp.Process):
    def __init__(self, cap):
        mp.Process.__init__(self)
        self.cap = cap
        vid_output_path = os.path.join(pathlib.Path(__file__).parent,"output_sample.avi")
        self.video_recorder = cv2.VideoWriter(vid_output_path,cv2.VideoWriter_fourcc("M","J","P","G"), 30, (640,480))
    
    # Process start running this method when process is started
    def run(self):
        print("Run Record")
        self.record()

    # Record video, destroy this object when press recording
    def record(self):
        while(self.cap.isOpened()):
            check,frame = self.cap.read()
            if check == False:
                break
            else:
                cv2.putText(frame,"Recording",(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
                self.video_recorder.write(frame)
                cv2.waitKey(1)
                
                
class ServoProcess(mp.Process):
    def __init__(self, servo):
        mp.Process.__init__(self)
        self.servo = servo
     
    # Start press servo
    def run(self):
        self.pressServo()

    def Normalize(self,deg):
        return ((deg ) / (90)) * (1 - (-1)) + (-1)
    
    def pressServo(self):
        time.sleep(1)
        self.servo.value = self.Normalize(75)
        time.sleep(0.5)
        self.servo.detach()    
    
# ***************** reading code satrt from this *****************
def main():
    test = View()
    


if __name__ == "__main__":
    main()
    # print()