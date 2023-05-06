from tkinter import *
import cv2
from PIL import Image, ImageTk
import pathlib
import os
import pigpio
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.animation as animation
style.use("ggplot")
import numpy as np
import multiprocessing as mp

PRIMARY_COLOR = "#C1C1C1"

def Normalize(deg):
    return ((deg ) / (90)) * (1 - (-1)) + (-1)

class View(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.box_centroid = np.array([(400)//2 , (400)//2])
        self.bounding_box = np.array([[
            [self.box_centroid[0],self.box_centroid[1]],
            [450,self.box_centroid[1]],
            [450,400-50],
            [self.box_centroid[0],400-50]
        ]])
        
        # Initialize attribute value
        self.record_status = False
        self.x=[0]
        self.y=[0]
        
        # Create lock object for mutual exclusion lock
        self.lock = mp.Lock()
        
        # Setup camera
        self.cap = cv2.VideoCapture(0)
        
        # Make UI fullscreen.
        self.attributes("-fullscreen", True)
        
        self.bind("<Escape>", lambda e: self.quit())
        
        # Set rgb background color "#C1C1C1"
        self["background"] = PRIMARY_COLOR

        # Add camera
        self.camera = Label(self, borderwidth=2, relief="solid")
        self.camera.pack(padx=100, side=LEFT, anchor=CENTER)
        
        self.col2 = Frame(self,width=1000,height=1000, background=PRIMARY_COLOR)
        self.col2.pack(side=RIGHT, anchor=CENTER, padx=(50,50))
        self.col2.grid_propagate(0)

        self.fig = Figure(figsize=(7, 7), dpi=100, facecolor=PRIMARY_COLOR)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_xlabel("Time(s)")
    
        self.graph_row = Label(self.col2, borderwidth=2, width=101, height=20, background=PRIMARY_COLOR)
        self.graph_row.grid(row=1,pady=(40,40), padx=(5,5))
        
        # create a canvas to display the plot
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_row)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(anchor=CENTER, padx=(100,100), fill=BOTH)
        
        myFont = font.Font(size=30)

        self.button_row = Label(self.col2, background=PRIMARY_COLOR)
        self.button_row.grid(row=2)
        
        # Add button to UI
        self.button = Button(self.button_row, text="Start",font=myFont, command=self.startRecord, width=10, height=2)
        self.button.pack(padx=20, side=RIGHT, anchor=CENTER)
        
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
        print(self.record_status)
        # Create record process with attribute VideoCapture object
        if self.record_status == True:
            
            # Create record process object
            self.record = Record(cap=self.cap)
            
            # Start record process
            self.record.start()
        
        # Destroy record process object when stop recording
        else :
            self.record.terminate()
            del self.record

    def show_camera(self):
        ret, self.frame = self.cap.read()
        if(ret):
            cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            
            gray_frame = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)
            contrast_frame = cv2.convertScaleAbs(gray_frame, alpha=3.0, beta=-200)      

            in_roi_frame = contrast_frame[self.box_centroid[0]:401, self.box_centroid[1]:401]
            
            if self.record_status:
                cv2.putText(cv2image, "Running",(30,30), cv2.FONT_HERSHEY_DUPLEX, 1.0, [255, 0, 0],2)
            else:
                cv2.putText(cv2image, "Idle",(30,30), cv2.FONT_HERSHEY_DUPLEX, 1.0, [0, 255, 0],2)
   
            # Draw bounding box on frame.
            cv2.polylines(cv2image,self.bounding_box,True,(0,255,255))
            
            # Calculate average intensity of interesting nail area
            avg_intensity = np.mean(in_roi_frame)
            
            self.lock.acquire()
            self.x.append(self.x[-1]+1)
            self.y.append(avg_intensity)
            self.lock.release()

            convImg = Image.fromarray(cv2image)
            convImg = convImg.resize((700, 700))
            imgTk = ImageTk.PhotoImage(convImg)
            self.camera.imgtk = imgTk
            self.camera.configure(image=imgTk)
            
            # will call function record when show_camera run after 2 ms
            # self.camera.after(2, self.record)
            # will call recursive function whne pass to 2 ms
            self.camera.after(2, self.show_camera)
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
                
"""               
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
        self.servo.value = self.Normalize(15)
        time.sleep(0.5)
        self.servo.detach()
"""

def main():
    test = View()
    

if __name__ == "__main__":
    main()
