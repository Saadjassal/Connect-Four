from websockets.asyncio.server import broadcast, serve
import asyncio
import json
import secrets
from connect4 import PLAYER1, PLAYER2, Connect4


JOIN = {}
WATCH = {}

async def error(websocket, message):
    event = {
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))


async def replay(websocket, game):

    for player, column, row in game.moves.copy():
        event = {
            "type": "play",
            "player": player,
            "column": column,
            "row": row,
        }
        await websocket.send(json.dumps(event))


async def play(websocket, game, player, connected):
 
    async for message in websocket:
       
        event = json.loads(message)  # Parse a "play" event from the UI.
        assert event["type"] == "play"
        column = event["column"]

        try:
            row = game.play(player, column)
        except ValueError as exc:
            # Send an "error" event if the move was illegal.
            await error(websocket, str(exc))
            continue

        # Send a "play" event to update the UI.
        event = {
            "type": "play",
            "player": player,
            "column": column,
            "row": row,
        }
        broadcast(connected, json.dumps(event))

        # If move is winning, send a "win" event.
        if game.winner is not None:
            event = {
                "type": "win",
                "player": game.winner,
            }
            broadcast(connected, json.dumps(event))


async def start(websocket):
  
    game = Connect4()
    connected = {websocket}

    join_key = secrets.token_urlsafe(12)
    print(f"http://127.0.0.1:8000/?join={join_key}")
    JOIN[join_key] = game, connected

    watch_key = secrets.token_urlsafe(12)
    print(f"http://127.0.0.1:8000/?watch={watch_key}")
    WATCH[watch_key] = game, connected

    try:
        event = {
            "type": "init",
            "join": join_key,
            "watch": watch_key,
        }
        await websocket.send(json.dumps(event))
        # Receive and process moves from the first player.
        await play(websocket, game, PLAYER1, connected)
    finally:
        del JOIN[join_key]
        del WATCH[watch_key]


async def join(websocket, join_key):
   
    # Find the Connect Four game.
    try:
        game, connected = JOIN[join_key]
    except KeyError:
        await error(websocket, "Game not found.")
        return

    # Register to receive moves from this game.
    connected.add(websocket)
    try:
        # Send the first move, in case the first player already played it.
        await replay(websocket, game)
        # Receive and process moves from the second player.
        await play(websocket, game, PLAYER2, connected)
    finally:
        connected.remove(websocket)


async def watch(websocket, watch_key):
   
    # Find the Connect Four game.
    try:
        game, connected = WATCH[watch_key]
    except KeyError:
        await error(websocket, "Game not found.")
        return

    
    connected.add(websocket)# Register
    try:
        await replay(websocket, game)
        await websocket.wait_closed()
    finally:
        connected.remove(websocket)


async def handler(websocket):
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"

    if "join" in event:
        await join(websocket, event["join"])
    elif "watch" in event:
        await watch(websocket, event["watch"])
    else:
        await start(websocket)


async def main():
    async with serve(handler, "", 8001) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())