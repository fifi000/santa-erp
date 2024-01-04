from datetime import datetime, timedelta
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm

from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session

from db.config import get_session
from db.auth import UserDB

from api.auth.models import Token, User
from api.auth.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES, 
    authenticate_user, 
    get_password_hash,
    create_access_token, 
    get_current_active_user, 
    get_user
)


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/token', response_model=Token)
async def login_for_access_token(
    *,
    session: Annotated[Session, Depends(get_session)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/register')
async def register(
    *,
    session: Annotated[Session, Depends(get_session)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    if get_user(session, form_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User already exists'
        )
    user = User(
        username=form_data.username,
        hashed_password=get_password_hash(form_data.password)
    )
    session.add(UserDB(**user.model_dump()))
    session.commit()

    return {'ok', True}


@router.get('/users/me/', response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@router.get('/time')
async def get_time(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return {'time': datetime.now()}
