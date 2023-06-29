from time  import sleep
import pigpio
pi = pigpio.pi() # Connect to local Pi.
pi.set_mode(17, pigpio.OUTPUT)
pi.set_servo_pulsewidth(17,1250) #closed
print ("Start")
sleep (0.25)
pi.set_servo_pulsewidth(17, 0)
sleep (5)
pi.set_servo_pulsewidth(17,2500) #closed
sleep(1)
pi.set_servo_pulsewidth(17, 0)