from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from . import crud, models, schemas, security, dependencies
from .database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(dependencies.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(dependencies.get_current_user)):
    return current_user

@app.get("/admin/dashboard")
def admin_dashboard(current_user: models.User = Depends(dependencies.role_checker([models.Role.admin]))):
    return {"message": f"Welcome to the admin dashboard, {current_user.username}!"}

@app.get("/distributor/dashboard")
def distributor_dashboard(current_user: models.User = Depends(dependencies.role_checker([models.Role.distributor]))):
    return {"message": f"Welcome to the distributor dashboard, {current_user.username}!"}

@app.get("/supplier/dashboard")
def supplier_dashboard(current_user: models.User = Depends(dependencies.role_checker([models.Role.supplier]))):
    return {"message": f"Welcome to the supplier dashboard, {current_user.username}!"}
