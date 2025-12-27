from pydantic import BaseModel, field_validator
from pydantic import BaseModel


# # Pydantic models for signup
# class UserSignup(BaseModel):
#     email: str
#     password: str

# Pydantic models for login
class UserLogin(BaseModel):
    email: str
    password: str

# Pydantic models for signup
class UserSignup(BaseModel):
    """
    Schema for user signup requests, ensuring basic email format and strong password criteria.
    """
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def strong_password(cls, password):
        """
        Validates that the password meets minimum security requirements:
        at least 8 characters, one uppercase, one lowercase, one digit, and one special character.
        """
        if len(password) < 8:
            raise ValueError("Password kam az kam 8 characters ka ho")

        if not re.search(r"[A-Z]", password):
            raise ValueError("Password mein 1 uppercase zaroori hai")

        if not re.search(r"[a-z]", password):
            raise ValueError("Password mein 1 lowercase zaroori hai")

        if not re.search(r"\d", password):
            raise ValueError("Password mein 1 number zaroori hai")

        if not re.search(r"[!@#$%^&*]", password):
            raise ValueError("Password mein 1 special character zaroori hai")

        return password
