import asyncio
import websockets
from firebird import SESSIONS
from firebird.watcher import monitor_logs
import os
import json
import logging
import logging.config


__all__  = [
    'main'
]
PORT = os.getenv('INTERNAL_WS_PORT', 8001)
INSTANCE_PATH = os.getenv('INSTANCE_PATH')


def get_logger(config_path=None):
    config_path = config_path or os.path.join(INSTANCE_PATH, 'logging.conf')
    logging.config.fileConfig(config_path)
    return logging.getLogger('watcher')


async def handler(websocket):   
    SESSIONS.add(websocket)
    update_connection_count()
    logger.info(f'Session added: {websocket}')
    try:
        await websocket.wait_closed()
    finally:
        SESSIONS.remove(websocket)
        update_connection_count()
        logger.info(f'Session removed: {websocket}')

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
    global logger 
    logger = get_logger()
    asyncio.run(main())