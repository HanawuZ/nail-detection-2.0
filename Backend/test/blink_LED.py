import RPi.GPIO as GPIO
import time

# Configure the PIN # 8
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setwarnings(False)

# Blink Interval 
blink_interval = .5 #Time interval in Seconds

print("Start")

# Blinker Loop
while True:
    GPIO.output(11, True)
    time.sleep(blink_interval)
    GPIO.output(11, False)
    time.sleep(blink_interval)

# Release Resources
GPIO.cleanup()
