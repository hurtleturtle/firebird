import asyncio
import websockets
from firebird import SESSIONS
from firebird.watcher import monitor_logs
import os
import json


__all__  = [
    'main'
]
PORT = os.getenv('INTERNAL_WS_PORT', 8001)


async def handler(websocket):   
    SESSIONS.add(websocket)
    update_connection_count()
    try:
        await websocket.wait_closed()
    finally:
        SESSIONS.remove(websocket)
        update_connection_count()

def update_connection_count():
    websockets.broadcast(SESSIONS, json.dumps({'connections': len(SESSIONS)}))


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