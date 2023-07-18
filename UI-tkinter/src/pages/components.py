import tkinter as tk

class SuccessPopup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("300x200")

        # Calculate the coordinates to center the window on the screen
        # Calculate the x and y coordinates for centering the window
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()
        position_right = int(self.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.winfo_screenheight() / 2 - window_height / 2)

        # Create message content
        label = tk.Label(self, text="Save Success")
        label.pack(pady=20)

        # Add a button to close the popup
        button = tk.Button(self, text="Close", command=self.destroy)
        button.pack()

class ErrorPopup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("300x200")

        # Create message content
        label = tk.Label(self, text="Error, please try again!!")
        label.pack(pady=20)

        # Add a button to close the popup
        button = tk.Button(self, text="Close", command=self.destroy)
        button.pack()