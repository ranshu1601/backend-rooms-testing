from starlette.routing import Route
from .views import getallrooms,createRoom, getRoom, addRoom, acceptPending, getPending,liveRoom,deleteRoom,removeListner,addPublicListner,saveSDP,startRoom,roomTimeline,uploadRoomPicture,getUserRoomsListners

rooms_urlpatterns=[
    Route('/create_room/',createRoom, methods=["POST"]),
    Route('/get_room/{room_code:str}',getRoom, methods=["GET"]),
    Route('/add/',addRoom, methods=["POST"]),
    Route('/addPublic/{room_code:str}',addPublicListner, methods=["GET"]),
    Route('/accept/',acceptPending, methods=["POST"]),
    Route('/list/{room_code:str}',getPending, methods=["GET"]),
    Route('/remove_listner/{room_code:str}/{profile_id:str}',removeListner, methods=["GET"]),
    Route('/start_room/{room_code:str}',startRoom,methods=["POST"]),
    Route('/live_rooms/',liveRoom, methods=["GET"]),
    Route('/save_SDP/{room_code:str}/{profile_id:str}',saveSDP, methods=["POST"]),
    Route('/delete_room/{room_code:str}',deleteRoom, methods=["GET"]),
    Route('/room_timeline/',roomTimeline, methods=["GET"]),
    Route('/get_all_rooms/',getallrooms, methods=["GET"]),
    Route('/roompic/{room_code:str}',uploadRoomPicture, methods=["POST"]),
    Route('/listners',getUserRoomsListners, methods=["GET"])
    
]
