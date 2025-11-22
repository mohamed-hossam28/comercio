from fastapi import FastAPI, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import database

app = FastAPI()

# --- static files ---
app.mount("/css", StaticFiles(directory="views/css"), name="css")
app.mount("/js", StaticFiles(directory="views/js"), name="js")
app.mount("/style", StaticFiles(directory="views/style"), name="style")
app.mount("/images", StaticFiles(directory="views/images"), name="images")
app.mount("/webfonts", StaticFiles(directory="views/webfonts"), name="webfonts")

# --- DB init ---
@app.on_event("startup")
def on_startup():
    database.init_db()


@app.get("/")
async def read_root():
    return FileResponse("views/Web.html")


@app.get("/Register")
async def read_registration():
    return FileResponse("views/RegistrationForm.html")


# -------------------------------
# ⭐ POST: Receive Registration Data
# -------------------------------
@app.post("/register-user")
async def register_user(
    first_name: str = Form(...),
    last_name: str = Form(...),
    dob: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    sex: str = Form(...),
    phone: str = Form(...),
    country: str = Form(...),
    db: Session = Depends(database.get_db)
):
    # Insert into DB
    from models.users import User

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        dob=dob,
        email=email,
        password=password,
        sex=sex,
        phone=phone,
        country=country
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Registration successful!", "user_id": new_user.id}
