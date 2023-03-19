import asyncio
import aiofiles
from aiofiles.os import stat
import os
import websockets
import json
from time import sleep


__all__ = [
    'run'
]
SESSIONS = set()


async def handler(websocket):
    SESSIONS.add(websocket)
    async for message in websocket:
        event = json.loads(message)



async def monitor_logs():
    temperature_log_path = '/var/log/monitor/temp.log'
    last_modified = 0

    while True:
        details = await stat(temperature_log_path)
        if details.st_mtime > last_modified:
            last_modified = details.st_mtime
            async with aiofiles.open(temperature_log_path, 'rb') as f:
                try:
                    await f.seek(-2, os.SEEK_END)
                    while await f.read(1) != b'\n':
                        await f.seek(-2, os.SEEK_CUR)
                except OSError:
                    await f.seek(0)
                last_line = await f.readline()
                timestamp, level, temperature = last_line.decode().split(' - ')
                event = {
                    'timestamp': timestamp,
                    'temperature': float(temperature.replace('\'C', ''))
                }
                print(SESSIONS, event)
                websockets.broadcast(SESSIONS, json.dumps(event))


async def serve_websockets():
    async with websockets.serve(handler, '', 8001):
        await asyncio.Future()


async def main():
    server = asyncio.create_task(serve_websockets())
    logs = asyncio.create_task(monitor_logs())

    await server
    await logs

def run():
    asyncio.run(main(), debug=True)


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        pass