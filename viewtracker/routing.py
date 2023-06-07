from .consumers import ViewTrackingSocket
from starlette.routing import WebSocketRoute

vt_socketpatterns = [
    WebSocketRoute("/ws/vt", ViewTrackingSocket),
]