import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ADMIN_USERNAME = os.getenv("JWT_ADMIN_USERNAME")
ADMIN_PASSWORD_HASH = os.getenv("JWT_ADMIN_PASSWORD_HASH")

if not SECRET_KEY or not ADMIN_USERNAME or not ADMIN_PASSWORD_HASH:
    raise RuntimeError("SECRET_KET, ADMIN_USERNAME and ADMIN_PASSWORD_HASH must be configured in .env")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # pulls out bearer token from the HTTP header

def authenticate_admin(username:str, password:str) -> bool:
    if username != ADMIN_USERNAME:
        return False
    return password_hash.verify(password, ADMIN_PASSWORD_HASH)

def create_access_token(username:str)->str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub":username, "exp":expires_at}

    return jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM) #encoding the payload using the secret-key and the algorithm


def get_current_user(token:str = Depends(oauth2_scheme))->str:
    credentials_exception = HTTPException(
                                status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Invalid or expired authentication token",
                                headers={"WWW-Authenticate":"Bearer"}
                                )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username != ADMIN_USERNAME:
            raise credentials_exception
        return username
    except InvalidTokenError:
        raise credentials_exception
