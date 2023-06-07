from starlette.responses import JSONResponse
from server.auth import jwt_authentication
from server.settings import notify
from .models import Rooms


async def addActiveListner(request):
    try:
        room = Rooms()

        user_id=request.user_id

        print(user_id)

        room_code = request.path_params["room_code"]
        print(room_code)

        res, count = room.addPublic(room_code, user_id)

        room.close()

        return JSONResponse(res,status_code=200)


async def remove_active_Listner(request):
    try:
        room = Rooms()

        user_id=request.path_params["profile_id"]
        print(user_id)
        room_code = request.path_params["room_code"]
        print(room_code)
        res, count =room.remove_active_listner(user_id,room_code)

        room.close()

        return JSONResponse(res,status_code=200)

    except Exception as e:
        return JSONResponse({"message":str(e),"status":False},status_code=400)