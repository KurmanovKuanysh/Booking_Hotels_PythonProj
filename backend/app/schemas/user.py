from pydantic import BaseModel, Field

class UserBase(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=6, max_length=100)
    password: str = Field(min_length=6, max_length=100)
    role: str = Field(min_length=3, max_length=100)

class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=6, max_length=100)
    password: str = Field(min_length=6, max_length=100)
    role: str = Field(min_length=3, max_length=100)

class UserRead(UserBase):
    id: int = Field(gt=0)

class UserLogin(BaseModel):
    email: str = Field(min_length=6, max_length=100)
    password: str = Field(min_length=6, max_length=100)

class UserRegister(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=6, max_length=100)
    password: str = Field(min_length=6, max_length=100)