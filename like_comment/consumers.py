from json import dumps
from server.settings import group
from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocketState

class LikeCommentViewSocket(WebSocketEndpoint):

    def __init__(self, scope, receive, send):
        super().__init__(scope, receive, send)
        group.group_add("room", self)

    async def on_connect(self, websocket):
        self.websocket = websocket
        await self.websocket.accept()

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
        group.group_discard("room", self)
        await self.websocket.close()


