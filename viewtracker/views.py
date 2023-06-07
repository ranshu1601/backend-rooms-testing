from starlette.responses import JSONResponse
from .models import ViewTracker

async def getViews(request):
    try:
        room_code = request.path_params["room_code"]
        views = ViewTracker()
        data = views.get(room_code)
        views.close()

        return JSONResponse({"message":"Success", "data":data, "status":True})

    except Exception as e:
        return JSONResponse({"message":str(e),"status":False},status_code=400)

