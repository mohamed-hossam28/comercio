from fastapi import APIRouter, Depends, status, Form, Request
from fastapi.responses import JSONResponse
from models.users import User
import database
from sqlalchemy.orm import Session
import auth
from controller import hash_password, verify_password
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
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"success": False, "message": "This email is already registered."}
        )
    hashed_password = hash_password(password)
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        dob=dob,
        email=email,
        password=hashed_password,
        sex=sex,
        phone=phone,
        country=country
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"success": True, "message": "Registration successful"}


@users_router.post("/login")
async def login_user(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(database.get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if user and verify_password(password, user.password):
        # create a session token and set it in an HTTP-only cookie
        token = auth.create_session(user.id)
        resp = JSONResponse(content={"user_name": user.first_name, "user_id": user.id})
        resp.set_cookie(key="session_token", value=token, httponly=True, samesite="lax")
        return resp
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Invalid email or password"}
        )


@users_router.get("/me")
def get_me(request: Request, db: Session = Depends(database.get_db)):
    token = request.cookies.get("session_token")
    user_id = auth.get_user_id_from_token(token)
    if not user_id:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Not authenticated"})
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Invalid session"})
    
    user_data = {
        "user_id": user.id,
        "user_name": user.first_name,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": user.phone,
        "country": user.country,
        "dob": user.dob,
        "sex": user.sex
    }
    
    response = JSONResponse(content=user_data)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@users_router.put("/update-profile")
async def update_profile(
    request: Request,
    first_name: str = Form(None),
    last_name: str = Form(None),
    phone: str = Form(None),
    country: str = Form(None),
    password: str = Form(None),
    dob: str = Form(None),
    sex: str = Form(None),
    db: Session = Depends(database.get_db)
):
    token = request.cookies.get("session_token")
    user_id = auth.get_user_id_from_token(token)
    
    if not user_id:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Not authenticated"})
        
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found"})

    if first_name: user.first_name = first_name
    if last_name: user.last_name = last_name
    if phone: user.phone = phone
    if country: user.country = country
    if password: user.password = password
    if dob: user.dob = dob
    if sex: user.sex = sex

    db.commit()
    db.refresh(user)
    
    return {"message": "Profile updated successfully!", "user_name": user.first_name}


@users_router.post("/logout")
def logout(request: Request):
    token = request.cookies.get("session_token")
    if token:
        auth.invalidate_session(token)
    resp = JSONResponse(content={"message": "Logged out"})
    resp.delete_cookie("session_token")
    return resp

