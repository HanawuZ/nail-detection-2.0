from tkinter import *
import cv2
from PIL import Image, ImageTk
import pathlib
import os

# multiprocessing
import multiprocessing as mp

# videocap = None

class View(Tk):
    def __init__(self):
        
        # globel
        # global videocap
        self.VIDEO_TEST_PATH = os.path.join(
            pathlib.Path(__file__).parent, "outpy.avi")
        self.record_status = False


        Tk.__init__(self)
        self.geometry("1900x600")
        # self.attributes("-fullscreen", True)
        self.bind('<Escape>', lambda e: self.quit())
        self["background"] = "#161616"

        # self.cap = cv2.VideoCapture(self.VIDEO_TEST_PATH)  # Demo Video
        self.cap = cv2.VideoCapture(0) # Webcam
        # videocap = self.cap
        # self.mainWindows = Tk(screenName="New Windows")
        # self.mainWindows.geometry("800x600")

        self.camera = Label(self, borderwidth=0)
        self.camera.pack(padx=20, side=LEFT, anchor=CENTER)
        self.button = Button(self, text="Record", command=self.startRecord, height=5, width=20)
        self.button.pack(padx=20, side=RIGHT, anchor=CENTER)

        self.show_camera()
        # Show UI
        self.mainloop()

    # Change state of variable to start functions
    def startRecord(self):
        self.record_status = not self.record_status
        
        # Create record process with attribute VideoCapture object
        if self.record_status == True:
            self.record = Record(cap=self.cap)
        
            # Start record process
            self.record.start()
        
        # Destroy record process object when stop recording
        else :
            self.record.terminate()
            del self.record


    def show_camera(self):
        ret, self.frame = self.cap.read()
        if(ret):
            cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            if self.record_status == True:
                cv2.putText(cv2image,"Running",(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
            else :
                cv2.putText(cv2image,"Not running",(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)

            convImg = Image.fromarray(cv2image)
            # convImg = convImg.resize(
            #     (
            #         int(
            #             self.winfo_screenheight(
            #             )*(4/3) - 100),
            #         int(
            #             self.winfo_screenheight() - 100
            #         )
            #     )
            # )  # Resize image from camera
            imgTk = ImageTk.PhotoImage(convImg)
            self.camera.imgtk = imgTk
            self.camera.configure(image=imgTk)
            # will call function record when show_camera run after 5 ms
            # self.camera.after(5, self.record)
            # will call recursive function whne pass to 5 ms
            self.camera.after(5, self.show_camera)
        else:
            self.cap.release()
            self.camera.destroy()


# ***************** path to Multiprocessing (Recording) **********************
class Record(mp.Process):
    def __init__(self, cap):
        mp.Process.__init__(self)
        self.cap = cap
        vid_output_path = os.path.join(pathlib.Path(__file__).parent,"output_sample.avi")
        self.video_recorder = cv2.VideoWriter(vid_output_path,cv2.VideoWriter_fourcc("M","J","P","G"), 30, (640,480))
    
    # Process start running this method when process is started
    def run(self):
        print("Run Record")
        self.record()

    # Record video, destroy this object when press recording
    
    def record(self):
        # print("Test")
        print(type(self.cap))
        # while(self.cap.isOpened()):
        #     check,frame = self.cap.read()
        #     if check == False:
        #         break
        #     else:
        #         # cv2.putText(frame,"Recording",(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
        #         self.video_recorder.write(frame)
                
        #         if cv2.waitKey(1) & 0xFF == ord('q'):
        #             print("Stop recording")
        #             break
                
# ***************** reading code satrt from this *****************
def main():
    # test = None
    test = View()
    # test.show_camera()s
    # test.mainloop()


if __name__ == "__main__":
    main()
    # print()

