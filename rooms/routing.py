from .consumers import RoomSocket
from .server_socket import *
from starlette.routing import WebSocketRoute

room_socketpatterns=[
    WebSocketRoute("/ws/room/{token:str}", RoomSocket),
    WebSocketRoute("/ws/connect", create_or_join_room),
]
