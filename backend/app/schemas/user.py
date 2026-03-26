from pydantic import BaseModel, Field, ConfigDict

class UserCreate(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=6, max_length=100)
    password: str = Field(min_length=6, max_length=100)
    role: str = Field(min_length=3, max_length=100)

class UserRead(BaseModel):
    id: int = Field(gt=0)
    name: str
    email: str
    role: str

    #dictionary to json
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: str = Field(min_length=6, max_length=100)
    password: str = Field(min_length=6, max_length=100)

class UserRegister(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=6, max_length=100)
    password: str = Field(min_length=6, max_length=100)