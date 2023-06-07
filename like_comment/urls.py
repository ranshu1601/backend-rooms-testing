from starlette.routing import Route
from .views import commentRoom, getViews, likeUser, checkLikes

lc_urlpatterns = [
    Route('/comment/', commentRoom, methods=["POST","DELETE"]),
    Route('/get/{id:str}', getViews, methods=["GET"]),
    Route('/user/room_likes/{id:str}', checkLikes, methods=["GET"]),
    Route('/like/', likeUser, methods=["POST"]),
    
]
