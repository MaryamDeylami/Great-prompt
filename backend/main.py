# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from typing import List

from . import crud, models, llm
from .auth import create_access_token, verify_token

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# -------------------
# Users
# -------------------
@app.post("/register", response_model=models.UserOut)
def register(user: models.User):
    try:
        if crud.get_user(user.email):
            raise HTTPException(status_code=400, detail="User already exists")
        created_user = crud.create_user(user)
        return {"message": "User created", "user": created_user}
    except Exception as e:
        # این خط باعث می‌شود خطای واقعی در ترمینال نشان داده شود
        print("Error in register:", e)
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/login")
def login(data: models.LoginData):
    user = crud.authenticate_user(data.email, data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"email": user['email'], "role": user['role']})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me")
def get_me(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"email": payload['email'], "role": payload.get("role")}

@app.get("/users/{email}", response_model=models.UserOut)
def get_user(email: str):
    user = crud.get_user(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"email": user["email"], "role": user["role"]}

# -------------------
# Prompts
# -------------------
@app.post("/prompts")
def add_prompt(prompt: models.Prompt, token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    prompt.user_email = payload['email']
    return crud.create_prompt(prompt)

@app.get("/prompts")
def list_prompts(skip: int = 0, limit: int = 20):
    return crud.get_prompts(skip=skip, limit=limit)

# -------------------
# Feedback
# -------------------
@app.post("/feedback")
def send_feedback(feedback: models.Feedback, token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    feedback.user_email = payload['email']
    return crud.add_feedback(feedback)

# -------------------
# LLM
# -------------------
@app.post("/ai")
def ask_ai(prompt: models.Prompt):
    try:
        response = llm.get_ai_response(prompt.text)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")
