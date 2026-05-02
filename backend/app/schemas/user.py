import re

from pydantic import BaseModel, Field, ConfigDict, model_validator, EmailStr, model_validator

from backend.app.models.user import UserRole
from backend.app.core.exceptions import NotMatchedPasswords, PasswordValidationError


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=6, max_length=100)
    password: str = Field(min_length=8, max_length=100)
    role: UserRole = UserRole.USER

class UserRead(BaseModel):
    id: int = Field(gt=0)
    name: str
    email: str
    role: UserRole
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

    @model_validator(mode='after')
    def password_check(self):
        spec_symbols = re.search(r'[!@#$%^&*(),.?":{}|<>]', self.password)
        upper_case = re.search(r'[A-Z]', self.password)
        if not upper_case and spec_symbols:
            raise PasswordValidationError("Password must contain at least one uppercase letter and one special symbol.")
        return self


class UserEdit(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=100)
    email: EmailStr | None = Field(default=None, min_length=6, max_length=100)
    password: str | None = Field(default=None, min_length=8, max_length=100)

class UserEditAdmin(UserEdit):
    is_active: bool | None = Field(default=None)
    role: UserRole

class UserChangePassword(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=100)
    confirm_password: str = Field(min_length=8, max_length=100)

    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.new_password != self.confirm_password:
            raise NotMatchedPasswords
        return self

    @model_validator(mode='after')
    def password_check(self):
        spec_symbols = re.search(r'[!@#$%^&*(),.?":{}|<>]', self.new_password)
        upper_case = re.search(r'[A-Z]', self.new_password)
        if not upper_case and spec_symbols:
            raise PasswordValidationError("Password must contain at least one uppercase letter and one special symbol.")
        return self
