# import websocket, json
# from config import *

# socket = #url

# def authenticate(ws):
#     pass

# def get_event(ws, message):
#     pass

# ws = websocket.WebsocketApp(socket, on_open= authenticate, on_message= get_event, on_end= None)
# ws.run_forever()


# import asyncio
# import websockets
# ip='localhost'
# async def echo(websocket, path):
#     async for message in websocket:
#         if message == 'create or join':
#             addPublic()
#             await websocket.send(f'your message is this ' + message)

# asyncio.get_event_loop().run_until_complete(
#     websockets.serve(echo, ip, 8080))
# asyncio.get_event_loop().run_forever()

import socketio
import uvicorn
import asyncio

sio = socketio.AsyncServer(async_mode='asgi')
app= socketio.ASGIApp(sio, static_files={
        '/':'./static/'
})

client_count=0

@sio.event
async def connect(sid, environ):
        print('connected')
        await sio.emit('log', {'array': 'Connection established'})

@sio.on('message')
async def message(sid, message):
        print(f'Client said {message}')
        await sio.emit('message', message, to=sid)

@sio.on('create or join')
async def Join_room(sid,room):
        print(f'Received request to creat or join room ' + room)
        global client_count
        client_count+=1
        if client_count == 0:
            await sio.emit('created', {'room': room,'sid': sid})
        elif  client_count ==1:
            print(f'Client ID '+ sid + 'joined room' + room)
            await sio.emit('joined', {'room': room, 'sid':sid})
        else:
            await sio.emit('full', {'room': room})

@sio.on('disconnect')
async def disconnect(sid):
        print(f'Peer or server disconnected.')
        await sio.emit('bye', {'msg': 'Peer or server disconnected.'})

@sio.on('bye')
async def bye(sid, room):
        print(f'Peer said bye on room {room}')


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8008)
