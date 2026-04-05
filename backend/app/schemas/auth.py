from pydantic import BaseModel

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: str
    email: str | None = None
    role: str | None = None
    type: str = "access"

class RefreshTokenData(BaseModel):
    sub: str
    email: str | None = None
    role: str | None = None
    type: str = "refresh"

class RefreshRequest(BaseModel):
    refresh_token: str

class LogOutRequest(BaseModel):
    refresh_token: str
