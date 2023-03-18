import asyncio
import websockets
import json
from models import PLAYER1, PLAYER2, Connect4


async def handler(websocket):
    game = Connect4()
    players = [PLAYER1, PLAYER2]
    player_idx = 0

    async for message in websocket:
        event = json.loads(message)
        responses = [{'type': 'error', 'message': 'Unknown event'}]

        if event.get('type') == 'play':
            player = players[player_idx]
            column = event.get('column')

            try: 
                row = game.play(player, column=column)
                responses[0] = {'type': 'play', 'player': player, 'column': column, 'row': row}
                player_idx = (player_idx + 1) % 2
            except RuntimeError:
                responses[0] = {'type': 'error', 'message': 'Illegal move. Try again'}

            if game.winner:
                responses.append({'type': 'win', 'player': game.winner})

            for response in responses:
                await websocket.send(json.dumps(response))

async def main():
    async with websockets.serve(handler, '', 8001):
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())