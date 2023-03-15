import tkinter as tk
import os
import cv2
import sys
from PIL import Image, ImageTk
from pathlib import Path
from gpiozero import Servo, Button
from time import sleep, time
import multiprocessing as mp

fileName = os.path.join(Path(__file__).parent, "\WebcamCap.txt")
# fileName = os.environ['ALLUSERSPROFILE'] + "\WebcamCap.txt"
press_start_time = 0
cancel = False
e = mp.Event()
start_delay = 0
record_process = None
record_status = False
cap = None

servo = Servo(17)
 
def changeCam(event=0, nextCam=-1):
    global camIndex, cap, fileName
 
    if nextCam == -1:
        camIndex += 1
    else:
        camIndex = nextCam
    del(cap)
    cap = cv2.VideoCapture(camIndex)
 
    #try to get a frame, if it returns nothing
    success, frame = cap.read()
    if not success:
        camIndex = 0
        del(cap)
        cap = cv2.VideoCapture(camIndex)
 
    f = open(fileName, 'w')
    f.write(str(camIndex))
    f.close()

def startRecording(e):
    VID_OUTPUT_PATH = os.path.join(Path(__file__).parent,"output_sample.avi")
    out = cv2.VideoWriter(VID_OUTPUT_PATH,cv2.VideoWriter_fourcc("M","J","P","G"), 20, (640,480))
    while(cap.isOpened()):
        if e.is_set():
            out.release()
            # cv2.destroyAllWindows()
            e.clear()
        ret, frame = cap.read()
        if ret==True:
            out.write(frame)
        else:
            break
    

def pressServo(event = 0):
    global press_start_time, record_process, record_status
    
    # REF : https://stackoverflow.com/questions/25149543/record-opencv-video-during-tkinter-mainloop
    record_process = mp.Process(target=startRecording, args=(e,))
    record_process.start()
    def Normalize(deg):
        return ((deg ) / (90)) * (1 - (-1)) + (-1)
    servo.value = Normalize(75)
    sleep(0.5)
    servo.detach()
    press_start_time = time()
    record_status = True


def show_frame():
    global cancel, prevImg, button, press_start_time, start_delay, record_process, record_status
        
    # Read video frame
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    
    # Show recording status label
    # If video is recording, show "Recording" on current frame.
    if record_status :
        cv2.putText(cv2image,"Recording",(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
    
    # Else then show "Not Recording" on current frame.
    else :
        cv2.putText(cv2image,"Not Recording",(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)

    prevImg = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
                
    # If frame is not capture, then play frame
    if not cancel:
        press_end_time = time()
        lmain.after(10, show_frame)
        
        # If servo press for 5 seconds, that release servo
        if int(press_end_time - press_start_time) == 5:
            
            # Get time for delay before stop record
            start_delay = time()
            servo.min()
            sleep(0.5)
            servo.detach()
            press_start_time = 0
        
        # If time has delay for 4 seconds, It will stop recording and terminate record process
        if int(press_end_time - start_delay) == 4:
            record_process.terminate()
            record_process.join()
            start_delay = 0
            record_status = False

            
if __name__ == "__main__":
    try:
        f = open(fileName, 'r')
        camIndex = int(f.readline())
    except:
        camIndex = 0
     
    cap = cv2.VideoCapture(camIndex)
     
    success, frame = cap.read()
    if not success:
        if camIndex == 0:
            print("Error, No webcam found!")
            sys.exit(1)
        else:
            changeCam(nextCam=0)
            success, frame = cap.read()
            if not success:
                print("Error, No webcam found!")
                sys.exit(1)
   
    servo.min()
    sleep(0.1)
    servo.detach()
     
    mainWindow = tk.Tk()
    mainWindow.resizable(width=False, height=False)
    mainWindow.bind('<Escape>', lambda e: mainWindow.quit())
    lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
    button = tk.Button(mainWindow, text="Press", command=pressServo)
    button_changeCam = tk.Button(mainWindow, text="Switch Camera", command=changeCam)
     
    lmain.pack()
    button.place(bordermode=tk.INSIDE, relx=0.5, rely=0.9, anchor=tk.CENTER, width=300, height=50)
    button.focus()
    button_changeCam.place(bordermode=tk.INSIDE, relx=0.85, rely=0.1, anchor=tk.CENTER, width=150, height=50)
        
    show_frame()
    mainWindow.mainloop()

