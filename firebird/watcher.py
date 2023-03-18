import asyncio
import websockets
import json
import os
from time import sleep


__all__ = [
    'run'
]


async def handler(websocket):
    temperature_log_path = '/var/log/monitor/temp.log'
    last_modified = 0

    while True:
        details = os.stat(temperature_log_path)

        if details.st_mtime > last_modified:
            last_modified = details.st_mtime
            with open(temperature_log_path, 'rb') as f:
                try:
                    f.seek(-2, os.SEEK_END)
                    while f.read(1) != b'\n':
                        f.seek(-2, os.SEEK_CUR)
                except OSError:
                    f.seek(0)
                last_line = f.readline().decode()
                print(last_line.strip())
                timestamp, level, temperature = last_line.split(' - ')
            event = {
                'timestamp': timestamp,
                'temperature': temperature
            }
            await websocket.send(json.dumps(event))
        # sleep(1)


async def main():
    async with websockets.serve(handler, '', 8001):
        await asyncio.Future()


def run():
    asyncio.run(main())


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        pass