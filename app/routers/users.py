from datetime import timedelta
from fastapi import APIRouter, status, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database import get_db
from app import dependencies as crud
from app.schemas import users as schemas


router = APIRouter(prefix="/users", tags=['Users'])
auth = APIRouter(prefix="", tags=['Users'])


# Login == generate token
@auth.post("/login")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(email=form_data.username, password=form_data.password, db=db)
    if not user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials !")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await crud.create_token(user=user, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


# Create user
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(email=user.email, db=db)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with that email already exist !")
    # creating user
    new_user = await crud.create_user(user=user, db=db)
    # return token
    return await crud.create_token(user=new_user)


# Get all users
@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is not any registered user")
    return users


# Get current user
@router.get("/me", status_code=status.HTTP_200_OK, response_model=schemas.User)
def get_me(user: schemas.User = Depends(crud.get_current_user)):
    return user


# Get user by id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.User)
def get_user(id, db: Session = Depends(get_db)):
    return crud.get_user_by_id(id, db)


# Delete user by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id, db: Session = Depends(get_db)):
    return crud.delete_user(id, db)


# Update user
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.User)
def update_user(id, user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.update_user(id, user, db)
