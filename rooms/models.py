from bson.json_util import dumps, loads
from server.settings import clientOpen,s3Client
from datetime import datetime
import time

class Rooms:

    def __init__(self):
        
        self.client=clientOpen()
    

    def creatorPP(self, room_code):
        creator = self.client.myspace.rooms.find_one({"room_code":room_code}, {"creator":True})["creator"]
        print(creator)
        return creator["profile_picture"]

    def getImage(self, id):
        return self.client.auth.profile.find_one({"_id":id},{"profile_picture":True})["profile_picture"]

    def test(self,profile,title,schedule,room_type,users=[]):

        return loads(dumps(self.client.auth.profile.find_one({"_id":profile})))

    def create(self,profile,room_code,title,category,schedule,room_type=None,users=[]):
        data=loads(dumps(self.client.auth.profile.find_one({"_id":profile})))
        if not data:
            res={
                    "message":"User Not Found",
                    "status":True
                }
            return res
        channel_name=data["channel_name"]
       
        if self.client.myspace.rooms.find_one({"schedule":schedule, "creator":profile}):
    
            raise ValueError("Schedule time is already occupied")
        
        else:

            listener=loads(dumps(self.client.auth.profile.find_one({"_id":profile})))
            creator={
                "_id":listener["_id"],
                "profile_picture":listener["profile_picture"],
                "channel_name":listener["channel_name"],
                "name":listener["name"]
            }
            # room_code = '_'.join(channel_name.split(' '))+"_"+'_'.join(title.split(' '))+"_"+str(schedule)+"_"+str(time.time()).split('.')[0]
            
            room_live_status = False
            # If the schedule time is before or equal to current time then it is live. 
            # On Frontend there should also be check for not allowing the before time than current time.
            # Schedule time is divided by 1000 as it is comming in milliseconds 
            if datetime.fromtimestamp(schedule / 1000) <= datetime.now():
                room_live_status = True
                
            # add categories in user categories
            # self.client.categories.users.insert_one( {
            #         "_id": listener["_id"],
            #         "id": listener["_id"],
            #         "categories":category,
            #         "sub_cat":[],
            #         "sub_category":[]
            #         }
            #  )

            if not room_type:
    
                self.client.myspace.rooms.insert_one({
                    # "_id":profile+"_"+title+"_"+str(datetime.utcnow().timestamp()),
                    # let mongodb generate id 
                    "creator":creator,
                    "title":title,
                    "admin":listener["email"],      # store creator email id to use it for join room event.
                    "schedule":schedule,
                    "private":room_type,
                    "category":category,
                    "live":room_live_status,
                    "room_code":room_code,      # to ensure room_code always unique added datetime.now
                    "listeners":[],
                    "sub_category":[],        # attributes from liverooms
                    "adminSocket":"",
                    "allowedUsers":[],
                    "otherUsers":[],
                    "screenShared":[],
                    "message":[]
                })
    
            else:
                listeners=[]
                for i in users:
                    listener=self.client.auth.profile.find_one({"_id":i})
                    listeners.append({
                        "id":i,
                        "name":listener["name"],
                        "channelName":listener["channel_name"],
                        "profilePicture":listener["profile_picture"]                     
                    })

                self.client.myspace.rooms.insert_one({
                    # "_id":profile+"_"+title+"_"+str(datetime.utcnow().timestamp()),
                    # let mongodb generate id 
                    "creator":creator,
                    "title":title,
                    "admin":listener["email"],  
                    "schedule":schedule,
                    "private":room_type,
                    "category":category,
                    "live":room_live_status,
                    "room_code":room_code,       # add time.time to ensure room_code always unique
                    "listeners":listeners,
                    "sub_category":[],        # attributes from liverooms
                    "adminSocket":"",
                    "allowedUsers":[],
                    "otherUsers":[],
                    "screenShared":[],
                    "message":[]
                })
            # return room code 
            return room_code

    def get(self, room_name):
        
        room_details=loads(dumps(self.client.myspace.rooms.find_one({"room_code":room_name})))
        if room_details:
            res = {
                "message":"Success",
                "data":{
                    "room":room_details
                },
                "status":True
            }

        else:
            res={
                "message":"Room Not Found",
                "status":False
            }

        return res

    def status(self, room_code, user_id):
        room=loads(dumps(self.client.myspace.rooms.find_one({"room_code":room_code})))

        if len(room["listeners"])==10:
            return "Room is full"

        if user_id in room["listeners"]:
            return "Listener already exist"

    def getCreator(self, room_code):
        return loads(dumps(self.client.myspace.rooms.find_one({"room_code":room_code})))["creator"]

    def storePending(self, room_code, user_id):
        print('storePending')
        listener=self.client.auth.profile.find_one({"_id":user_id})
        r=self.client.myspace.pending.find_one({"id":room_code})
        if r:
            print('r')
    
            for i in r["listeners_pending"]:
                if i["id"]==user_id:
                    return "User Already Exist in Pending List"

            self.client.myspace.pending.update({"id":room_code},
                {
                    "$push":{
                        "listeners_pending":{
                        "id":listener["_id"],
                        "name":listener["name"],
                        "channelName":listener["channel_name"],
                        "profilePicture":listener["profile_picture"]
                        }
                    }
                }
            )

        else:
            print('iserting')
            self.client.myspace.pending.insert_one({
                    "id":room_code,
                    "listeners_pending":[{
                        "id":listener["_id"],
                        "name":listener["name"],
                        "channelName":listener["channel_name"],
                        "profilePicture":listener["profile_picture"]
                    }]
                }
            )
        return "User added to pending list"
            
    def acceptPending(self, room_code, permitted):
        print('called accept pending')

        if not self.client.myspace.rooms.find_one({"room_code":room_code}):
            raise "Invalid Room Code"
        listeners=[]
        for i in permitted:
            listener=self.client.auth.profile.find_one({"_id":i})
            listeners.append({
                 "id": i,
                  "name":listener["name"],
                  "channelName":listener["channel_name"],
                  "profilePicture":listener["profile_picture"]
            })
        print('checking for status listenrs')
        for i in permitted:
            listener=self.client.auth.profile.find_one({"_id":i})
            
            self.client.myspace.pending.update_one({"id":room_code},
                {
                    "$pull":{
                        "listeners_pending":{
                         "id": i,
                        "name":listener["name"],
                        "channelName":listener["channel_name"],
                        "profilePicture":listener["profile_picture"]
                        }
                    }
                }
            )
        for listener in listeners:
            self.client.myspace.rooms.update_one({"room_code":room_code},
                {
                    "$push":{
                        "listeners":listener
                    }
                }
            )
        print('permission added')
        return "Permission Granted"


    def addPublic(self, room_name, user_id):
        listener=loads(dumps(self.client.auth.profile.find_one({"_id":user_id})))
        print(listener)
        if not listener:
            print('listners no found')
            return "Listner Not found"
        room=loads(dumps(self.client.myspace.rooms.find_one({"room_code":room_name})))
        if not room:
            print('not found room')
            return "Room not found"
        
        self.client.myspace.rooms.update_one({"room_code":room_name},
            {
                "$push":{
                    "listeners":{
                        "id":listener["_id"],
                        "name":listener["name"],
                        "channelName":listener["channel_name"],
                        "profilePicture":listener["profile_picture"]
                    }
                }
            }
        )
        print('listners added')
        return "Listener added"  


    def remove_listner(self,profile,room_name):
        listener=loads(dumps(self.client.auth.profile.find_one({"_id":profile})))
        if not listener:
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
            return res

        self.client.myspace.rooms.update_one({"room_code":room_name},
            {
                "$pull":{
                    "listeners":{
                         "id":listener["_id"],
                        "name":listener["name"],
                        "channelName":listener["channel_name"],
                        "profilePicture":listener["profile_picture"]
                    }
                }
            }
        )
        res={
            "message":"listner Removed from room",
            "status":True
        }
        return res

    def getlive_rooms(self):
        return loads(dumps(self.client.myspace.rooms.find( {"live":True} )))

    def start_room(self,room_name,sdpCandidate,sdpMLineIndex,sdpMid,serverUrl,type):
        room_details = loads(dumps(self.client.myspace.rooms.find_one({"room_code":room_name})))
        if room_details:
            self.client.myspace.rooms.update_one({"room_code":room_name} ,{"$set": { "live":True,"start_time":str(datetime.utcnow().timestamp()),
            "sdpCandidate":sdpCandidate, "sdpMLineIndex":sdpMLineIndex,"sdpMid":sdpMid, "serverUrl":serverUrl, "type":type}})
            res={
                "message":"Room ready to go live",
                "status":True
            }
        else:
            res={
                "message":"Room Not Found",
                "status":False
            }
        return res

    def delete(self,room_name):
        room_details = loads(dumps(self.client.myspace.rooms.find_one({"room_code":room_name})))
        if room_details:
            self.client.myspace.rooms.delete_one({"room_code":room_name})
            res={
                "message":"Room deleted",
                "status":True
            }
        else:
            res={
                "message":"Room Not Found",
                "status":False
            }
        return res

    def save_SDP(self,room_name,profile,sdpCandidate,sdpMLineIndex,sdpMid,serverUrl,type):
        user=self.client.auth.profile.find_one({"_id":profile})
        if not user:
            res={
                "message":"User Not Found",
                "status":True
            }

        room_details = loads(dumps(self.client.myspace.rooms.find_one({"room_code":room_name})))
        if room_details:
            self.client.myspace.rooms.update_one({"room_code":room_name},
            {
                "$pull":{
                    "listeners":{
                        "_id":profile
                    }
                }
            })
            self.client.myspace.rooms.update_one({"room_code":room_name},
            {
                "$push":{
                    "listeners":{
                        "_id":profile,
                        "name":user["name"],
                        "profilePicture":user["profile_picture"],
                        "channelName":user["channel_name"],
                         "sdpCandidate":sdpCandidate, 
                        "sdpMLineIndex":sdpMLineIndex,
                        "sdpMid":sdpMid, 
                        "serverUrl":serverUrl, 
                        "type":type,
                    }
                }
            })
            
            res={
                "message":"Credentials Saved",
                "status":True
            }
        else:
            res={
                "message":"Room Not Found",
                "status":False
            }
        return res

    def get_savedrooms(self,profile):
        return loads(dumps(self.client.myspace.savedrooms.find({"creator":{"_id":profile}})))


    def token(self, profile):
        print('token found is ',self.client.notifications.tokens.find_one({"profile":profile},{"token":True})["token"])
        return self.client.notifications.tokens.find_one({"profile":profile},{"token":True})["token"]

    def getPending(self, room_code, user_id):
        return loads(dumps(self.client.myspace.pending.find({"id":room_code})))

    def getChannelName(self, user_id):
        return self.client.auth.profile.find_one({"_id":user_id},{"channel_name":True})["channel_name"]

    def allRooms(self):
        return loads(dumps(self.client.myspace.rooms.find()))
    
    def prevRoomListners(self,user_id):
        """
        Get the listners of the previous room of the user
        """
        rooms = loads(dumps(self.client.myspace.rooms.find({"creator._id": user_id}).sort("schedule", -1).limit(1)))
        listners = []
        if len(rooms) > 0 and len(rooms[0]["listeners"]) > 0:
            for users in rooms[0]["listeners"]:
                user_profile = self.client.auth.profile.find_one({"_id": users["id"]})
                listners.append({
                    "id": user_profile["_id"],
                    "name": user_profile["name"],
                    "channelName": user_profile["channel_name"],
                    "profilePicture": user_profile["profile_picture"],
                    "follower": len(user_profile["follower"]),
                    "following": len(user_profile["following"]),
                    "area_of_expert": user_profile["area_of_expert"]
                })
            return listners

        return []
        
        
    def uploadThumbnail(self, room_code, file):

        try:
            self.client.myspace.rooms.update_one({"room_code":room_code},{"$set":{"thumbnail":file}})
            return True
        except:
            return False
    
    def close(self):
        self.client.close()
