from pydantic import BaseModel, Field, ConfigDict, model_validator, EmailStr

from backend.app.core.exceptions import NotMatchedPasswords


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=6, max_length=100)
    password: str = Field(min_length=8, max_length=100)
    role: str = Field(min_length=3, max_length=100)

class UserRead(BaseModel):
    id: int = Field(gt=0)
    name: str
    email: str
    role: str
    is_active: bool = True

    #dictionary to JSON
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: str = Field(min_length=6, max_length=100, description="Email of the user")
    password: str = Field(min_length=8, max_length=100, description="Password of the user")

class UserRegister(BaseModel):
    name: str = Field(min_length=3, max_length=100, description="Name of the user")
    email: EmailStr
    password: str = Field(min_length=8, max_length=100, description="Password of the user")

class UserEdit(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=100)
    email: EmailStr | None = Field(default=None, min_length=6, max_length=100)
    password: str | None = Field(default=None, min_length=8, max_length=100)

class UserEditAdmin(UserEdit):
    is_active: bool | None = Field(default=None)
    role: str | None = Field(default=None, min_length=3, max_length=100)

class UserChangePassword(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=100)
    confirm_password: str = Field(min_length=8, max_length=100)

    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.new_password != self.confirm_password:
            raise NotMatchedPasswords
        return self