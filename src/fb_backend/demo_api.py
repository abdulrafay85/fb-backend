import re
from security import hash_password, verify_password, create_manual_token, verify_manual_token
from fb_backend.schemas import UserSignup, UserLogin
from fastapi import HTTPException
from fb_backend.db import ShortTermMemory
import uuid

def email_exists(email: str, user_item):
    if user_item.data.get("email") == email:
        raise HTTPException(status_code=400, detail="Email already registered")
    return False

memory = ShortTermMemory()

# # Signup endpoint
@app.post("/signup")
async def signup(user: UserSignup):
    # Check if email already exists
    for user_item in memory.buffer:
        email_exists(user.email, user_item)
    
    hashed_password = hash_password(user.password)
    user_id = str(uuid.uuid4())
    memory.add_memory(data={"email": user.email, "password": hashed_password}, user_id=user_id, run_id="run_1")
    return {"message": "User created", "user_id": user_id}
    
# # Login endpoint 
@app.post("/login")
async def login(user: UserLogin):
    for user_item in memory.buffer:
        print(f"user_item: {user_item}")
        if user_item.data["email"] == user.email:
            if verify_password(user.password, user_item.data["password"]):
                token = create_manual_token(user_item.user_id)
                return {
                    "message": "Logged in", 
                    "token": token,
                    "user_id": user_item.user_id  # Ye add kiya
                }
            else:
                raise HTTPException(status_code=401, detail="Invalid credentials")
    raise HTTPException(status_code=404, detail="User not found")
