# from starlette.routing import Route
# from .views import createRoom, getRoom, addRoom, acceptPending, getPending,liveRoom,deleteRoom,removeListner,addPublicListner,saveSDP,startRoom

# rooms_urlpatterns=[
#     Route('/create_room/',createRoom, methods=["POST"]),
#     Route('/get_room/{room_code:str}',getRoom, methods=["GET"]),
#     Route('/add/',addRoom, methods=["POST"]),
#     Route('/add_active_Public/{room_code:str}',addPublic, methods=["GET"]),
#     Route('/accept/',acceptPending, methods=["POST"]),
#     Route('/list/{room_code:str}',getPending, methods=["GET"]),
#     Route('/remove_listner/{room_code:str}/{profile_id:str}',removeListner, methods=["GET"]),
#     Route('/start_room/{room_code:str}',startRoom,methods=["POST"]),
#     Route('/live_rooms/',liveRoom, methods=["GET"]),
#     Route('/save_SDP/{room_code:str}/{profile_id:str}',saveSDP, methods=["POST"]),
#     Route('/delete_room/{room_code:str}',deleteRoom, methods=["GET"]),
# ]