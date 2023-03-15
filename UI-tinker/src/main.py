from tkinter import *
import cv2
from PIL import Image, ImageTk
import pathlib
import os


class View(Tk):
    def __init__(self):
        self.VIDEO_TEST_PATH = os.path.join(
            pathlib.Path(__file__).parent, "outpy.avi")
        # globel
        self.recorder = False

        Tk.__init__(self)
        self.geometry("800x600")
        # self.attributes("-fullscreen", True)
        self.bind('<Escape>', lambda e: self.quit())
        self["background"] = "#161616"

        self.cap = cv2.VideoCapture(self.VIDEO_TEST_PATH)  # Demo Video
        # self.cap = cv2.VideoCapture(0) # Webcam

        # self.mainWindows = T"k(screenName="New Windows")
        # self.mainWindows.geometry("800x600")

        self.camera = Label(self, borderwidth=0)
        self.camera.pack(padx=20, side=LEFT, anchor=CENTER)
        self.button = Button(
            self, text="exit", command=self.startRecord, height=5, width=20)
        self.button.pack(padx=20, side=RIGHT, anchor=CENTER)

    # Change state of variable to start functions
    def startRecord(self):
        self.recorder = not self.recorder

    # Function to records or start save data (example start servo and record camera)

    def record(self):
        if(self.recorder):
            print("record")

    def show_camera(self):
        ret, self.frame = self.cap.read()
        if(ret):
            cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            convImg = Image.fromarray(cv2image)
            convImg = convImg.resize(
                (
                    int(
                        self.winfo_screenheight(
                        )*(4/3) - 100),
                    int(
                        self.winfo_screenheight() - 100
                    )
                )
            )  # Resize image from camera
            imgTk = ImageTk.PhotoImage(convImg)
            self.camera.imgtk = imgTk
            self.camera.configure(image=imgTk)
            # will call function record when show_camera run after 5 ms
            self.camera.after(5, self.record)
            # will call recursive function whne pass to 5 ms
            self.camera.after(5, self.show_camera)
        else:
            self.cap.release()
            self.camera.destroy()

# *****************reading code satrt from this*****************


def main():
    test = View()
    test.show_camera()
    test.mainloop()


if __name__ == "__main__":
    main()
    # print()
