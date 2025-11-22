from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()


app.mount("/views", StaticFiles(directory="views"), name="views")

@app.get("/", response_class=HTMLResponse)
def home():
    with open("views/Web.html", "r", encoding="utf-8") as f:
        return f.read()