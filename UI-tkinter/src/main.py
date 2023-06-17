import tkinter as tk
import tkinter.font as font
import ttkbootstrap as ttk
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
import asyncio
import websockets
import subprocess
import datetime

PRIMARY_COLOR = "#C1C1C1"
# subprocess.run(["python"])

_id = 1

class Patient:
    
    def __int__(self):
        pass
    
    def set_patient_data(self,patient_id):
        global _id
        self.patient_id = patient_id
        self.date_time = datetime.datetime.now()
        self.id = _id
        _id+=1
        
        

def Normalize(deg):
    return ((deg ) / (90)) * (1 - (-1)) + (-1)

class View(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.box_centroid = np.array([(400)//2 , (400)//2])
        self.bounding_box = np.array([[
            [self.box_centroid[0]+150,self.box_centroid[1]+50],
            [300,self.box_centroid[1]+50],
            [300,400-180],
            [self.box_centroid[0]+150,400-180]
        ]])
        
        # form variables
        self.patient = Patient()
        
        # Initialize attribute value
        self.record_status = False
        self.x=[0]
        self.y=[0]
        
        # Create lock object for mutual exclusion lock
        self.lock = mp.Lock()
        
        self.websocket = None

        # Setup camera
        self.cap = cv2.VideoCapture(0)
        
        # Make UI fullscreen.
        # self.attributes("-fullscreen", True)
        # self.geometry("500x200")
        
        self.bind("<Escape>", lambda e: self.quit())
        
        # Set rgb background color "#C1C1C1"
        # self["background"] = PRIMARY_COLOR
        
        self.style = ttk.Style()
        self.style.configure(".", font=("Helvetica", 20))
        
        
        self.col1 = tk.Frame(self,width=750,height=600,borderwidth=1, relief="solid")
        self.col1.pack(side=tk.LEFT, anchor=tk.CENTER, padx=(0,0))
        self.col1.grid_propagate(0)
        
        self.camera_label = tk.Label(self.col1, text="Inference", font=("Helvetica", 26))
        self.camera_label.grid(row=1)
        
        # Add camera
        self.camera = tk.Label(self.col1)
        self.camera.grid(row=2,pady=(0,0), padx=(20,20))
        
        
        self.col2 = tk.Frame(self,width=600,height=600, background=PRIMARY_COLOR)
        self.col2.pack(side=tk.LEFT, anchor=tk.CENTER, padx=(0,0))
        self.col2.grid_propagate(0)
        
        self.fig = Figure(figsize=(5.5, 4), dpi=100, facecolor="#FFFFFF")
        self.ax = self.fig.add_subplot(1, 1, 1)
    
        self.graph_row = tk.Label(self.col2)
        self.graph_row.grid(row=1,pady=(0,0), padx=(0,0))
        
        self.x_label = tk.Label(self.col2, text="Time(s)", font=("Helvetica", 18))
        self.x_label.grid(row=2,pady=(0,20), padx=(0,0))
        # create a canvas to display the plot
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_row)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(anchor=tk.CENTER, padx=(0,0), fill=tk.BOTH, pady=(0,20))
        
        self.col3 = tk.Frame(self,width=600,height=600,borderwidth=1, relief="solid")
        self.col3.pack(side=tk.LEFT, anchor=tk.CENTER, padx=(0,0))
        self.col3.grid_propagate(0)
        
        
        self.patient_id_label = ttk.Label(master=self.col3, text="Patient ID", width=50,  font=("Helvetica", 18), borderwidth=1, relief="solid")
        self.patient_id_label.grid(row=1,padx=5)
        
        self.patient_id_container = tk.Frame(master=self.col3, width=50, borderwidth=1, relief="solid")
        self.patient_id_container.grid(row=2, padx=0, pady=5)
        
        self.ent = tk.Entry(master=self.patient_id_container)
        self.ent.pack()
        
            
        
        self.anim = animation.FuncAnimation(self.fig, self.animate, interval=500)

        self.button_row = tk.Label(self.col2)
        # self.button_row.config(bg=PRIMARY_COLOR)
        self.button_row.grid(row=3)
        
        # Add button to UI
        self.button = ttk.Button(self.button_row, text="Start",
                                command=self.startRecord, width=12, bootstyle="outline")
        
        self.show_text_btn = ttk.Button(self.col3, text="Show Text", command=self.show_text)
        self.show_text_btn.grid(row=3)
        
        self.show_text = tk.Label(self.col3)
        self.show_text.grid(row=4)
        
        self.show_date = tk.Label(self.col3)
        self.show_date.grid(row=5)
        
        self.show_id = tk.Label(self.col3)
        self.show_id.grid(row=6)

        self.button.pack(padx=0, pady=(20,0), side=tk.RIGHT, anchor=tk.CENTER, ipadx=20, ipady=20)
        
        self.show_camera()
        
        # Show UI
        self.mainloop()

    def show_text(self):
        patient_id = self.ent.get()  # Get the text from the Entry widget
        self.patient.set_patient_data(patient_id)
        self.show_text.config(text=self.patient.patient_id)  # Set the text of the Label widget
        self.show_date.config(text=self.patient.date_time)  # Set the text of the Label widget
        self.show_id.config(text=self.patient.id)  # Set the text of the Label widget

    def animate(self, i):
        # update the data for the plot
        self.lock.acquire()
        
        xs = self.x[-40:]
        ys = self.y[-40:]
        self.ax.clear()
        self.ax.plot(xs,ys)
        self.lock.release()
        self.ax.set_ylim(0, 2)
    
    async def connect(self):
        self.websocket = await websockets.connect("ws://0.0.0.0:8080")
    
    async def pressServo(self):
        await self.connect()
        if self.record_status == True:
            await self.websocket.send("1000")
        else :
            await self.websocket.send("1900")
        await self.websocket.close()
    
    # Change state of variable to start functions
    def startRecord(self):
        self.record_status = not self.record_status
        asyncio.run(self.pressServo())
        """
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
        """
    def show_camera(self):
        ret, self.frame = self.cap.read()
        if(ret):
            cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            
            gray_frame = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)
            contrast_frame = cv2.convertScaleAbs(gray_frame, alpha=3.0, beta=-300)      
            #cv2image = contrast_frame
            in_roi_frame = contrast_frame[self.box_centroid[0]:401, self.box_centroid[1]:401]
            
            if self.record_status:
                cv2.putText(cv2image, "Running",(30,30), cv2.FONT_HERSHEY_DUPLEX, 1.0, [255, 0, 0],2)
            else:
                cv2.putText(cv2image, "Idle",(30,30), cv2.FONT_HERSHEY_DUPLEX, 1.0, [0, 255, 0],2)
   
            # Draw bounding box on frame.
            cv2.polylines(cv2image,self.bounding_box,True,(0,255,255))
            
            # Calculate average intensity of interesting nail area
            avg_intensity = np.mean(in_roi_frame)
            
            avg_intensity = (avg_intensity)/(255)
            
            avg_intensity = avg_intensity-0.15
            avg_intensity = avg_intensity/0.1
            
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
            self.camera.after(5, self.show_camera)
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

def main():
    test = View()
    

if __name__ == "__main__":
    main()
