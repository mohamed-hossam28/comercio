from fastapi import APIRouter,Depends,status,Request,Form
from fastapi.responses import JSONResponse
from models.users import User
import database
from sqlalchemy.orm import Session

users_router = APIRouter()

@users_router.post("/register-user")
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