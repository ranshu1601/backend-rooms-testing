from .consumers import LikeCommentViewSocket
from starlette.routing import WebSocketRoute

lc_socketpatterns = [
    WebSocketRoute("/ws/room", LikeCommentViewSocket),
]