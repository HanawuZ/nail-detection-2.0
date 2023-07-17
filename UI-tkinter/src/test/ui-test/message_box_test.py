import tkinter as tk
from tkinter import messagebox

def show_custom_message():
    # Create a new toplevel window
    popup = tk.Toplevel()
    popup.title("Custom Message")
    popup.geometry("300x200")

    # Create message content
    label = tk.Label(popup, text="This is a custom message!")
    label.pack(pady=20)

    # Add a button to close the popup
    button = tk.Button(popup, text="Close", command=popup.destroy)
    button.pack()

# Create the main Tkinter window
root = tk.Tk()

# Add a button to trigger the custom message box
button = tk.Button(root, text="Show Custom Message", command=show_custom_message)
button.pack(pady=50)

# Start the Tkinter event loop
root.mainloop()
