from bson.json_util import dumps, loads
from server.settings import clientOpen
from datetime import datetime

class Rooms:

    def __init__(self):
        
        self.client=clientOpen()
    
    def addPublic(self, room_name, user_id):
        active_listener=loads(dumps(self.client.auth.profile.find_one({"_id":user_id})))
        if not active_listener:
            return "Active Listner Not found"
        room=loads(dumps(self.client.myspace.rooms.find_one({"room_code":room_name})))
        if not room:
            return "Room not found"
        
        self.client.myspace.rooms.update({"room_code":room_name},
            {
                "$push":{
                    "active_listeners":{
                        "_id":active_listener["_id"],
                        "profile_picture":active_listener["profile_picture"],
                        "channel_name":active_listener["channel_name"],
                        "name":active_listener["name"]
                    }
                }
            }
        )
        # len(self.client)
        count=0
        return "Active Listener added"  , count


    def remove_active_listner(self,profile,room_name):
        active_listener=loads(dumps(self.client.auth.profile.find_one({"_id":profile})))
        if not active_listener:
            res={
                "message":"User Not Found",
                "status":True
            }
            return res
        data=self.client.myspace.rooms.find_one({"room_code":room_name})
        if not data:
            res={
                "message":"Room not found",
                "status":True
            }
            return res, count