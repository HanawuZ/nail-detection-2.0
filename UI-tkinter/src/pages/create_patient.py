import tkinter as tk
import ttkbootstrap as ttk
# from pages.camera_and_graph import CameraAndGraph
class CreatePatient(tk.Frame):
    def __init__(self, parent, controller, camera_and_graph, patient):
        tk.Frame.__init__(self, parent)
        self.bind("<Escape>", lambda e: self.quit())

        self.patient = patient
        self.camera_and_graph = camera_and_graph
        container = tk.Frame(self, borderwidth=1, relief="solid")
        container.pack(side = "top", fill = "y", expand = True, padx=30, pady=30)

        # container.grid_rowconfigure(0, weight = 0)
        # container.grid_columnconfigure(0, weight = 1)
        
        style = ttk.Style()
        style.configure(".", font=("Helvetica", 16))

        # Create a frame with a solid border
        header_frame = tk.Frame(container,)
        header_frame.pack(fill="x")


        # Place your content in the left column
        left_content = tk.Label(header_frame, text="เพิ่มข้อมูลผู้ป่วย", font=("Helvetica", 26))
        left_content.grid(row=0, column=0, sticky="w")

        # Add label and textfield for Patient_ID
        patient_id_frame = tk.Frame(container, borderwidth=1, relief="solid",)
        # patient_id_frame.pack(fill="x")
        patient_id_frame.pack(anchor="w",fill="x", padx=(0,0))

        patient_id_label = tk.Label(patient_id_frame, text="รหัสผู้ป่วย *", font=("Helvetica", 18))
        patient_id_label.pack(anchor="w", padx=(0,0))
        

        self.patient_id_entry = ttk.Entry(patient_id_frame, bootstyle="primary", font=("Helvetica", 16), width=55)
        self.patient_id_entry.pack(anchor="w", padx=(20,0), ipady=5)



        firstname_frame = tk.Frame(container,borderwidth=1, relief="solid")
        firstname_frame.pack(anchor="w", padx=(0,0), fill="x")


        firstname_label = tk.Label(firstname_frame, text="ชื่อ", font=("Helvetica", 18))
        firstname_label.pack(anchor="w", padx=(15,0))

        self.firstname_entry = ttk.Entry(firstname_frame, bootstyle="primary", width=55, font=("Helvetica", 16))
        self.firstname_entry.pack(anchor="w", padx=(20,0), ipady=5)

        lastname_frame = tk.Frame(container,borderwidth=1, relief="solid")
        lastname_frame.pack(anchor="w", padx=(15,0), fill="x")

        lastname_label = tk.Label(firstname_frame, text="นามสกุล", font=("Helvetica", 18))
        lastname_label.pack(anchor="w", padx=(15,0))

        self.lastname_entry = ttk.Entry(firstname_frame, bootstyle="primary", width=55, font=("Helvetica", 16))
        self.lastname_entry.pack(anchor="w", padx=(20,0), ipady=5)

        # Add label and textfield for Patient_ID
        datetime_frame = tk.Frame(container,borderwidth=1, relief="solid")
        datetime_frame.pack(fill="x")


        datetime_label = tk.Label(datetime_frame, text="วัน/เดือน/ปี เวลา", font=("Helvetica", 18))
        datetime_label.pack(anchor="w", padx=(15,0))

        datetime_entry = ttk.Entry(datetime_frame, bootstyle="primary", width=55, font=("Helvetica", 16))
        datetime_entry.pack(anchor="w", padx=(20,0), ipady=5)


        buttons_row = tk.Frame(container,borderwidth=1, relief="solid")
        buttons_row.pack()
        

        back_btn_frame = tk.Frame(buttons_row, borderwidth=1, relief="solid", 
                                  width=200, height=100)
        back_btn_frame.grid(row=1, column=1,)
        back_btn_frame.pack_propagate(0)

        back_button = ttk.Button(back_btn_frame, 
                                 bootstyle="danger-outline",
                                 text="ย้อนกลับ", 
                                 command = lambda : controller.show_frame(camera_and_graph),
                                 )
    
        back_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relheight=0.75, relwidth=0.75)
        back_btn_frame = tk.Frame(buttons_row, borderwidth=1, relief="solid",width=200, height=100)
        back_btn_frame.grid(row=1, column=2)
        back_btn_frame.pack_propagate(0)

        back_button = ttk.Button(back_btn_frame, 
                                 bootstyle="success",
                                 text="บันทึก", )
    
        back_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relheight=0.75,  relwidth=0.75)
    
    def add_patient_data(self):
        patient_id = self.patient_id_entry.get()
        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()


if __name__ == "__main__":
    create_patient = CreatePatient()