import socketio
import pymongo
import uuid
sio = socketio.AsyncServer(cors_allowed_origins='*',async_mode="asgi")
app = socketio.ASGIApp(sio)


#socket_io = socketio.AsyncServer()
#socket_io.attach(web_app)

connection_uri = "mongodb+srv://myworld:myworld@cluster0.g3hr1.mongodb.net/cluster0?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_uri,connect=False)

myspace_db = client["myspace_db"]
room_db = myspace_db["room"]
room_sdp = myspace_db["sdp"]

@sio.event
async def connect(sid, environ):
    print(sid, "connected")

@sio.event
async def disconnect(sid):

    #room_created_by = room_db.find_one({"client_connected": { "$in" : [sid] }})
    room_created_by = room_db.find_one({"client_connected": sid})
    print(room_created_by)
    room_count = room_created_by["room_count"]
    room_count -= 1

    # Updating room_count in db
    room_db.update_one({"client_connected": sid}, {"$set": {"room_count": room_count}})

    # Removing sid from client_connected while disconnecting
    room_sdp.delete_one({"sid": sid})
    room_db.update_one({"client_connected": sid}, {"$pull": {"client_connected": sid}})

    if room_created_by["room_created"] == sid:
        sio.leave_room(sid, room_created_by["room_id"])

    print(sid, "disconnected")


@sio.on("create or join")
async def create_or_join_room(sid, data):
    room = data["room"]  # room_1
    
    # Try to getting existing room's data
    try:
        room_dict = room_db.find_one({"room_id": room})  # Checks the presence of room
        room_dict_id = room_dict["_id"]
        room_count = room_dict["room_count"]
        
    except:
        room_dict = False

    # Joining a room if it already exists in db
    if room_dict:
        sio.enter_room(sid, room)  # Joins the room
        await sio.emit("join", {"room": room,"sid":sid}, to=room)  # Emits to 'join' event
        print(f"{sid} joined room : {room}")
        room_count += 1
        # Updating room count in room
        room_db.update_one(
            {"room_id": room}, {"$set": {"room_count": room_count}}
        )
        room_db.update_one(
            {"room_id": room}, {"$push": {"client_connected": sid}}
        )
        
    # Creating a room and storing in database
    else:
        sio.enter_room(sid, room)  # Creates a room
        room_dict = {"_id":str(uuid.uuid4()),"room_id": room, "room_created": sid, "room_count": 1}  # Room data
        room_db.insert_one(room_dict)  # Inserts room data to db
        room_db.update_one(
            {"room_id": room}, {"$push": {"client_connected": sid}}
        )  
        
        # Updates client connected to room
        await sio.emit(
            "created", {"room": room, "sid": sid}, to=sid
        )  
        # Emits event 'joined' to client
        print(f"{sid} created room: {room}")  # Status in terminal




#for setting sdp for a socketid
@sio.on("message")
async def set_room_clients(sid,data):
    print("Into Message event : "+str(data))
    #for first time peer connection
    try:
        print("Running Message Event TRY")
        type = data["type"]
        label = data["label"]
        candidate = data["candidate"]
        id = data["id"]
        xfrom = data["from"]
        to = data["to"]
        #part = data["part"]
        final_dict = {"sid":sid,"type":type,"label":label,"candidate":candidate,"id":id,"from":xfrom,"to":to}
        print(final_dict)
        await sio.emit("message response",final_dict,to=to)
        print("Try Done")
    #for creating offer
    except:
        print("Running Message Event EXCEPT")
        type = data["type"]
        sdp = data["sdp"]
        xfrom = data["from"]
        to = data["to"]
        part = data["part"]
        final_dict = {"sid":sid,"type":type,"sdp":sdp,"from":xfrom,"to":to,"part":part}
        await sio.emit("message response",final_dict,to=to)

    room_dict = room_sdp.update_one({"sid" : sid},{"$set": final_dict},True)
    

#for getting sdp variable in DB
@sio.on("get room sdp")
async def get_room_clients(sid):
    res = {}
    room_dict = room_sdp.find_one({"sid": sid})
    for i in room_dict:
        if i != "_id":
            res[i] = room_dict[i]
    print(res)
    await sio.emit("get room clients response",res,to=sid)


@sio.on("all")
async def get_room_clients(sid):
    print("Running All")
    res = {}
    room_dict = room_sdp.find_one({"sid": sid})
    for i in room_dict:
        if i != "_id":
            res[i] = room_dict[i]
    print("Res -> "+str(res))
    await sio.emit("all response",res,to=sid)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)

