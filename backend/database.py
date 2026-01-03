# db.py
import os
from pymongo import MongoClient
from passlib.hash import bcrypt

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "my_project")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

users_collection = db.users
prompts_collection = db.prompts
feedback_collection = db.feedback


def hash_password(password: str) -> str:
    # محدود کردن طول به 72 بایت برای ایمنی
    password = password.encode('utf-8')[:72].decode('utf-8', 'ignore')
    return bcrypt.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    password = password.encode('utf-8')[:72].decode('utf-8', 'ignore')
    return bcrypt.verify(password, hashed)
