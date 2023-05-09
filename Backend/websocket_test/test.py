from gpiozero import Servo
from time import sleep
import asyncio
import websockets
import pigpio

pi = pigpio.pi() # Connect to local Pi.
pi.set_mode(17, pigpio.OUTPUT)
pi.set_servo_pulsewidth(17,1250) #closed

async def handler(websocket):
    while True:
        message = await websocket.recv()
        print("Data Received : " + message)
        val = int(message)
        pi.set_servo_pulsewidth(17,val) #closed
        await websocket.send("data : "+message)
	
async def main():
    async with websockets.serve(handler, "0.0.0.0", 8080):
        await asyncio.Future()
	
if __name__ == "__main__":
    asyncio.run(main())
