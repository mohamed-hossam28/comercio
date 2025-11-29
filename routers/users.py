from fastapi import APIRouter,Depends,status,Form
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


@users_router.post("/login")
async def login_user(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(database.get_db)
):
    user = db.query(User).filter(User.email == email, User.password == password).first()
    if user:
        return {"user_name": user.first_name}
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Invalid email or password"}
        )

