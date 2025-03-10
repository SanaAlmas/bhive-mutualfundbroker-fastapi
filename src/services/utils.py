import jwt
import uuid
import logging
from datetime import datetime, timedelta
from config import config_obj
from passlib.context import CryptContext

ACCESS_TOKEN_EXPIRY = 3600

password_context = CryptContext(
    schemes=['bcrypt']
)

def generate_password_hash(password: str) -> str:
    password_hash = password_context.hash(password)
    return password_hash

def verify_password_hash(password: str, password_hash: str) -> bool:
    return password_context.verify(password, password_hash)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {
        'user': user_data,
        'exp': datetime.now() + (expiry if expiry else timedelta(seconds=ACCESS_TOKEN_EXPIRY)),
        'jti': str(uuid.uuid4()),
        'refresh': refresh
    }

    token = jwt.encode(
        payload=payload,
        key=config_obj.JWT_SECRET_KEY,
        algorithm=config_obj.JWT_ALGORITHM
    )
    return token

def decode_access_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=config_obj.JWT_SECRET_KEY,
            algorithms=[config_obj.JWT_ALGORITHM]
        )

        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None