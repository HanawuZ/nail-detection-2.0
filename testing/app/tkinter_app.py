import tkinter as tk


root_window = tk.Tk()

root_window.title("Application title")
root_window.geometry("300x100")
root_window.configure(background = "#353535")

tk.Label(root_window, text='Hello World').pack()

root_window.mainloop()
