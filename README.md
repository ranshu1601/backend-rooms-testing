
# Backend Rooms - 

## Base URL - http://rooms.joinmyworld.in/
## Instance Name - Backend_Rooms
## Live Branch Name - testing
## Database used - myspace
## Postman Collection - Rooms

**Note-Updated database.Previously it was liverooms. Now we are using myspace database for socket and room.**

**Note - Users should be authenticated for performing following operations.
Details documents present in main Branch**


| Request Type/Path |Body | Response |
| :---         |     :---:      |          :---: | 
| Create Room | {"title":string,"category":array of string,|room_code
|Path - /create_room/|"schedule":time(ex -123855667896512),"private":boolean,|-
|Method POST |users":Array of allowed users} |-
|-|If room is private then pass users arrays containing allowed|-
|-| users id’sIf room is public no need to pass users|-
|-----------------------------|-------------------------------|---------------------------------|
|Get room details  | Path param - room_code | detailed room description |
Path -  /get_room/ | - | -
Method: GET |- | -
|-----------------------------|-------------------------------|---------------------------------|
|Add New Listner  | {  “room_code”:”suraj-code”} | listner added details |
Path -  /add/ | - | -
Method: POST |- | -
|-----------------------------|-------------------------------|---------------------------------|
|Add Public Listner | Path param - room_code | listner added details |
Path -  /addPublic/ | - | -
Method: GET |- | -
|-----------------------------|-------------------------------|---------------------------------|
|Accept pending request | {"room_code":string,"listners":array of user id} | - |
Path -  /accept/ | - | -
Method: POST |- | -
|-----------------------------|-------------------------------|---------------------------------|
|Get pending user list | Path param - room_code| list of users pending |
Path -  /list/ | - | -
Method: GET |- | -
|-----------------------------|-------------------------------|---------------------------------|
|Remove listner | Path param - room_code| - |
Path -  /remove_listner/ | - | -
Method: GET |- | -
|-----------------------------|-------------------------------|---------------------------------|
|Get live rooms | - | list of live rooms
Path -  /live_rooms/ | - | -
Method: GET |- | -
|-----------------------------|-------------------------------|---------------------------------|
|Delete room | - | deleted message
Path -  /delete_rooms/ | - | -
Method: GET |- | -
|-----------------------------|-------------------------------|---------------------------------|
|Get room timeline | - | deleted message
Path -  /room_timeline/ | - | -
Method: GET |- | -
|-----------------------------|-------------------------------|---------------------------------|
|Get all rooms | - | list of all rooms 
Path -  /all_rooms/ | - | -
Method: GET |- | -




