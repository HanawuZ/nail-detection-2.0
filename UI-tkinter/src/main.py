import tkinter as tk
from pages.camera_and_graph import CameraAndGraph
from pages.create_patient import CreatePatient
from models.Patient import Patient

class App(tk.Tk):
	
	# __init__ function for class tkinterApp
	def __init__(self, *args, **kwargs):
		
		self.patient = Patient("HN123456789", "John", "Doe")

		# __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)
		self.geometry("1280x720")
        
		# creating a container
		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		# initializing frames to an empty array
		self.frames = {}
		
		camera_and_graph = CameraAndGraph(container, self, CreatePatient,self.patient)
		self.frames[CameraAndGraph] = camera_and_graph
		camera_and_graph.grid(row = 0, column = 0, sticky ="nsew")
		
		create_patient = CreatePatient(container, self, CameraAndGraph,self.patient)
		self.frames[CreatePatient] = create_patient
		create_patient.grid(row = 0, column = 0, sticky ="nsew")

        # Open CameraAndGraph first if app is execute
		self.show_frame(CameraAndGraph)

	# to display the current frame passed as
	# parameter
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

# first window frame startpage

if __name__ == "__main__":
	# Driver Code
    app = App()
    app.mainloop()
