import asyncio
import websockets

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
    async with websockets.serve(handler, "0.0.0.0", 10000):
        await asyncio.Future()

asyncio.run(main())

