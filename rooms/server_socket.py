import socketio
import pymongo

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={"/": "./public/"})

connection_uri = "mongodb+srv://shiyan:Shiyanshiyan1@cluster0.dzenl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_uri)

myspace_db = client["myspace_db"]
room_db = myspace_db["room"]

@sio.event
def connect(sid, environ):
    print(sid, "connected")


@sio.event
def disconnect(sid):
    room_created_by = room_db.find_one({"room_created": sid})
    room_count = room_created_by["room_count"]
    room_count -= 1
    # Updating room_count in db
    room_db.update_one({"client_connected": sid}, {"$set": {"room_count": room_count}})
    room_client_connected_to = room_db.find_one({"client_connected": sid})
    # Removing sid from client_connected while disconnecting
    room_db.update({"client_connected": sid}, {"$pull": {"client_connected": sid}})
    if room_created_by["room_created"] == sid:
        sio.leave_room(sid, room_created_by["room_id"])
    print(sid, "disconnected")


@sio.on("create or join")
def create_or_join_room(sid, data):
    room = data["room"]  # room_1
    # Try to getting existing room's data
    try:
        room_dict = room_db.find_one({"room_id": room})  # Checks the presece of room
        room_dict_id = room_dict["_id"]
        room_count = room_dict["room_count"]
    except Exception:
        pass

    # Joining a room if it already exists in db
    if room_dict:
        sio.enter_room(sid, room)  # Joins the room
        sio.emit("join", {"room": room}, to=room)  # Emits to 'join' event
        print(f"{sid} joined room : {room}")
        room_count += 1
        # Updating room count in room
        room_db.update_one({"room_id": room}, {"$set": {"room_count": room_count}})
        room_db.update({"room_id": room}, {"$push": {"client_connected": sid}})
        # Room full condition
        if room_count > 2:
            sio.emit("full", {"room": room}, to=sid)
            print(f"Room {room} is full, Unable to join")

    # Creating a room and storing in database
    else:
        sio.enter_room(sid, room)  # Creates a room
        room_dict = {"room_id": room, "room_created": sid, "room_count": 1}  # Room data
        room_db.insert_one(room_dict)  # Inserts room data to db
        room_db.update(
            {"room_id": room}, {"$push": {"client_connected": sid}}
        )  # Updates client connected to room
        sio.emit(
            "created", {"room": room, "sid": sid}, to=sid
        )  # Emits event 'joined' to client
        print(f"{sid} created room: {room}")  # Status in terminal


@sio.on("message")
def message(sid, data):
    sio.emit("message", data, to=sid)
