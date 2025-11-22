from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/css", StaticFiles(directory="views/css"), name="css")
app.mount("/js", StaticFiles(directory="views/js"), name="js")
app.mount("/style", StaticFiles(directory="views/style"), name="style")
app.mount("/images", StaticFiles(directory="views/images"), name="images")
app.mount("/webfonts", StaticFiles(directory="views/webfonts"), name="webfonts")
templates = Jinja2Templates(directory="views")

@app.get("/")
async def read_root(request: Request): 
    """
    Renders the main web.html page.
    """
    return templates.TemplateResponse(
        "Web.html", 
        {
            "request": request
        }
    )

@app.get("/Register")
async def read_registration(request: Request): 
    """
    Renders the RegistrationForm.html page.
    """
    return templates.TemplateResponse(
        "RegistrationForm.html", 
        {
            "request": request
        }
    )