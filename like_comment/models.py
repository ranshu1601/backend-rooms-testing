from server.settings import clientOpen
from datetime import datetime
from bson.json_util import loads, dumps


class Like:
    def __init__(self):
        self.client = clientOpen()

    """def create_or_delete(self,profile_id,user_id,room_code):
        if c:=self.client.users.likes.find_one({"room_code":room_code, "user_id":user_id}):
            #Delete Like
            if profile_id in c["users"]:
                self.client.users.likes.update(
                    {"room_code": room_code, "user_id":user_id},
                    {
                        "$pull":{"users":profile_id}
                    }
                )
                return "Like Deleted Successfully"

            # Add New Like to Existing

            self.client.users.likes.update({"room_code":room_code, "user_id":user_id},
                {
                    "$push":{"users":profile_id}
                }
            )
            
        else:
            self.client.users.likes.insert_one({
                "_id": profile_id+"_"+str(datetime.utcnow().timestamp()),
                #"profile_id": profile_id, 
                "user_id": user_id, 
                "room_code": room_code,
                "users":[profile_id]
            })

        return "Liked Successfully" """

    def create_or_delete(self,user_id,room_code):
        if c:=self.client.myspace.likes.find_one({"room_code":room_code, "user_id":user_id}):

            self.client.myspace.likes.delete_many({"room_code":room_code, "user_id": user_id})
            return "Liked Deleted Successfully"

        else:
            self.client.myspace.likes.insert_one({ 
                "_id": user_id+"_"+str(datetime.utcnow().timestamp()),
                "user_id": user_id,
                "room_code": room_code,
            })

        return "Liked Successfully" 

    def checkUserLikes(self, user_id):
        res = []
        res = loads(dumps(self.client.myspace.likes.find({"user_id":user_id})))
        return res
    

    def close(self):
         self.client.close()   


class Comment:
    def __init__(self):
        self.client = clientOpen()

    def create(self, profile_id, room_code, comment):
        profile = loads(dumps(self.client.auth.profile.find_one({"_id":profile_id})))

        if self.client.rooms.comments.find_one({"room_code":room_code}):

            # Add New Comment to Existing Comment
            self.client.rooms.comments.update_one({"room_code":room_code},
                {
                    "$push":{
                        "comments":{
                            "comment_id":profile_id+"_"+str(datetime.utcnow().timestamp()),
                            "profile_id":profile_id,
                            "channel_name":profile["channel_name"],
                            "profile_picture":profile["profile_picture"],
                            "comment":comment,
                        }
                    }
                }
            )

        else:
            #Add New Comment
            self.client.rooms.comments.insert_one({
                "_id":room_code+"_"+str(datetime.utcnow().timestamp()),
                "room_code":room_code,
                "comments":[
                    {
                        "comment_id":profile_id+"_"+str(datetime.utcnow().timestamp()), 
                        "profile_id":profile_id, 
                        "channel_name":profile["channel_name"], 
                        "profile_picture":profile["profile_picture"], 
                        "comment":comment, 
                    }
                ]
            })

        return "Commented Successfully"

    def delete(self, room_comment_id, comment_id):
        print(room_comment_id, comment_id)
        if c:=self.client.rooms.comments.find_one({"_id":room_comment_id}):
            self.client.rooms.comments.update_one({"_id":room_comment_id},
                {
                    "$pull":{
                        "comments":{"comment_id":comment_id}
                    }
                }
            )
            return "Comment Deleted Successfully"
        return "Comment Does not Exist"

    def getComment(self, id):
        return loads(dumps(self.client.rooms.comments.find_one({"room_code":id})))

    def close(self):
        self.client.close()


class LikeCommentView:

    def __init__(self):
        self.client = clientOpen()

    def get(self, room_code):
        res = dict()
        res["room_code"]=room_code

        res["comments"]=loads(dumps(self.client.rooms.comments.find_one({"room_code":room_code})))

        res["views"]=loads(dumps(self.client.rooms.views.find_one({"_id":{"$regex":room_code}})))

        
        viewers = loads(dumps(self.client.rooms.viewtracker.find({"room_code":room_code},{"profile"}))) 
        res["viewers"]=[]

        for i in viewers:
            res["viewers"].append(i)


    
        res["users_likes"] = loads(dumps(self.client.myspace.likes.find({"room_code":room_code},{"user_id", "users"})))     
        


        return res

    def close(self):
        self.client.close()

