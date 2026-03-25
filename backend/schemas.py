from pydantic import BaseModel, Field, validator
from typing import List


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2)
    phone: str = Field(..., min_length=8, max_length=15)
    password: str = Field(..., min_length=4)
    persona: str
    interests: List[str]

    @validator("interests", pre=True)
    def clean_interests(cls, v):
        return [i.strip().lower() for i in v]


class UserLogin(BaseModel):
    phone: str
    password: str


class UserResponse(BaseModel):
    user_id: int