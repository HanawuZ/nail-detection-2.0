from tkinter import *
import cv2
from PIL import Image, ImageTk

class View(Tk):
    def __init__(self):
        Tk.__init__(self, screenName="Testing")
        # self.geometry("800x600")
        self.attributes("-fullscreen", True)
        self.bind('<Escape>', lambda e: self.quit())
        self["background"] = "#161616"

        self.cap = cv2.VideoCapture("D:/Nail-Research/nail-detection-2.0/UI-tinker/src/outpy.avi")
        # self.mainWindows = T"k(screenName="New Windows")
        # self.mainWindows.geometry("800x600")

        self.camera = Label(self, borderwidth=0)
        self.camera.pack(padx=20, side=LEFT, anchor=CENTER)

    
    def show_camera(self):
        _, frame = self.cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        convImg = Image.fromarray(cv2image)
        convImg = convImg.resize((int(self.winfo_screenheight(
        )*(4/3) - 100), int(self.winfo_screenheight() - 100)))  # Resize image from camera
        imgTk = ImageTk.PhotoImage(convImg)
        self.camera.imgtk = imgTk
        self.camera.configure(image=imgTk)
        self.camera.after(5, self.show_camera)



def main():
    test = View()
    test.show_camera()
    test.mainloop()

if __name__ == "__main__":
    main()
