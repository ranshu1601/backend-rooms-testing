from starlette.routing import Route
from .views import page_not_found
from rooms.urls import rooms_urlpatterns
from rooms.routing import room_socketpatterns
from viewtracker.routing import vt_socketpatterns
from viewtracker.urls import views_urlpatterns
from like_comment.urls import lc_urlpatterns
from like_comment.routing import lc_socketpatterns

urlpatterns=[
    Route('/', page_not_found, methods=["GET","POST"]),
]

urlpatterns.extend(rooms_urlpatterns)
urlpatterns.extend(room_socketpatterns)
urlpatterns.extend(vt_socketpatterns)
urlpatterns.extend(views_urlpatterns)
urlpatterns.extend(lc_urlpatterns)
urlpatterns.extend(lc_socketpatterns)
