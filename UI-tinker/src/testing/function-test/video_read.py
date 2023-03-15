import cv2
import pathlib
import os
from time import sleep
from gpiozero import Button


# Define videos directory path
# Path is something like .../Capillary-refill-detection/src/videos
VID_DIRECTORY_PATH = os.path.join(pathlib.Path(__file__).parent, "videos")

# Initialize gpio 21 for being record button.
record_button = Button(21)
record_status = False

"""
# Define video path.
vid1_path = os.path.join(VID_DIRECTORY_PATH,'output.mp4')
vid2_path = os.path.join(VID_DIRECTORY_PATH,'output2.mp4')
vid3_path = os.path.join(VID_DIRECTORY_PATH,'output3.mp4')
vid4_path = os.path.join(VID_DIRECTORY_PATH,'output4.mp4')
vid5_path = os.path.join(VID_DIRECTORY_PATH,'output5.mp4')
vid6_path = os.path.join(VID_DIRECTORY_PATH,'output6.mp4')
"""

# Initialize camera
video = cv2.VideoCapture(0)
frame_width = int(video.get(3))
frame_height = int(video.get(4))
output_path = os.path.join(VID_DIRECTORY_PATH,"output.mp4")
out = cv2.VideoWriter(output_path,cv2.VideoWriter_fourcc("M","J","P","G"), 20, (frame_width,frame_height))


while(video.isOpened()):
    
    # Read video frame and get status of frame.
    check,frame = video.read()

    # Close window if video end
    # If frame's status is false then break from loop.
    if check == False:
        break
    
    if record_button.is_pressed:
        record_status = not record_status
        sleep(0.1)
        if record_status:
            
            print("Start Recording")
        else :
            print("Stop Recording")
            
    if record_status:
        cv2.putText(frame,"Recording",(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
        out.write(frame)
    else :
        cv2.putText(frame,"Not Recording",(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
    cv2.imshow("Camera", frame)

    # Close window when press button 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()
    