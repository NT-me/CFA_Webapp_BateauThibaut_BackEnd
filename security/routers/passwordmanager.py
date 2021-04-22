from datetime import datetime, timedelta
from typing import Optional
import utils as u
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from security.data.models import User as dbUser

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = u.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class newUser(BaseModel):
    username: str
    full_name: str
    password: str


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    active: Optional[bool] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="pswd/token")

ADRESS_CANVA = u.ADRESS_CANVA
router = APIRouter(
            prefix="/pswd",
            tags=["password"]
            )

db_string = u.DB_SEC_PATH
engine = create_engine(db_string, connect_args={'check_same_thread': False})
Session = sessionmaker(engine)
session = Session()


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    user = session.query(dbUser).filter(dbUser.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.query(dbUser).filter(dbUser.username == username).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: dbUser = Depends(get_current_user)):
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return User(username=current_user.username,
    email=current_user.email,
    full_name=current_user.full_name,
    active=current_user.active)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/users/test/", response_model=dict)
async def test_if_user_is_connected(current_user: User = Depends(get_current_active_user)):
    return {"detail": True}


@router.post("/new")
async def create_new_user(newuser: newUser):
    resDB = session.query(dbUser).filter(dbUser.username == newuser.username)
    resDB = resDB.all()

    if len(resDB) == 0:
        nU = dbUser(username=newuser.username, full_name=newuser.full_name, hashed_password=pwd_context.hash(newuser.password), active=True)
        session.add(nU)
        session.commit()
        return({"status":"Success, user created"})
    else:
        raise HTTPException(status_code=400, detail="User aldready exist")
