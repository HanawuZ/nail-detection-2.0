##############################################################
# Contributed by Pet002
##############################################################
# use this custom pin-factory to fix servo jitter. 
# IMPORTANT: make sure pigpio deamon is running: 'sudo pigpiod'
from gpiozero import Servo, Button
from time import sleep

# create a custom pin-factory to fix servo jitter
# more info here: https://gpiozero.readthedocs.io/en/stable/api_output.html#servo
# and here: https://gpiozero.readthedocs.io/en/stable/api_pins.html


servo = Servo(17)

"""
while True:
    servo.detach()
    servo.min()
    print("servo min")
    sleep(3)

    servo.mid()
    print("servo mid")
    sleep(3)

    servo.max()
    print("servo max")
    sleep(3)
"""
# Initialize gpio 21 for button press
press_button = Button(21)

# Function for normalize servo press degree
def Normalize(deg):
    return ((deg ) / (90)) * (1 - (-1)) + (-1)

try:
    servo.min()
    while True:
        sleep(0.1)
        servo.detach()
        sleep(0.1)
        servo.value = Normalize(75)
        sleep(0.5)
        servo.detach()
        sleep(5)
        servo.min()
        sleep(0.5)
        servo.detach()
        
except KeyboardInterrupt:
    servo.min()
    sleep(0.1)
    servo.detach()
    print("program stopped")
    

# servo.min()
# sleep(0.1)
# servo.detach()
