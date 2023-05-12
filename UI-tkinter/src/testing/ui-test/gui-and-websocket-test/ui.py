import asyncio
import websockets
import tkinter as tk

class App:
    def __init__(self, master):
        self.master = master
        self.websocket = None
        self.button = tk.Button(self.master, text="Send", command=self.send)
        self.button.pack()

    async def connect(self):
        self.websocket = await websockets.connect("ws://localhost:8765")

    async def send_test_string(self):
        await self.connect()
        await self.websocket.send("test")
        await self.websocket.close()
        
    def send(self):
        asyncio.run(self.send_test_string())

root = tk.Tk()
app = App(root)
root.mainloop()