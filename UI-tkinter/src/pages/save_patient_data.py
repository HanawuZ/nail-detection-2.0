import tkinter as tk
import ttkbootstrap as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.animation as animation
import random
import json
style.use("ggplot")
import requests
from .components import *

class ViewAndSavePatient(tk.Frame):

    def animate(self, i):
        if i >= len(self.sample_data):
            return
        # self.y.append(self.data[i])
        self.y.append(self.sample_data[i])
        self.ax.clear()
        self.ax.plot(self.y)
        self.ax.set_ylim([0,200])

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.sample_data = [random.randint(50, 100) for _ in range(100)]
        self.data = []
        self.controller = controller
        self.y =[]
        self.canvas = None
        
        style = ttk.Style()
        style.configure(".", font=("Helvetica", 16))

        col1 = tk.Frame(self,width=650,height=720,borderwidth=1, relief="solid")
        col1.pack(side=tk.LEFT)
        col1.grid_propagate(0)
        col1.grid_rowconfigure(0, weight=0)
        col1.grid_columnconfigure(0, weight=1)
        
        patient_data_container = tk.Frame(col1, borderwidth=1, relief="solid")
        patient_data_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
       
        patient_data_container_header = tk.Label(patient_data_container, text="ข้อมูลผู้ป่วย", font=("Helvetica", 26))
        patient_data_container_header.grid(row=1)

        patient_data_container_body =  tk.Frame(patient_data_container, borderwidth=1, relief="solid")
        patient_data_container_body.grid(row=2)


        patient_id_label = ttk.Label(patient_data_container_body, text="รหัสผู้ป่วย", font=("Helvetica", 18))
        patient_id_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        self.patient_id_value = ttk.Label(patient_data_container_body, text=self.controller.patient.patient_id,font=("Helvetica", 18) )
        self.patient_id_value.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

        firstname_label = ttk.Label(patient_data_container_body, text="ชื่อ", font=("Helvetica", 18))
        firstname_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        self.firstname_value = ttk.Label(patient_data_container_body,  text=self.controller.patient.first_name, font=("Helvetica", 18))
        self.firstname_value.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        lastname_label = ttk.Label(patient_data_container_body, text="นามสกุล", font=("Helvetica", 18))
        lastname_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        self.lastname_value = ttk.Label(patient_data_container_body,  text=self.controller.patient.first_name,font=("Helvetica", 18))
        self.lastname_value.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)


        # # Add camera into camera column
        # self.camera = tk.Label(col1)
        # self.camera.grid(row=2,pady=(0,0), padx=(20,20))

        # Add row section for start button & create patient data button
        button_row = tk.Frame(patient_data_container)
        button_row.grid(row=4, pady=(30,0))

        start_button = ttk.Button(button_row, 
                                       bootstyle="outline",
                                       text="Start",
                                       width=12)

        start_button.pack(padx=10, pady=0, side=tk.LEFT, anchor=tk.CENTER, ipadx=15, ipady=15)

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
        self.graph_row = tk.Frame(col2)
        self.graph_row.grid(row=2)
        
        # # Define a text to show that x axis is Time(in second)
        # x_label = tk.Label(col2, text="Time(s)", font=("Helvetica", 18))
        # x_label.grid(row=3)

        #         # Add row section for start button & create patient data button
        # button_row = tk.Frame(col2)
        # button_row.grid(row=4, pady=(30,0))

        # start_button.pack(padx=10, pady=0, side=tk.LEFT, anchor=tk.CENTER, ipadx=15, ipady=15)
        # save_patient_btn = ttk.Button(button_row,
        #                               bootstyle="primary",
        #                               text="บันทึกข้อมูลผู้ป่วย", 
        #                               width=12)
        # save_patient_btn.pack(padx=10, pady=0, side=tk.RIGHT, anchor=tk.CENTER, ipadx=15, ipady=15)
    
  

    def show_popup(self):
        # Create an instance of the CustomMessageBox class
        popup = SuccessPopup(self)
        popup.grab_set()

    def patient_data_on_change(self):
        self.patient_id_value.configure(text=self.controller.patient.patient_id)
        self.firstname_value.configure(text=self.controller.patient.first_name)
        self.lastname_value.configure(text=self.controller.patient.last_name)

    def navigate_to_camera_and_graph(self):
        camera_and_graph = self.controller.get_page("CameraAndGraph").__class__
        self.canvas.get_tk_widget().destroy()  # Destroy the canvas widget
        self.y.clear()
        self.controller.show_frame(camera_and_graph)

    def on_enter(self):
        self.data = self.controller.patient.data
        self.patient_data_on_change()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_row)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(anchor=tk.CENTER, fill=tk.BOTH)
        self.anim = animation.FuncAnimation(self.fig, self.animate, interval=100)
    
    def insert_patient_data(self):
        patient_data = {
            "pid" : self.controller.patient.patient_id,
            "pname" : self.controller.patient.first_name,
            "psurname" : self.controller.patient.last_name,
            "data": self.controller.patient.data,
        }
        if len(self.intensity_list) == 0 :
            print("Please collect data value")
        else :
            try :
                json_object = json.dumps(patient_data, indent = 4) 
                response = requests.post('http://localhost:8080/nail', data=json_object)
                print(response)
                self.intensity_list.clear()
            except:
                print("Error, please try again!!")



