from json import dumps
from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocketState
from .models import Rooms
from server.auth import jwt_authentication_socket
from server.settings import group

async def sendData(data):
    
    await group.group_send("room", data=data)
    
class RoomSocket(WebSocketEndpoint):

    encoding = "json"

    def __init__(self, scope, receive, send):
        super().__init__(scope, receive, send)
        group.group_add("room", self)

    async def on_connect(self, websocket):
        self.websocket=websocket
        token = self.websocket.path_params['token']
        res, self.user_id = await jwt_authentication_socket(token)
        await self.websocket.accept()
        if res:
            self.room = Rooms()
        else:
            self.websocket.send_json({"message":"User not Authenticated","status":False})
            await self.websocket.close()

    #async def on_receive(self, websocket, data):


    async def broadcast(self, data: dict):
        if self.websocket.application_state == WebSocketState.CONNECTED:
            await self.websocket.send(message={
                "type": "websocket.send",
                "text": dumps(data)
            })
            return True
        else:
            return False


    async def on_disconnect(self, websocket, close_code):
        await self.websocket.close()
        self.room.close()

