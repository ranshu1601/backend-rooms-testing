import socketio
import time
sio = socketio.Client()
sio.connect("http://3.110.83.207:5000")
time.sleep(3)

@sio.on("get room clients response")
def xyz(data):
    print(data)

@sio.on("all response")
def xyz1(data):
    print(data)

sio.emit("create or join",{"room":"test-room"})
time.sleep(3)
sio.emit("set room sdp",{"sid":"sid","type":"type","label":"label","candidate":"candidate","id":"id","from":"xfrom","to":"to"})
time.sleep(5)
sio.emit("get room sdp")
time.sleep(5)
sio.emit("all")
time.sleep(5)
sio.disconnect()