from bson.json_util import dumps, loads
from server.settings import clientOpen
from datetime import datetime

class ViewTracker:

    def __init__(self):

        self.client = clientOpen()

    def total(self, room_code):
        total_duration = count = 0
        for i in loads(dumps(self.client.rooms.viewtracker.find({"room_code":room_code}))):
            total_duration += i["duration"]
            count += 1

        if self.client.rooms.views.find_one({"_id":{"$regex":room_code}}):
            self.client.rooms.views.update_one({"_id":{"$regex":room_code}},{"$set":{"total_duration":total_duration}})

            self.client.rooms.views.update_one({"_id":{"$regex":room_code}},{"$set":{"total_viewers":count}}) 

        else:
            self.client.rooms.views.insert_one({
                "_id":room_code+str(datetime.utcnow().timestamp()),
                "id":room_code,
                "total_duration":total_duration,
                "total_viewers":count
            })

    def create(self, id, room_code, duration):
        if c:=self.client.rooms.viewtracker.find_one({"room_code":room_code, "id":id}):
            if c["duration"]<duration:
                self.client.rooms.viewtracker.update({"room_code":room_code, "id":id},{"$set":{"duration":duration}})

        else:
            user = self.client.auth.profile.find_one({"_id":id})
            profile_picture = user["profile_picture"]
            channel_name = user["channel_name"]
            
            self.client.rooms.viewtracker.insert_one({
                "_id":id+str(datetime.utcnow().timestamp()), 
                "id":id,
                "room_code":room_code, 
                "duration":duration, 
                "profile":{"profile_picture":profile_picture, "channel_name":channel_name},
            })

    def get(self,room_code):
        return loads(dumps(self.client.rooms.views.find_one({"_id":{"$regex":room_code}})))
        
    def close(self):
        self.client.close()

    