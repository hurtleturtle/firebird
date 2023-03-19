import asyncio
import websockets
from firebird import SESSIONS
from firebird.watcher import monitor_logs

__all__  = [
    'main'
]


async def handler(websocket):   
    SESSIONS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        SESSIONS.remove(websocket)


async def serve_websockets():
    async with websockets.serve(handler, '', 8001):
        await asyncio.Future()


async def main():
    server = asyncio.create_task(serve_websockets())
    logs = asyncio.create_task(monitor_logs())

    await server
    await logs


def run():
    asyncio.run(main())