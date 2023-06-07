from starlette.routing import Route
from .views import getViews

views_urlpatterns=[
    Route('/views/{room_code:str}', getViews, methods=["GET"])
]