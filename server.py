import asyncio
import websockets
import os

sender = None
viewer = None

async def handler(ws):
    global sender, viewer

    role = await ws.recv()

    if role == "SENDER":
        sender = ws
        print("Sender connected")
        try:
            async for msg in ws:
                if viewer:
                    await viewer.send(msg)
        finally:
            sender = None

    elif role == "VIEWER":
        viewer = ws
        print("Viewer connected")
        try:
            await ws.wait_closed()
        finally:
            viewer = None

async def main():
    port = int(os.environ.get("PORT", 10000))
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()

asyncio.run(main())


