from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from jose import jwt, JWTError
from passlib.context import CryptContext

from backend.app.core.config import settings
from backend.app.core.exceptions import PasswordVerifyError
from backend.app.schemas.auth import RefreshTokenData, TokenData

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        raise PasswordVerifyError
def create_access_token(data: TokenData, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)))
    to_encode = {"sub": data.sub, "email": data.email, "role": data.role, "type": data.type, "exp": expire,}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, [settings.ALGORITHM])
    except JWTError:
        return {}

def create_refresh_token(data: RefreshTokenData) -> tuple[str, datetime]:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    payload = {"sub": data.sub, "email": data.email, "role": data.role, "type": data.type, "exp": expire,}

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token, expire

def decode_refresh_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, [settings.ALGORITHM])
    except JWTError:
        return {}


