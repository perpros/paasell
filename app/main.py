from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models, crud, schemas
from .database import engine, get_db
from .routers import auth as auth_router
from .dependencies import get_current_active_user

# Create all database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the authentication router
app.include_router(auth_router.router)

@app.on_event("startup")
def create_initial_roles():
    """Create initial roles if they don't exist on startup."""
    db = next(get_db())
    roles = ["Admin", "Support", "Supplier"]
    for role_name in roles:
        if not crud.get_role_by_name(db, name=role_name):
            crud.create_role(db, role_name=role_name, description=f"{role_name} role")
    db.close()


@app.get("/")
def read_root():
    return {"message": "Welcome to the B2B2C Wholesale Platform API"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user
