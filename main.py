from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

app.mount("/css", StaticFiles(directory="views/css"), name="css")
app.mount("/js", StaticFiles(directory="views/js"), name="js")
app.mount("/test", StaticFiles(directory="views/test"), name="test")
app.mount("/images", StaticFiles(directory="views/images"), name="images")
app.mount("/webfonts", StaticFiles(directory="views/webfonts"), name="webfonts")

@app.get("/")
async def read_root():
    return FileResponse("views/Web.html")

@app.get("/Register")
async def read_registration():
    return FileResponse("views/RegistrationForm.html")



