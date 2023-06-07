from starlette.endpoints import WebSocketEndpoint
from .models import ViewTracker
from like_comment.views import sendData


class ViewTrackingSocket(WebSocketEndpoint):
    encoding = 'json'

    async def on_connect(self,websocket):
        await websocket.accept()
        self.vt = ViewTracker()

    async def on_receive(self, websocket, data):
        try:
            if data["duration"]>5:
                self.vt.create(data["id"], data["room_code"], data["duration"])

            await websocket.send_json({"message":"success"})

            self.vt.total(data["room_code"])

            await sendData(data["room_code"])

        except Exception as e:
            await websocket.send_json({"message":str(e)})

    async def on_disconnect(self, websocket, close_code):
        await websocket.close()
        self.vt.close()
