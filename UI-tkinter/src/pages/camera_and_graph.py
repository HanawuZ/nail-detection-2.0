import tkinter as tk
import ttkbootstrap as ttk
import cv2
from PIL import Image, ImageTk
import pathlib
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.animation as animation
import numpy as np
import multiprocessing as mp
import asyncio
import websockets
style.use("ggplot")
PRIMARY_COLOR = "#C1C1C1"
# subprocess.run(["python"])


class CameraAndGraph(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
		
        # # label of frame Layout 2
        # label = ttk.Label(self, text ="Startpage",)
		
		# # putting the grid in its place by using
		# # grid
        # label.grid(row = 0, column = 4, padx = 10, pady = 10)

        self.controller = controller

        """
        Define bounding_box ROI with 4 coordination
        (300,250)-------(350,250)
            |               |
            |               |
        (300,280)-------(350,280)
        """
        self.bounding_box = np.array([[
            (300,250),
            (350,250),
            (350,280),
            (300,280),
        ]])
        self.cap = cv2.VideoCapture(0)

        # Initialize attribute value
        # Define record status to determine that device is recording or not, default value is False
        self.record_status = False
        self.patient = self.controller.patient
        # Define 2 arrays
        # x is int array to store frame values
        # y float array to store intensity of nail
        self.x=[0]
        self.y=[0]
        
        # Create lock instance for mutual exclusion lock
        self.lock = mp.Lock()
            
        # Create websocket instance for websocket connection
        self.websocket = None

        # configure the appearance of Tkinter widgets.
        # Use font "Helvetica" with size of font `20`
        self.style = ttk.Style()
        self.style.configure(".", font=("Helvetica", 20))

        
        camera_col = tk.Frame(self,width=650,height=720,borderwidth=1, relief="solid")
        camera_col.pack(side=tk.LEFT)
        camera_col.grid_propagate(0)
        
        # Add camera label "หน้าจอแสดงผล"
        camera_label = tk.Label(camera_col, text="หน้าจอแสดงผล", font=("Helvetica", 26))
        camera_label.grid(row=1)
    
        camera_col.grid_rowconfigure(0, weight=0)
        camera_col.grid_columnconfigure(0, weight=1)

        # Add camera into camera column
        self.camera = tk.Label(camera_col)
        self.camera.grid(row=2,pady=(0,0), padx=(20,20))

        patient_data_container = tk.Frame(camera_col, borderwidth=1, relief="solid")
        patient_data_container.grid(row=3, )

        
        patient_id_label = ttk.Label(patient_data_container, text="รหัสผู้ป่วย", font=("Helvetica", 18))
        patient_id_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        self.patient_id_value = ttk.Label(patient_data_container, text=self.patient.patient_id,font=("Helvetica", 18) )
        self.patient_id_value.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

        firstname_label = ttk.Label(patient_data_container, text="ชื่อ", font=("Helvetica", 18))
        firstname_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        self.firstname_value = ttk.Label(patient_data_container,  text=self.patient.first_name, font=("Helvetica", 18))
        self.firstname_value.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        lastname_label = ttk.Label(patient_data_container, text="นามสกุล", font=("Helvetica", 18))
        lastname_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        self.lastname_value = ttk.Label(patient_data_container,  text=self.patient.first_name,font=("Helvetica", 18))
        self.lastname_value.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)
        
        ########## These're component for graph and button section ####################
        # Define second column for display graph and button
        col2 = tk.Frame(self,width=630,height=720)
        col2.pack(anchor=tk.CENTER)
        col2.grid_propagate(0)
        
        col2.grid_rowconfigure(0, weight=0)
        col2.grid_columnconfigure(0, weight=1)
        
        # Define a text to show that x axis is Time(in second)
        graph_label = tk.Label(col2, text="Graph", font=("Helvetica", 26))
        graph_label.grid(row=1)

        # Define figure for graph with size of (5.5,4)
        self.fig = Figure(figsize=(5.5, 4), dpi=100, facecolor="#FFFFFF")
        self.ax = self.fig.add_subplot(1, 1, 1)

        # Define graph section
        graph_row = tk.Frame(col2)
        graph_row.grid(row=2)
        
        # Define a text to show that x axis is Time(in second)
        x_label = tk.Label(col2, text="Time(s)", font=("Helvetica", 18))
        x_label.grid(row=3)

        # create a canvas to display the plot
        canvas = FigureCanvasTkAgg(self.fig, master=graph_row)
        canvas.draw()
        canvas.get_tk_widget().pack(anchor=tk.CENTER, fill=tk.BOTH)
        
        self.anim = animation.FuncAnimation(self.fig, self.animate, interval=500)

        # Add row section for start button & create patient data button
        button_row = tk.Frame(col2)
        button_row.grid(row=4, pady=(30,0))

        start_button = ttk.Button(button_row, 
                                       bootstyle="outline",
                                       text="Start",
                                       command=self.start_record,
                                       width=12)
    

        start_button.pack(padx=10, pady=0, side=tk.LEFT, anchor=tk.CENTER, ipadx=15, ipady=15)
        add_patient_btn = ttk.Button(button_row,
                                          bootstyle="success",
                                          text="เพิ่มข้อมูลผู้ป่วย", 
                                          command=self.navigate_to_create_patient,
                                          width=12)
    

        add_patient_btn.pack(padx=10, pady=0, side=tk.RIGHT, anchor=tk.CENTER, ipadx=15, ipady=15)
        
        self.show_camera()
    
    def patient_data_on_change(self):
        self.patient_id_value.configure(text=self.patient.patient_id)
        self.firstname_value.configure(text=self.patient.first_name)
        self.lastname_value.configure(text=self.patient.last_name)

    def navigate_to_create_patient(self):
        create_patient_page = self.controller.get_page("CreatePatient")
        create_patient_page.use_effect()
        self.controller.show_frame(create_patient_page.__class__)
        
    def animate(self, i):
        # update the data for the plot
        self.lock.acquire()
        
        xs = self.x[-40:]
        ys = self.y[-40:]
        self.ax.clear()
        self.ax.plot(xs,ys)
        self.lock.release()
        # self.ax.set_ylim(0, 2)

    def show_camera(self):
        ret, self.frame = self.cap.read()
        if(ret):
            cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

            gray_frame = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)
            contrast_frame = cv2.convertScaleAbs(gray_frame, alpha=3.0, beta=-300)      
            cv2image = contrast_frame
            in_roi_frame = contrast_frame[300:351, 250:281]
            
            if self.record_status:
                cv2.putText(cv2image, "Running",(30,30), cv2.FONT_HERSHEY_DUPLEX, 1.0, [255, 0, 0],2)
            else:
                cv2.putText(cv2image, "Idle",(30,30), cv2.FONT_HERSHEY_DUPLEX, 1.0, [0, 255, 0],2)
   
            # Draw bounding box on frame.
            cv2.polylines(cv2image,self.bounding_box,True,(0,255,255))
            
            # Calculate average intensity of interesting nail area
            avg_intensity = np.mean(in_roi_frame)
            
            # avg_intensity = (avg_intensity)/(255)
            
            # avg_intensity = avg_intensity-0.15
            # avg_intensity = avg_intensity/0.1
            
            self.lock.acquire()

            self.x.append(self.x[-1]+1)
            self.y.append(avg_intensity)
            self.lock.release()

            convImg = Image.fromarray(cv2image)
            convImg = convImg.resize((500, 500))
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

    async def connect(self):
        self.websocket = await websockets.connect("ws://0.0.0.0:8080")
        
    def start_record(self):
        self.record_status = not self.record_status
        asyncio.run(self.press_servo())

    async def press_servo(self):
        await self.connect()
        if self.record_status == True:
            await self.websocket.send("1000")
        else :
            await self.websocket.send("1900")
        await self.websocket.close()
           
    
        
##############################################################################################	

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

if __name__ == "__main__":
    app = CameraAndGraph()

