from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import database
from routers import users, order
import time

app = FastAPI()


app.mount("/css", StaticFiles(directory="views/css"), name="css")
app.mount("/js", StaticFiles(directory="views/js"), name="js")
app.mount("/style", StaticFiles(directory="views/style"), name="style")
app.mount("/images", StaticFiles(directory="views/images"), name="images")
app.mount("/webfonts", StaticFiles(directory="views/webfonts"), name="webfonts")

@app.on_event("startup")
def on_startup():
    database.init_db()

templates = Jinja2Templates(directory="views")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("Web.html", {"request": request, "timestamp": int(time.time())})

@app.get("/Register")
async def read_registration(request: Request):
    return templates.TemplateResponse("RegistrationForm.html", {"request": request})


app.include_router(users.users_router)
app.include_router(order.order_router)
