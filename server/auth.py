from starlette.responses import JSONResponse
from datetime import datetime
from .local_settings import JWT_SECRET_KEY
import jwt
import functools

async def verify_access_token(token):
    present_time = datetime.utcnow()
    print(present_time)
    try:
        payload = jwt.decode(token, algorithms=["HS256"], key=JWT_SECRET_KEY)

        if payload.get("typ") != "access":
            raise jwt.exceptions.InvalidKeyError("Refresh token sent")

        if present_time.timestamp() > payload.get("exp"):
            raise jwt.exceptions.ExpiredSignatureError("Token Invalid or Expired")

        return True, payload.get('id')

    except Exception as e:
        raise e


def jwt_authentication(endpoint, *args, **kwargs):

    @functools.wraps(endpoint)
    async def inner(request, **kwargs):

        try:
            token = request.headers['authorization'].split(" ")[1]

            res, user_id = await verify_access_token(token)
            
        except Exception as e:
            return JSONResponse(content={
                "message": str(e),
                "status": False
            }, status_code=401)

        if res:
            request.user_id = user_id
            return await endpoint(request, **kwargs)

    return inner

async def jwt_authentication_socket(token):
    try:
        res, user_id = await verify_access_token(token)

        return res, user_id

    except Exception as e:

        return False, None
