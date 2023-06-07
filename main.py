from starlette.applications import Starlette
from server.urls import urlpatterns
import uvicorn
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

middleware=[
        Middleware(CORSMiddleware,allow_origins=["*"],allow_headers=["*"],allow_methods=["*"],)
]

app = Starlette(routes=urlpatterns, middleware=middleware)

if __name__ == "__main__":
        print(f'Starting server at port 8000')
        uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", debug=True)
