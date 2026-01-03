# crud.py (نسخه اصلاح شده)
from datetime import datetime
from typing import List, Optional
from pymongo import ASCENDING
from .database import users_collection, prompts_collection, feedback_collection, hash_password, verify_password
from .models import User, Prompt, Feedback

# -------------------
# Users
# -------------------

def create_user(user: User):
    try:
        user_dict = user.dict()
        user_dict["password"] = hash_password(user.password)
        users_collection.insert_one(user_dict)
        return user_dict
    except Exception as e:
        print("Error in create_user:", e)
        raise e


def authenticate_user(email: str, password: str):
    user = users_collection.find_one({"email": email})
    if not user or not verify_password(password, user['password']):
        return None
    user.pop("password")
    return user


def get_user(email: str):
    return users_collection.find_one({"email": email}, {"password": 0})


# -------------------
# Prompts
# -------------------

def create_prompt(prompt: Prompt):
    now = datetime.utcnow()
    prompt_dict = prompt.dict()
    prompt_dict.update({
        "created_at": now,
        "updated_at": now,
        "versions": [{"version": 1, "content": prompt.content, "created_at": now}]
    })
    prompts_collection.insert_one(prompt_dict)
    return prompt_dict


def update_prompt(prompt_id, new_content: str):
    now = datetime.utcnow()
    prompt = prompts_collection.find_one({"_id": prompt_id})
    if not prompt:
        return None

    # افزایش نسخه
    versions = prompt.get("versions", [])
    new_version_number = len(versions) + 1
    versions.append({"version": new_version_number, "content": new_content, "created_at": now})

    prompts_collection.update_one(
        {"_id": prompt_id},
        {"$set": {"content": new_content, "updated_at": now, "versions": versions}}
    )
    return prompts_collection.find_one({"_id": prompt_id})


def get_prompts(
    owner_id: Optional[str] = None,
    category: Optional[str] = None,
    tags: Optional[List[str]] = None,
    skip: int = 0,
    limit: int = 20
):
    query = {}
    if owner_id:
        query["owner_id"] = owner_id
    if category:
        query["category"] = category
    if tags:
        query["tags"] = {"$all": tags}

    return list(prompts_collection.find(query).sort("created_at", ASCENDING).skip(skip).limit(limit))


# -------------------
# Feedback
# -------------------

def add_feedback(feedback: Feedback):
    feedback_dict = feedback.dict()
    feedback_dict["created_at"] = datetime.utcnow()
    feedback_collection.insert_one(feedback_dict)
    return feedback_dict


def get_feedback(prompt_id: str):
    return list(feedback_collection.find({"prompt_id": prompt_id}).sort("created_at", ASCENDING))


# -------------------
# Indexing پیشنهادی
# -------------------
# اجرا فقط یک بار بعد از اتصال به DB
def create_indexes():
    users_collection.create_index("email", unique=True)
    prompts_collection.create_index("owner_id")
    feedback_collection.create_index("prompt_id")
