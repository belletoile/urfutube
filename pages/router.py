from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from user.router import profile, login
from video.router import get_video_id, get_video, get_my_video

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@router.get("/profile")
def get_search_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})


@router.get("/main_page")
def get_user(request: Request, operations=Depends(get_video)):
    return templates.TemplateResponse("main_page.html", {"request": request, "operations": operations})


@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})


@router.get("/login/signup")
def login(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@router.get("/upload_video")
def upload(request: Request):
    return templates.TemplateResponse("upload_video.html", {"request": request})


@router.get("/video/{id}")
def get_video_id(request: Request, operations=Depends(get_video_id)):
    return templates.TemplateResponse("video.html",  {"request": request, "operations": operations})
