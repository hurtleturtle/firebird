import asyncio
import websockets
from firebird import SESSIONS
from firebird.watcher import monitor_logs
import os

__all__  = [
    'main'
]
PORT = os.getenv('INTERNAL_WS_PORT', 8002)


async def handler(websocket):   
    SESSIONS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        SESSIONS.remove(websocket)


async def serve_websockets():
    async with websockets.serve(handler, '', PORT):
        await asyncio.Future()


async def main():
    server = asyncio.create_task(serve_websockets())
    logs = asyncio.create_task(monitor_logs())

    await server
    await logs


def run():
    asyncio.run(main())