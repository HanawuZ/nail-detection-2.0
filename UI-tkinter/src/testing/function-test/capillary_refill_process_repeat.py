
"""
####### PSEUDO CODE ########

@ process
function read_nail_intensity() then
    ....
    ....
    while true then
        if video is end then
            set terminate status to true
            break
        end
        
        Lock aqquire
        Read nail intensity frame by frame
        Add frame value to list x
        Add Nail intensity value to list y
        Lock release
        Display video
    end
end

function real_time_plotting() then
    Initialize animated function
    Show plot
end

@ process
function camera_run() then
    ...
    ...
    while true then
        if button is pressed then
            Set Record status to true
        end
    
        if Record status is true then
            Start Record video
        end
    
        Display video
    end
    
    ...
    ...
end

@ process
function servo_run() then
    ....
    ....
    while true then
        if Record status is true then
            Servo is pressed for 5 second
            Set terminate status to true
            Set Record status to false
            Release Servo
            break loop
        end
    end
    ....
    ....
end

main function

    Declare terminate status. default is false
    Declare record status. default is false
   
    Initialize read nail intensity process

    while(true) then
        Initialize servo process
        Initialize camera process
        Detach servo
        Set servo in min angle
        Delay 0.1 s
        Detach servo
            
           
            servo_process.start()
            camera_process.start()
            
            # Join these 2 processes together for parallelly running.
            servo_process.join()
            camera_process.join()
            
            if bool(terminate_status.value)then
                set camera status to false
                set terminate status to false
                servo_process.terminate()
                camera_process.terminate()
            end
        end
        
        if read nail status is true then
            manager=mp.Manager()

            lock = mp.Lock()

            list_x = manager.list()
            list_y = manager.list()
            list_x.append(0)
            list_y.append(0)
                
            read_nail_intensity_process = mp.Process(target=read_nail_intensity, args=( list_x, list_y, lock))  
            read_nail_intensity_process.start()
              
            real_time_plotting(list_x, list_y, lock)
            read_nail_intensity_process.join()
            
            if terminate status is true then
                set read nail status to false
                set terminate status to false
                set camera status to true
                terminate real nail intensity process
            end
        end
    end loop

"""


"""
Implements program that execute multiprocesses consists of
- Video capture and recording from camera
- When press button. Servo will start presssing nail and video start recording
  If servo is release, then wait for a certain before stop recording.
- Plotting line graph of capillary after Servo was releases

"""
import numpy as np
import cv2
import pathlib
import os
from gpiozero import Servo, Button
from time import sleep
import multiprocessing as mp
import matplotlib.pyplot as plt
import matplotlib.animation as animation

servo, press_button = Servo(17), Button(21)

# Define videos directory path
# Path is something like .../Capillary-refill-detection/src/videos
VID_DIRECTORY_PATH = os.path.join(pathlib.Path(__file__).parent, "videos")

output_path = os.path.join(VID_DIRECTORY_PATH,"output_sample.avi")
out = cv2.VideoWriter(output_path,cv2.VideoWriter_fourcc("M","J","P","G"), 20, (640,480))

roi = np.array([[
    [210,125],
    [425,125],
    [425,330],
    [210,330]
]])

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

def read_nail_intensity(list_x, list_y, lock, terminate_status):
    valueOfXPlot = 0
    vid6_path =  os.path.join(VID_DIRECTORY_PATH,"output6.mp4")

    box_centroid = np.array([(180+450)//2 , (80+400)//2])
    bounding_box = np.array([[
        [box_centroid[0],box_centroid[1]],
        [450,box_centroid[1]],
        [450,400-50],
        [box_centroid[0],400-50]
    ]])

    # Read video from videos directory.
    video = cv2.VideoCapture(vid6_path) # for select video path

    while(video.isOpened()):
        # Read video frame and get status of frame.
        check,frame = video.read()

        if check == False:
            terminate_status.value = 1
            break

        # Convert BGR frame to Grayscale frame.
        frame = cv2.resize(src=frame, dsize=(640,480))
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        contrast_frame = cv2.convertScaleAbs(gray_frame, alpha=3.0, beta=-200)      # Contrast values 3

        in_roi_frame = contrast_frame[box_centroid[0]:401, box_centroid[1]:401]

        # Draw bounding box on frame.
        cv2.polylines(contrast_frame,bounding_box,True,(0,255,255))
        cv2.circle(contrast_frame, (box_centroid[0], box_centroid[1]), radius=3, color=(255, 255, 255), thickness=-1)
        cv2.imshow("Result", contrast_frame)
        
        # Store frame intensity value.
        avg_intensity = np.mean(in_roi_frame)
        valueOfXPlot += 1
        lock.acquire()
        list_x.append(valueOfXPlot/30)
        list_y.append(avg_intensity)
        lock.release()

         # Close window when press button 'q'
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()

def animate(i, list_x, list_y, lock):
    lock.acquire()
    ax.clear()
    ax.plot(list_x, list_y)
    lock.release()
    
def real_time_plotting(list_x, list_y, lock):
    # This function is called periodically from FuncAnimation
    # Set up plot to call animate() function periodically
    _ = animation.FuncAnimation(fig, animate, fargs=(list_x, list_y, lock), interval=25)
    plt.show()

def camera_run(record_status, terminate_status):
    
    # Initialize camera
    video = cv2.VideoCapture(-1)
    frame_width = int(video.get(3))
    frame_height = int(video.get(4))

    while(video.isOpened()):
    
        # Read video frame and get status of frame.
        check,frame = video.read()

        # Close window if video end
        # If frame's status is false then break from loop.
        if check == False:
            break
        
        cv2.polylines(frame,roi,True,(0,255,255))
 
        if press_button.is_pressed:
            record_status.value = 1
            sleep(0.1)        
        
        if bool(record_status.value):
            cv2.putText(frame,"Recording",(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
            out.write(frame)
        else :
            cv2.putText(frame,"Not Recording",(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
        cv2.imshow("Camera", frame)
        
        # Close window when press button 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if bool(terminate_status.value):
            break
    video.release()
    cv2.destroyAllWindows()

    

def servo_run(record_status, terminate_status):
    
    def Normalize(deg):
        return ((deg ) / (90)) * (1 - (-1)) + (-1)
    servo.detach()
    sleep(0.1)
    servo.min()
    sleep(0.1)
    servo.detach()
    while True:
        if(bool(record_status.value)):
            sleep(0.1)
            servo.value = Normalize(75)
            sleep(0.5)
            servo.detach()
            sleep(5)
            servo.min()
            sleep(0.5)
            servo.detach()
            sleep(3)
            terminate_status.value= 1
            record_status.value = 0
            break
            
       
if __name__ == "__main__":
    
    # Declare shared memory integer var `record_status` for checking recording state
    record_status = mp.Value("i",0)
    
    # Declare shared memory integer var `terminated_status` for check if ternimated status is true
    terminate_status = mp.Value("i",0)
            
    manager=mp.Manager()

    # creating a lock object
    lock = mp.Lock()


    try:
        while True:
            # Detach servo
            servo.min()
            sleep(0.05)
            servo.detach()
        
            # Initialize servo process    
            servo_process = mp.Process(target=servo_run, args=(record_status, terminate_status,))
            
            # Initialize camera process
            camera_process = mp.Process(target=camera_run, args=(record_status, terminate_status,))
            
            # Start servo process and camera process
            servo_process.start()
            camera_process.start()
        
            # Join these 2 processes together for parallelly running.
            servo_process.join()
            camera_process.join()
            
            # If terminate status is true, then terminate servo process and camera process
            # and start read nail intensity process
            if bool(terminate_status.value):
                terminate_status.value = 0
                
                # Terminate servo process and camera process.
                servo_process.terminate()
                camera_process.terminate()
                
                # Join terminated processes to finish jobs.
                servo_process.join()
                camera_process.join()
                
                # Declare list_x and list_y
                list_x = manager.list()
                list_y = manager.list()
                
                # Append 0 to list_x and list_y 
                list_x.append(0)
                list_y.append(0)
                
                # Initialize read nail intensity process
                read_nail_intensity_process = mp.Process(target=read_nail_intensity, args=(list_x,list_y,lock,terminate_status))
                
                # Start process
                read_nail_intensity_process.start()
                
                real_time_plotting(list_x, list_y, lock)
                
                # Join read nail process to main process
                read_nail_intensity_process.join()
                
                if bool(terminate_status.value):
                    terminate_status.value = 0
                    read_nail_intensity_process.terminate()
                    read_nail_intensity_process.join()
            
        
    except:
        servo.detach()
        servo.min()
        sleep(0.05)
        servo.detach()
        servo_process.terminate()
        camera_process.terminate()
        servo_process.join()
        camera_process.join()
        exit()
    
    
    """
    try : 
        # Detach servo
        servo.detach()
        servo.min()
        sleep(0.1)
        servo.detach()
        
        # Start servo process and camera process
        servo_process.start()
        camera_process.start()
        
        # Join these 2 processes together for parallelly running.
        servo_process.join()
        camera_process.join()
        
        # If terminate status is true, then terminate servo process and camera process
        # and start read nail intensity process
        if bool(terminate_status.value):
        
            servo_process.terminate()
            camera_process.terminate()
            manager=mp.Manager()

            # creating a lock object
            lock = mp.Lock()

            list_x = manager.list()
            list_y = manager.list()
            list_x.append(0)
            list_y.append(0)
            
            read_nail_intensity_process = mp.Process(target=read_nail_intensity, args=( list_x, list_y, lock))
            # real_time_plotting_process = mp.Process(target=real_time_plotting, args=( list_x, list_y, lock))
            # เธเธ” servo
            
            read_nail_intensity_process.start()
            # real_time_plotting_procsess.start()
            real_time_plotting(list_x, list_y, lock)
            read_nail_intensity_process.join()
            
        
    # If found any error during running, then detach servo and terminate all processes.
    except:
        servo.min()
        sleep(0.05)
        servo.detach()
        servo_process.terminate()
        camera_process.terminate()
"""
