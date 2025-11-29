from fastapi import APIRouter, Depends, status, Form, Request
from fastapi.responses import JSONResponse
from models.users import User
import database
from sqlalchemy.orm import Session
import auth

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
    response = JSONResponse(content={"user_id": user.id, "user_name": user.first_name})
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@users_router.post("/logout")
def logout(request: Request):
    token = request.cookies.get("session_token")
    if token:
        auth.invalidate_session(token)
    resp = JSONResponse(content={"message": "Logged out"})
    resp.delete_cookie("session_token")
    return resp

