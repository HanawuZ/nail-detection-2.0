from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gpiozero import Servo
from time import sleep

servo = Servo(17)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hello_world() -> str:
    print("Test")
    servo.max()
    sleep(1)
    
    return "Hello World"
    
servo.detach()

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8080)) # in this case will get a port in docker if it can be running in docker but if not will use port 8080 to running
    uvicorn.run(app, host="0.0.0.0", port=port)
