from starlette.responses import JSONResponse
from server.auth import jwt_authentication
from server.settings import notify,s3Client,AWS_STORAGE_BUCKET_NAME,AWS_BASE_URL
from .models import Rooms
import json
import datetime
import os 

#new
import pymongo
from bson.json_util import dumps, loads

connection_uri = "mongodb+srv://myworld:myworld@cluster0.g3hr1.mongodb.net/cluster0?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_uri,connect=False)
myspace_db = client["myspace"]
room_db = myspace_db["rooms"]

def parse_json(data):
    """function to parse data as a json"""
    return json.loads(dumps(data))

# @jwt_authentication
async def uploadRoomPicture(request):
    print('calling upload view')
    # import pdb; pdb.set_trace();
    try:
        room_code= request.path_params['room_code']
        form = await request.form()
        current_time=int(datetime.datetime.utcnow().timestamp())
        thumbnail = f"media/room_thumbnail/Thumbnail{room_code}_{current_time}.jpg"
        upload_thumbnail = await form["thumbnail"].read()
        # create path if not exist
        if not os.path.exists(thumbnail):
            os.makedirs(os.path.dirname(thumbnail), exist_ok=True)
        
        with open(thumbnail,"wb+") as f:
            f.write(upload_thumbnail)
        s3 = s3Client()
        s3.upload_file(
            thumbnail,
            AWS_STORAGE_BUCKET_NAME,
            thumbnail[6:],
            ExtraArgs={"ACL": "public-read"}
        )
        room = Rooms()
        room.uploadThumbnail(room_code,AWS_BASE_URL + thumbnail[6:])
        room.close()
        return JSONResponse({"message":"Thumbnail Uploaded Successfully","status":True})

    except Exception as e:

        return JSONResponse({"message":str(e),"status":False},status_code=400)


async def getallrooms(request):
    try:
        
        # res = loads(dumps(client.myspace_db.room.find( {} )))
        room = Rooms()
        res = room.allRooms() #find rooms at room collection
        res = parse_json(res)
        room.close()
        if not res :

            res={
                "message":"success",
                "data":[],
                "status":True
            }
            
        
        return JSONResponse(res,status_code=200)
    except Exception as e:
        return JSONResponse({"message":str(e),"status":False},status_code=400)

@jwt_authentication
async def createRoom(request):
    try:
        profile_id = request.user_id

        form = await request.json()

        room = Rooms()

        if not form["private"]:
            room_name = room.create(profile_id,form['room_code'],form["title"],form["category"],form["schedule"],form["private"])

        else:
            room_name = room.create(profile_id,form['room_code'],form["title"],form["category"],form["schedule"],form["private"],form["users"])
            
        
        res={
            "message":"Success",
            "data":{
                "unique_room_name":room_name
            },
            "status":True
        }

        room.close()
        return JSONResponse(res,status_code=200)
    
    except Exception as e:
        return JSONResponse({"message":str(e),"status":False},status_code=400)


async def getRoom(request):

    try:
        room_code = request.path_params["room_code"]

        room = Rooms()

        res = room.get(room_code)
        # serialize data
        res = parse_json(res)        
        room.close()
        if res["status"]:

            return JSONResponse(res,status_code=200)

        return JSONResponse(res,status_code=400)
    
    except Exception as e:
        return JSONResponse({"message":str(e),"status":False},status_code=400)

@jwt_authentication
async def addRoom(request):
    try:
        user_id = request.user_id

        data = await request.json()
        room = Rooms()

        status=room.status(data["room_code"], user_id)
        if(status == "Room is full" or status == "Listener already exist"):
            room.close()
            return JSONResponse({"message":status,"status":False},status_code=400)
        creator = room.getCreator(data["room_code"])
        room_code=data["room_code"]
        try:
            token=room.token(creator['_id'])
        except Exception as e:
            print(e)
            pass
            # return JSONResponse({"message":"Creator is not online","error":e,"status":False},status_code=400)
        image=room.getImage(user_id)
        cn=room.getChannelName(user_id)
        try:
            notify(token,f"{cn} wants to join your room","Room Request",data["room_code"],creator['_id'],image)
        except Exception as e:
            print(str(e))
            pass 
            # return JSONResponse({"message":"Error in sending notification","error":str(e),"status":False},status_code=400)
        res={
            "message":"Success",
            "data":room.storePending(data["room_code"], user_id), #store pending listeners
            "status":True
        }
        room.close()
        
        return JSONResponse(res,status_code=200)
    
    except Exception as e:
        print(str(e))
        return JSONResponse({"message":str(e),"status":False},status_code=400)

@jwt_authentication
async def getPending(request):
    try:
        user_id = request.user_id

        room_code = request.path_params["room_code"]

        room = Rooms()        

        res={
            "message":"Success",
            "data":parse_json(room.getPending(room_code, user_id)),
            "status":True
        }
        room.close()

        return JSONResponse(res,status_code=200)

    except Exception as e:
        return JSONResponse({"message":str(e),"status":False},status_code=400)

@jwt_authentication
async def acceptPending(request):
    #import pdb; pdb.set_trace();
    try:
        user_id = request.user_id

        data = await request.json()
        room = Rooms()  

        res={
            "message":"Success",
            "data":room.acceptPending(data["room_code"], data["listeners"]),
            "status":True
        }
        image=room.creatorPP(data["room_code"])
        for i in data["listeners"]:
            try:
                notify(room.token(i),"Your request to join room granted","Request Granted",data["room_code"],i,image)
            except Exception as e:
                return JSONResponse({"message":"Error in sending notification","error":str(e),"status":False},status_code=400)

        room.close()
        return JSONResponse(res,status_code=200)

    except Exception as e:
        return JSONResponse({"message":str(e),"status":False},status_code=400)

@jwt_authentication
async def addPublicListner(request):
    try:
        room = Rooms()

        user_id=request.user_id

        room_code = request.path_params["room_code"]
        
        # add listener to room
        res=room.addPublic(room_code, user_id)
        res = parse_json(res)
        room.close()
        print(res)

        return JSONResponse({'message':res},status_code=200)

    except Exception as e:
        print(e)
        return JSONResponse({"message":str(e),"status":False},status_code=400)


@jwt_authentication
async def removeListner(request):
    try:
        room = Rooms()

        user_id=request.path_params["profile_id"]
        room_code = request.path_params["room_code"]
        res=room.remove_listner(user_id,room_code)
        res = parse_json(res)
        room.close()

        return JSONResponse(res,status_code=200)

    except Exception as e:
        return JSONResponse({"message":str(e),"status":False},status_code=400)

async def liveRoom(request):
    try:
        room = Rooms()
        res=room.getlive_rooms()
        res = parse_json(res)
        # print(res)
        if not res :

            res={
            "message":"success",
            "data":" No live rooms available at the moment ",
            "status":True
            }
            return JSONResponse(res,status_code=200)
        room.close()
        return JSONResponse(res,status_code=200)
    except Exception as e:
        return JSONResponse({"message":str(e),"status":False},status_code=400)

@jwt_authentication    
async def startRoom(request):
    try:
        room_code = request.path_params["room_code"]
        
        form = await request.json()

        room = Rooms()
        
        sdpCandidate=form["sdpCandidate"]
        sdpMLineIndex =form["sdpMLineIndex"]
        sdpMid =form["sdpMid"]
        serverUrl=form["serverUrl"]
        type=form["type"]

        res= room.start_room(room_code,sdpCandidate,sdpMLineIndex,sdpMid,serverUrl,type)
        res = parse_json(res)
        room.close()
        if res["status"]:

            return JSONResponse(res,status_code=200)

        return JSONResponse(res,status_code=400)
    
    except Exception as e:
        return JSONResponse({"message":str(e),"status":False},status_code=400)
        
@jwt_authentication
async def deleteRoom(request):
    try:
        room_code = request.path_params["room_code"]

        room = Rooms()
        res= room.delete(room_code)
        res = parse_json(res)
        room.close()
        if res["status"]:
            return JSONResponse(res,status_code=200)

        return JSONResponse(res,status_code=400)
    except Exception as e:
        return JSONResponse({"message":str(e),"status":False},status_code=400)

@jwt_authentication
async def saveSDP(request):
    try:
        room_code = request.path_params["room_code"]
        profile_id = request.path_params["profile_id"]
        
        form = await request.json()
        room = Rooms()

        sdpCandidate=form["sdpCandidate"]
        sdpMLineIndex =form["sdpMLineIndex"]
        sdpMid =form["sdpMid"]
        serverUrl=form["serverUrl"]
        type=form["type"]

        res=room.save_SDP(room_code,profile_id,sdpCandidate,sdpMLineIndex,sdpMid,serverUrl,type)
        res = parse_json(res)
        room.close()
        if res["message"]=="Room Not Found":
            return JSONResponse(res,status_code=404)
        return JSONResponse(res,status_code=200)
    
    except Exception as e:
        return JSONResponse({"message":str(e),"status":False},status_code=400)


async def roomTimeline(request):
    try:
        room = Rooms()
        # return all live rooms
        res = parse_json(room.allRooms())
        room.close()
        return JSONResponse({"message": res, "status": True},  status_code=200)
    except Exception as e:
        return JSONResponse({"message": str(e), "status":False}, status_code=400)
        
@jwt_authentication
async def getUserRoomsListners(request):
    """ function to get details of listners in rooms"""
    try:
        user_id = request.user_id
        room = Rooms()
        res = room.prevRoomListners(user_id)
        res = parse_json(res)
        room.close()
        return JSONResponse({"message":res,"status":True},status_code=200)
    except Exception as e:
        return JSONResponse({"message":str(e),"status":False}, status_code=400)
        
 
 

