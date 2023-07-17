import tkinter as tk
import ttkbootstrap as ttk
import subprocess


class AddPatient(tk.Frame):
    # def show_virtual_keyboard(self):
    #     subprocess.call(["onboard"])


    # def patient_data_on_change(self):

    #     patient_id = self.patient_id_entry.get()
    #     first_name = self.firstname_entry.get()
    #     last_name = self.lastname_entry.get()

    #     self.controller.patient.set_patient_data(patient_id,first_name,last_name)

    #     self.controller.patient.set_patient_data(patient_id, first_name, last_name)
    #     camera_and_graph = self.controller.get_page("CameraAndGraph")
    #     camera_and_graph.patient_data_on_change()

    # def navigate_to_camera_and_graph(self):
    #     camera_and_graph = self.controller.get_page("CameraAndGraph").__class__
    #     self.controller.show_frame(camera_and_graph)

    # def use_effect(self):
    #     self.patient_id_entry.delete(0,tk.END)
    #     self.firstname_entry.delete(0,tk.END)
    #     self.lastname_entry.delete(0,tk.END)

    def update_data(self):
        firstname_value = self.firstname_entry.get()  # Get the text from the entry widget
        lastname_value = self.lastname_entry.get()  # Get the text from the entry widget
        patient_id_value = self.patient_id_entry.get()  # Get the text from the entry widget
        camera_and_graph = self.controller.get_page("CameraAndGraph")
        data = {
            "patient_id" : patient_id_value,
            "firstname" : firstname_value,
            "lastname" : lastname_value,
        }
        camera_and_graph.update_data(data)  # Call the update_data method in CameraAndGraph

    def clear_data(self):
        self.patient_id_entry.delete(0, tk.END)
        self.firstname_entry.delete(0, tk.END)
        self.lastname_entry.delete(0, tk.END)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.bind("<Escape>", lambda e: self.quit())

        self.parent = parent
        self.controller = controller

        container = tk.Frame(self,)
        container.pack(side = "top", fill = "y", expand = True, padx=30, pady=30)

        # container.grid_rowconfigure(0, weight = 0)
        # container.grid_columnconfigure(0, weight = 1)
        
        style = ttk.Style()
        style.configure(".", font=("Helvetica", 16))

        # Create a frame with a solid border
        header_frame = tk.Frame(container,)
        header_frame.pack(fill="x")


        # Place your content in the left column
        left_content = tk.Label(header_frame, text="ข้อมูลผู้ป่วย", font=("Helvetica", 26))
        left_content.grid(row=0, column=0, sticky="w")

        # Add label and textfield for Patient_ID
        patient_id_frame = tk.Frame(container)
        # patient_id_frame.pack(fill="x")
        patient_id_frame.pack(anchor="w",fill="x", padx=(0,0))

        patient_id_label = tk.Label(patient_id_frame, text="รหัสผู้ป่วย *", font=("Helvetica", 18))
        patient_id_label.pack(anchor="w", padx=(0,0))
        

        self.patient_id_entry = ttk.Entry(patient_id_frame, bootstyle="primary", font=("Helvetica", 16), width=55)
        self.patient_id_entry.pack(anchor="w", padx=(20,0), ipady=5)
        # self.patient_id_entry.bind("<Button-1>", lambda event: self.show_virtual_keyboard())


        firstname_frame = tk.Frame(container)
        firstname_frame.pack(anchor="w", padx=(0,0), fill="x")


        firstname_label = tk.Label(firstname_frame, text="ชื่อ", font=("Helvetica", 18))
        firstname_label.pack(anchor="w", padx=(15,0))

        self.firstname_entry = ttk.Entry(firstname_frame, bootstyle="primary", width=55, font=("Helvetica", 16))
        self.firstname_entry.pack(anchor="w", padx=(20,0), ipady=5)
        # self.firstname_entry.bind("<Button-1>", lambda event: self.show_virtual_keyboard())


        lastname_frame = tk.Frame(container)
        lastname_frame.pack(anchor="w", padx=(15,0), fill="x")

        lastname_label = tk.Label(firstname_frame, text="นามสกุล", font=("Helvetica", 18))
        lastname_label.pack(anchor="w", padx=(15,0))

        self.lastname_entry = ttk.Entry(firstname_frame, bootstyle="primary", width=55, font=("Helvetica", 16))
        self.lastname_entry.pack(anchor="w", padx=(20,0), ipady=5)

        buttons_row = tk.Frame(container)
        buttons_row.pack()
        

        clear_btn_frame = tk.Frame(buttons_row, width=200, height=100)
        clear_btn_frame.grid(row=1, column=1,)
        clear_btn_frame.pack_propagate(0)

        clear_button = ttk.Button(clear_btn_frame, 
                                 bootstyle="outline",
                                 text="Clear", 
                                 command=self.clear_data
                                 )
    
        clear_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relheight=0.75, relwidth=0.75)
        
        update_btn_frame = tk.Frame(buttons_row,width=200, height=100)
        update_btn_frame.grid(row=1, column=2)
        update_btn_frame.pack_propagate(0)

        update_button = ttk.Button(update_btn_frame, 
                                 bootstyle="success",
                                 text="Update", 
                                 command=self.update_data
                                 )
    
        update_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relheight=0.75,  relwidth=0.75)

