import tkinter as tk
from pages.camera_and_graph import CameraAndGraph
from pages.save_patient_data import ViewAndSavePatient
from models.Patient import Patient

class App(tk.Tk):
	
	# __init__ function for class tkinterApp
	def __init__(self, *args, **kwargs):
		
		self.patient = Patient()

		# __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)
		self.geometry("1280x720")
		#self.attributes('-fullscreen', True)
        
		# creating a container
		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		# initializing frames to an empty array
		self.frames = {}
		
		camera_and_graph = CameraAndGraph(container, self)
		self.frames[CameraAndGraph] = camera_and_graph
		camera_and_graph.grid(row = 0, column = 0, sticky ="nsew")
		
		view_and_save_patient = ViewAndSavePatient(container, self)
		self.frames[ViewAndSavePatient] = view_and_save_patient
		view_and_save_patient.grid(row = 0, column = 0, sticky ="nsew")

        # Open CameraAndGraph first if app is execute
		self.show_frame(CameraAndGraph)

		# pprint(self.frames)

	# to display the current frame passed as
	# parameter
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.on_enter()

		frame.tkraise()

		# Call on_leave method for other frames to stop their animations
		for f in self.frames.values():
			if f != frame:
				f.on_leave()

	def get_page(self, classname):
		'''Returns an instance of a page given it's class name as a string'''
		for page in self.frames.values():
			if str(page.__class__.__name__) == classname:
				return page
		return None

# first window frame startpage

if __name__ == "__main__":
	# Driver Code
    app = App()
    app.mainloop()
