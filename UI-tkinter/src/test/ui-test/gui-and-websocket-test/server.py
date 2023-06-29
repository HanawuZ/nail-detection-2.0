import asyncio
import websockets

async def server(websocket, path):
    request = await websocket.recv()
    print("Received request:", request)
        
async def main():
    async with websockets.serve(server, "localhost", 8765):
        await asyncio.Future()    
    

if __name__ == "__main__":
    asyncio.run(main())


