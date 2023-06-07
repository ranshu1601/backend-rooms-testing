from starlette.responses import JSONResponse
from server.auth import jwt_authentication
from .models import Comment, LikeCommentView, Like
from server.settings import group, notify

async def sendData(room_code):
    lcv = LikeCommentView()

    await group.group_send("room", data=lcv.get(room_code))

    lcv.close()


@jwt_authentication
async def commentRoom(request):
    try:
        profile_id = request.user_id
        data = await request.json()
        comment = Comment()

        if request.method == 'POST':
            res = comment.create(profile_id, data["room_code"], data["comment"])
            await sendData(data["room_code"])
        else :
            res = comment.delete(data["room_comment_id"], data["comment_id"])

        comment.close()

        return JSONResponse({"message":res, "status": True})
    except Exception as e:
        return JSONResponse({"message":str(e),"status":False},status_code=400)


#@jwt_authentication
async def likeUser(request):
    try:
        #profile_id = request.user_id

        data = await request.json()

        like = Like()
        #For Room User Like
        #res = like.create_or_delete(profile_id, data["user_id"], data ["room_code"])

        res = like.create_or_delete(data["user_id"], data ["room_code"]) 
        
        #await sendData(data["room_code"])

        like.close()

        return JSONResponse({"message":res, "status": True})

    except Exception as e:
        return JSONResponse({"message":str(e), "status": False},status_code=400)


async def checkLikes(request):
    try:
        user_id = request.path_params["id"]
        like = Like()
        res = like.checkUserLikes(user_id)
        like.close()
        return JSONResponse({"message":res, "status": True})
    except Exception as e:
        return JSONResponse({"message":str(e), "status": False},status_code=400)
        

async def getViews(request):
    try:
        data = request.path_params["id"]
        res = LikeCommentView()
        result = res.get(data)
        res.close()

        return JSONResponse({"message":"Success", "data":result, "status":True})

    except Exception as e: 
        return JSONResponse({"message":str(e),"status":False},status_code=400) 
