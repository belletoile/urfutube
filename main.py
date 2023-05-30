import fastapi
import uvicorn
from fastapi.security import OAuth2PasswordBearer

from starlette.staticfiles import StaticFiles

from video.router import router as router_video
from user.router import router as router_user
from pages.router import router as router_pages

app = fastapi.FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(router_video)
app.include_router(router_user)
app.include_router(router_pages)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
