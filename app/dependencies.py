from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import email_validator as _email_check
from jose import jwt as _jwt

from app.core.config import settings
from app.models import users as _usermod, blogs as _blogmod
from app.schemas import users as _userschema, blogs as _blogschema
from app.database import get_db


"""
    These function will be used in the users
"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def verify_password(plain_password, hashed_password):
    # return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_all_users(db: Session):
    users = db.query(_usermod.User).all()
    return users


def get_user_by_id(id, db: Session):
    return db.query(_usermod.User).filter(_usermod.User.id == id).first()


def get_user_by_email(email: str, db: Session):
    return db.query(_usermod.User).filter(_usermod.User.email == email).first()


async def create_user(user, db: Session):
    # check if the email is valid
    try:
        valid = _email_check.validate_email(user.email)
        email = valid.email
    except _email_check.EmailNotValidError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please enter a valid email !")

    hashed_pwd = get_password_hash(user.password)
    new_user = _usermod.User(name=user.name, last_name=user.last_name, email=email, hashed_password=hashed_pwd)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Creating token
async def create_token(user: _usermod.User, expires_delta: timedelta | None = None):
    user_obj = _userschema.User.from_orm(user)

    user_dict = user_obj.dict()
    del user_dict["date_created"]

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    user_dict.update({"exp": expire})
    encoded_jwt = _jwt.encode(user_dict, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
    return dict(access_token=encoded_jwt, token_type='bearer')


# Authenticate user
def authenticate_user(email: str, password: str, db : Session):
    user = get_user_by_email(email=email, db=db)

    if not user:
        return False
    if not user.verify_password(password=password):
        return False
    return user


# Get current user
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    
    try:
        payload = _jwt.decode(token, settings.JWT_SECRET, settings.ALGORITHM)
        user = db.query(_usermod.User).get(payload["id"])
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password or email !")
    return _userschema.User.from_orm(user)


# Delete a user
def delete_user(id, db: Session):

    user_to_delete = db.query(_usermod.User).filter(_usermod.User.id == id)

    if not user_to_delete.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"User with {id} id not found")
    else:
        user_to_delete.delete()
        db.commit()

    return 'User deleted successfully !'


def update_user(id, request: _userschema.UserCreate, db: Session):

    user_to_update = db.query(_usermod.User).filter(_usermod.User.id == id)

    if not user_to_update.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"User with {id} id not found")
    else:
        user_to_update.update(request)
        db.commit()
        db.refresh(user_to_update)

    return user_to_update

"""
    These functions will be used in the blogs
"""


def get_all_blogs(db: Session):
    blogs = db.query(_blogmod.Blog).all()
    return blogs


def create_blog(blog: _blogschema.BlogBase, db: Session):
    new_blog = _blogmod.Blog(title=blog.title, body=blog.body)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


def get_blog(id, db: Session):
    blog = db.query(_blogmod.Blog).filter(_blogmod.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="blog not found")

    return blog


def delete_blog(id, db: Session):

    blog_to_delete = db.query(_blogmod.Blog).filter(_blogmod.Blog.id == id)

    if not blog_to_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="blog not found")
    else:
        blog_to_delete.delete(synchronize_session=False)

        db.commit()

    return 'blog deleted successfully'


def update_blog(id, request: _blogschema.BlogBase,db: Session):

    blog_to_update = db.query(_blogmod.Blog).filter(_blogmod.Blog.id == id)

    if not blog_to_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="blog not found")
    else:
        blog_to_update.update(request)
        db.commit()

    return blog_to_update
