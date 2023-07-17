import tkinter as tk

class SuccessPopup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("300x200")

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