import aiofiles
from aiofiles.os import stat
import os
import websockets
import json
from typing import IO
from firebird import SESSIONS
from datetime import datetime


__all__ = [
    'get_events',
    'monitor_logs'
]
LOG_PATH = os.getenv('LOG_PATH', '/var/log/monitor/temp.log')
DATE_FORMAT = os.getenv('DATE_FORMAT', '%Y-%m-%d %H:%M:%S,%f')


async def monitor_logs(log_path=LOG_PATH):
    """Monitor `log_path` for changes and get event on change"""
    last_modified = 0

    while True:
        details = await stat(log_path)
        if details.st_mtime > last_modified and SESSIONS:
            last_modified = details.st_mtime
            events = await get_events(log_path)
            websockets.broadcast(SESSIONS, json.dumps(events))


async def gather_events(filename=LOG_PATH, count=1):
    return await get_events(filename, count)


async def get_events(filename=LOG_PATH, count=1):
    """
    Get the `count` last events from `filename`. 
    """
    events_found = 0
    events = []

    async with aiofiles.open(filename, 'rb') as f:
        try:
            await f.seek(0, os.SEEK_END)

            # Find `count` newline characters
            while events_found < count:
                # Move cursor to one before the last '\n' in the file so that we don't immediately find
                # a newline
                await f.seek(-2, os.SEEK_CUR)

                while await f.read(1) != b'\n':
                    await f.seek(-2, os.SEEK_CUR)
                events_found += 1

            # Process each line and turn into an event
            for _ in range(events_found):
                events.append(await parse_event(f))
        except OSError:
            await f.seek(0)
            events.append(await parse_event(f))

        return events


async def parse_event(f:IO):
    last_line = await f.readline()
    timestamp, level, temperature = last_line.decode().split(' - ')
    event = {
        'timestamp': datetime.strptime(timestamp, DATE_FORMAT).isoformat(),
        'temperature': float(temperature.replace('\'C', ''))
    }
    return event
