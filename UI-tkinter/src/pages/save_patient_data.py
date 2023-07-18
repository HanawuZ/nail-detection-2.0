from pprint import pprint
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
        try :
            if i >= len(self.data):
                return
            self.y.append(self.data[i])
            # self.y.append(self.sample_data[i])
            self.ax.clear()
            self.ax.plot(self.y)
            self.ax.set_ylim([0,200])
        except :
            return

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.sample_data = [random.randint(50, 100) for _ in range(100)]
        self.data = None
        self.controller = controller
        self.y =[]
        self.canvas = None
        
        style = ttk.Style()
        style.configure(".", font=("Helvetica", 16))

        self.col1 = tk.Frame(self,borderwidth=1, relief="solid")
        self.col1.pack(side=tk.LEFT, fill=tk.BOTH,expand=True,anchor=tk.CENTER,)
        self.col1.grid_propagate(0)
        self.col1.grid_rowconfigure(0, weight=0)
        self.col1.grid_columnconfigure(0, weight=1)
        
        # Place your content in the left column
        container = tk.Frame(self.col1, borderwidth=1, relief="solid")
        container.grid(row=0, column=0,pady=(100,30))

        tk.Label(container, text="ข้อมูลผู้ป่วย", font=("Helvetica", 26)).pack(anchor="w", padx=(0,0))

        # Add label and textfield for Patient_ID
        self.patient_id_frame = tk.Frame(container)
        # patient_id_frame.pack(fill="x")
        self.patient_id_frame.pack(anchor="w",fill="x", padx=(0,0))

        patient_id_label = tk.Label(self.patient_id_frame, text="รหัสผู้ป่วย *", font=("Helvetica", 18))
        patient_id_label.pack(anchor="w", padx=(0,0))
        
        self.patient_id_entry = ttk.Entry(self.patient_id_frame, bootstyle="primary", font=("Helvetica", 16), width=55)
        self.patient_id_entry.pack(anchor="w", padx=(20,0), ipady=5)
        # self.patient_id_entry.bind("<Button-1>", lambda event: self.show_virtual_keyboard())

        self.firstname_frame = tk.Frame(container)
        self.firstname_frame.pack(anchor="w", padx=(0,0), fill="x")


        firstname_label = tk.Label(self.firstname_frame, text="ชื่อ", font=("Helvetica", 18))
        firstname_label.pack(anchor="w", padx=(15,0))

        self.firstname_entry = ttk.Entry(self.firstname_frame, bootstyle="primary", width=55, font=("Helvetica", 16))
        self.firstname_entry.pack(anchor="w", padx=(20,0), ipady=5)
        # self.firstname_entry.bind("<Button-1>", lambda event: self.show_virtual_keyboard())


        self.lastname_frame = tk.Frame(container)
        self.lastname_frame.pack(anchor="w", padx=(0,0), fill="x")

        lastname_label = tk.Label(self.lastname_frame, text="นามสกุล", font=("Helvetica", 18))
        lastname_label.pack(anchor="w", padx=(15,0))

        self.lastname_entry = ttk.Entry(self.lastname_frame, bootstyle="primary", width=55, font=("Helvetica", 16))
        self.lastname_entry.pack(anchor="w", padx=(20,0), ipady=5)


        # tk.Label(patient_data_container,borderwidth=1, text="ข้อมูลผู้ป่วย",
        #          relief="solid", font=("Helvetica", 26)).grid(row=1,pady=(100,0), sticky="w")
       
        # patient_data_container_body =  tk.Frame(patient_data_container, borderwidth=1, relief="solid")
        # patient_data_container_body.grid(row=2,pady=(20,0), sticky="w")


        # patient_id_label = ttk.Label(patient_data_container_body, text="รหัสผู้ป่วย", font=("Helvetica", 18))
        # patient_id_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        # self.patient_id_value = ttk.Label(patient_data_container_body, text=self.controller.patient.patient_id,font=("Helvetica", 18) )
        # self.patient_id_value.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

        # firstname_label = ttk.Label(patient_data_container_body, text="ชื่อ", font=("Helvetica", 18))
        # firstname_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        # self.firstname_value = ttk.Label(patient_data_container_body,  text=self.controller.patient.first_name, font=("Helvetica", 18))
        # self.firstname_value.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        # lastname_label = ttk.Label(patient_data_container_body, text="นามสกุล", font=("Helvetica", 18))
        # lastname_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        # self.lastname_value = ttk.Label(patient_data_container_body,  text=self.controller.patient.first_name,font=("Helvetica", 18))
        # self.lastname_value.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)


        # # Add camera into camera column
        # self.camera = tk.Label(col1)
        # self.camera.grid(row=2,pady=(0,0), padx=(20,20))

        self.status_label = tk.Label(self.col1)
        self.status_label.grid(row=1,pady=10)
        self.status_label.config(text="",font=("Helvetica", 16))
        
        # Add row section for start button & create patient data button
        button_row = tk.Frame(self.col1)
        button_row.grid(row=2)

        back_button = ttk.Button(button_row, 
                                       bootstyle="outline",
                                       text="Back",
                                       command=self.navigate_to_camera_and_graph,
                                       width=12)

        back_button.pack(padx=10, pady=0, side=tk.LEFT, anchor=tk.CENTER, ipadx=15, ipady=15)
        create_data_button = ttk.Button(button_row, 
                                       bootstyle="success",
                                       text="Create",
                                       command=self.insert_patient_data,
                                       width=12)

        create_data_button.pack(padx=10, pady=0, side=tk.LEFT, anchor=tk.CENTER, ipadx=15, ipady=15)

        self.col2 = tk.Frame(self,width=630,height=720)
        self.col2.pack(anchor=tk.CENTER)
        self.col2.grid_propagate(0)
        
        self.col2.grid_rowconfigure(0, weight=0)
        self.col2.grid_columnconfigure(0, weight=1)
    

        # Define figure for graph with size of (5.5,4)
        self.fig = Figure(figsize=(5.5, 4), dpi=100, facecolor="#FFFFFF")
        self.ax = self.fig.add_subplot(1, 1, 1)


        # Define graph section
        graph_label_frame = tk.Frame(self.col2)
        graph_label_frame.grid(row=1)

        tk.Label(graph_label_frame, text="ผลลัพธ์การตรวจ", font=("Helvetica", 26)).pack(anchor="w", padx=(0,0))
        
        # Define graph section
        self.graph_row = tk.Frame(self.col2)
        self.graph_row.grid(row=2)

        
        self.graph_label = tk.Label(self.col2, font=("Helvetica", 26))
        self.graph_label.grid(row=2)
        
        # # Define a text to show that x axis is Time(in second)
        # x_label = tk.Label(col2, text="Time(s)", font=("Helvetica", 18))
        # x_label.grid(row=3)

        # Add row section for start button & create patient data button
        button_row = tk.Frame(self.col2)
        button_row.grid(row=4, pady=(30,0))

        self.replay_btn = ttk.Button(button_row,
                                bootstyle="outline",
                                text="Replay", 
                                command=self.replay_graph,
                                width=12)
        self.replay_btn.pack(padx=10, pady=0, side=tk.LEFT, anchor=tk.CENTER, ipadx=15, ipady=15)

        self.clear_btn = ttk.Button(button_row,
                                bootstyle="danger",
                                text="Clear Data", 
                                # command=self.replay_graph,
                                width=12)
        self.clear_btn.pack(padx=10, pady=0, anchor=tk.CENTER, ipadx=15, ipady=15)
        self.clear_btn.config(state=tk.DISABLED)

        if not self.data:
            self.replay_btn.config(state=tk.DISABLED)
  

    def show_popup(self):
        # Create an instance of the CustomMessageBox class
        popup = SuccessPopup(self)
        popup.grab_set()

    def navigate_to_camera_and_graph(self):
        self.status_label.config(text="")
        camera_and_graph = self.controller.get_page("CameraAndGraph").__class__
        self.canvas.get_tk_widget().destroy()  # Destroy the canvas widget
        self.y.clear()
        self.controller.show_frame(camera_and_graph)

    def on_enter(self):
        self.data = self.controller.patient.data      
        if not self.data:
            self.graph_label = tk.Label(self.col2, font=("Helvetica", 26))
            self.graph_label.grid(row=2)
            self.graph_label.config(text="ไม่มีข้อมูล")
        else :
            self.graph_label.config(text="")
            self.replay_btn.config(state=tk.NORMAL)


        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_row)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(anchor=tk.CENTER, fill=tk.BOTH)
        self.anim = animation.FuncAnimation(self.fig, self.animate, interval=100)
    
    def replay_graph(self):
        self.y.clear()
        self.canvas.get_tk_widget().destroy()  # Destroy the canvas widget
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_row)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(anchor=tk.CENTER, fill=tk.BOTH)
        self.anim = animation.FuncAnimation(self.fig, self.animate, interval=100)
        

    def insert_patient_data(self):

        patient_data = {
            "pid" : str(self.patient_id_entry.get()),
            "pname" : str(self.firstname_entry.get()),
            "psurname" : str(self.lastname_entry.get()),
            "data": self.controller.patient.data,
        }
        pprint(patient_data)

        if not patient_data["pid"] or not patient_data["pname"] or not patient_data["psurname"]:
            self.status_label.config(text="กรุณากรอกข้อมูลให้ครบถ้วน",font=("Helvetica", 16),fg= "red")
            
        elif not patient_data["data"] :
            self.status_label.config(text="กรุณาเก็บข้อมูลการตรวจจับก่อน",font=("Helvetica", 16),fg= "red")
        
        else :
            try :
                json_data = json.dumps(patient_data, indent = 4) 
                response = requests.post('http://localhost:8080/nail', data=json_data)
                print(response)
            except:
                print("Error, please try again!!")



