from pymongo import MongoClient
from boto3 import client
from .local_settings import password, username, aws_access_key, aws_secret_access_key, aws_storage_bucket, aws_default_acl, apiKey
from pyfcm import FCMNotification
from datetime import datetime
'''
AWS CONNECTION
'''

AWS_STORAGE_BUCKET_NAME = aws_storage_bucket
AWS_DEFAULT_ACL = aws_default_acl
AWS_BASE_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/"

def s3Client():
    return client('s3',aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_access_key)


'''
DATABASE CONNECTION
'''

def clientOpen():   
    # return MongoClient(f"mongodb+srv://aiworld:i6TO1DZbtBzckOnx@mydb.xci1l.mongodb.net/mydb?retryWrites=true&w=majority")
    return MongoClient(f"mongodb+srv://myworld:myworld@Cluster0.g3hr1.mongodb.net/Cluster0?retryWrites=true&w=majority")
'''
FCM
'''

push_service = FCMNotification(api_key=apiKey)

def notify(token, body, event, id, profile_id, image):
    client=clientOpen()
    client.notifications.notification.update_one({"id":profile_id},
        {
            "$push":{
                "notification":{
                    "event":event,
                    "id":id,
                    "message":body,
                    "image":image,
                    "time":str(datetime.utcnow().timestamp())
                }
            }
        }
    )
    client.close()
    push_service.notify_single_device(registration_id=token, message_title="Rooms", message_body=body)

# connect for testing purpose
#def clientOpen():
#    return MongoClient(f"mongodb+srv://{username}:{password}@cluster0.jzv7p.mongodb.net/myworld?authSource=admin&replicaSet=atlas-39hn0j-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true")


"""
Groups
"""

class Groups:
    def __init__(self):
        self.groups = {}

    def group_add(self, group_name, websocket_endpoint):
        if group := self.groups.get(group_name):
            group.append(websocket_endpoint)
        else:
            self.groups.update({group_name: [websocket_endpoint, ]})

    def group_discard(self, group_name, websocket_endpoint):
        if group_name in self.groups:
            self.groups[group_name].remove(websocket_endpoint)

    async def group_send(self, group_name, data):
        if group := self.groups.get(group_name):
            for i in group:
                await i.broadcast(data=data)

group = Groups()