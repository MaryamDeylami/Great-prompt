# models.py (نسخه حرفه‌ای و کامل)
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict
from datetime import datetime

# -------------------
# Users
# -------------------
class User(BaseModel):
    email: EmailStr
    password: str
    role: str = "individual"        # individual / team / admin
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None


class UserOut(BaseModel):
    email: EmailStr
    role: str


class LoginData(BaseModel):
    email: EmailStr
    password: str


# -------------------
# Prompts
# -------------------
class PromptVersion(BaseModel):
    version: int
    content: str
    created_at: datetime


class Prompt(BaseModel):
    text: str
    user_email: EmailStr
    category: Optional[str] = None
    tags: Optional[List[str]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    versions: Optional[List[PromptVersion]] = []


# -------------------
# Feedback
# -------------------
class Feedback(BaseModel):
    prompt_id: str
    user_email: EmailStr
    feedback: str
    rating: Optional[int] = None  # برای امتیازدهی
    created_at: Optional[datetime] = None


# -------------------
# جستجو و فیلتر (Optional برای API)
# -------------------
class PromptFilter(BaseModel):
    owner_email: Optional[EmailStr] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = []
    skip: int = 0
    limit: int = 20
