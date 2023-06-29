import subprocess
import tkinter as tk

def show_virtual_keyboard():
    subprocess.call(["onboard"])
    
master = tk.Tk()
#master.attributes('-fullscreen', True)
tk.Label(master, text="First Name").grid(row=0)
tk.Label(master, text="Last Name").grid(row=1)

e1 = tk.Entry(master)
e2 = tk.Entry(master)

e1.grid(row=0, column=1)
e1.bind("<Button-1>", lambda event: show_virtual_keyboard())
e2.grid(row=1, column=1)
e2.bind("<Button-1>", lambda event: show_virtual_keyboard())


master.mainloop()
