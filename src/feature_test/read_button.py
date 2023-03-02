from gpiozero import Button
from time import sleep

# Initialize button object with gpio 21
button = Button(21)

while True:
    if button.is_pressed:
        print("Button is pressed")
    else:
        print("Button is not pressed")
    sleep(0.1)