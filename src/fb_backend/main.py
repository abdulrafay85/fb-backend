from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from enum import Enum
from fastapi.responses import RedirectResponse
from fastapi import Request, Response
from typing import Dict, Any, List, Annotated
from fastapi import Response
from dataclasses import dataclass
from fastapi import FastAPI, HTTPException, Query, Path
from fb_backend.mock import fake_products
from fb_backend.db import ShortTermMemory
from fb_backend.security import hash_password, verify_password, create_manual_token, verify_manual_token
import uuid
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from fb_backend.mock import inventory
from fb_backend.schemas import UserSignup, UserLogin
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000", "*"],  # Frontend ka URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize short term memory
memory = ShortTermMemory()

## version 3
# @app.post("/signup")
# async def signup(user: UserSignup):
    
#     # Check if email exists
#     for user_item in memory.buffer:
#         if user_item.data["email"] == user.email:
#             raise HTTPException(status_code=400, detail="Email already registered")
    
#     # Hash password & create user
#     hashed_password = hash_password(user.password)
#     user_id = str(uuid.uuid4())
#     memory.add_memory(data={"email": user.email, "password": hashed_password}, user_id=user_id, run_id="run_1")
    
#     # Return JSON
#     return {"message": "User created", "user_id": user_id}

@app.post("/signup")
async def signup(user: UserSignup):
    print(f"user: {user}")
    # Check if email exists
    for user_item in memory.buffer:
        print(f"user_item: {user_item}")
        if user_item.data["email"] == user.email:
            print(f"email already exists {user.email}")
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password & create user
    hashed_password = hash_password(user.password)
    user_id = str(uuid.uuid4())
    print(f"user_id: {user_id}")
    print(f"hashed_password: {hashed_password}")
    print(f"user.email: {user.email}")
    memory.add_memory(data={"email": user.email, "password": hashed_password}, user_id=user_id, run_id="run_1")
    print("add memory done")

    # Return JSON
    return {"message": "User created", "user_id": user_id}

# @app.post("/signup")
# async def signup(user: UserSignup):
#     print(f"Received signup: {user}")


# # version 3
# @app.post("/login")
# async def login(user: UserLogin, response: Response):
#     for user_item in memory.buffer:
#         if user_item.data.get("email") == user.email:
#             if verify_password(user.password, user_item.data.get("password")):
#                 token = create_manual_token(user_item.user_id)
#                 response.set_cookie(
#                     key="access_token",
#                     value=token,
#                     httponly=True,
#                     secure=False,
#                     samesite="lax"
#                 )

#                 return {"message": "Logged in successfully"}

#             raise HTTPException(status_code=401, detail="Invalid credentials")

#     raise HTTPException(status_code=401, detail="Invalid credentials")

# ---- Login endpoint ----
# @app.post("/login")
# async def login(user: UserLogin):
    
#     email = user.email
#     password = user.password

#     for user_item in memory.buffer:
#         if user_item.data.get("email") == email:
#             if verify_password(password, user_item.data.get("password")):
#                 token = create_manual_token(user_item.user_id)
#                 manual_tokens = {}  # token -> user_id
#                 manual_tokens[token] = user_item.user_id


#                 response.set_cookie(
#                     key="access_token",
#                     value=token,
#                     httponly=True,
#                     secure=False,  # production me True
#                     samesite="lax"
#                 )
#                 return JSONResponse({"message": "Logged in successfully", "token": token})

#             raise HTTPException(status_code=401, detail="Invalid credentials")

#     raise HTTPException(status_code=401, detail="Invalid credentials")


# ----------------

# @app.post("/login")
# async def login(user: UserLogin):
#     print(f"user: {user}")
#     print(f"Total users in memory: {len(memory.buffer)}")
#     print(f"All users: {[u.data.get('email') for u in memory.buffer]}")
#     # User ko find karo
#     found_user = None
#     # print(f"memory.buffer: {memory.buffer}")
#     for user_item in memory.buffer:
#         print(f"user_item: {user_item}")
#         if user_item.data.get("email") == user.email:
#             print(f"User found {user_item.data.get("email")}")
#             found_user = user_item
#             print(f"found_user: {found_user}")
    
#     # Check if user exists
#     if not found_user:
#         print(f"User not found")
#         raise HTTPException(status_code=401, detail="Invalid credentials")
    
#     # Verify password
#     if not verify_password(user.password, found_user.data["password"]):
#         print(f"Password not match")
#         raise HTTPException(status_code=401, detail="Invalid credentials")
    
#     # Create token
#     token = create_manual_token(found_user.user_id)
#     print(f"token: {token}")
    
#     # Response object banao
#     response = JSONResponse(content={"message": "Login successful", "user_id": found_user.user_id})
#     print(f"response: {response}")
    
#     # Cookie set karo
#     response.set_cookie(
#         key="access_token",
#         value=token,
#         httponly=True,
#         max_age=3600,  # 1 hour
#         samesite="lax"
#     )
#     print(f"response: {response}")    
#     return response

@app.post("/login")
async def login(user: UserLogin):
    print(f"user: {user}")
    print(f"Total users in memory: {len(memory.buffer)}")
    print(f"All users: {[u.data.get('email') for u in memory.buffer]}")
    
    found_user = None
    for user_item in memory.buffer:
        print(f"user_item: {user_item}")
        if user_item.data.get("email") == user.email:
            print(f"User found {user_item.data.get('email')}")
            found_user = user_item
            print(f"found_user: {found_user}")
    
    if not found_user:
        print(f"User not found")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(user.password, found_user.data["password"]):
        print(f"Password not match")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_manual_token(found_user.user_id) 
    print(f"token: {token}")
    
    response = JSONResponse(content={"message": "Login successful", "user_id": found_user.user_id})
    print(f"response: {response}")
    
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=3600,
        samesite="lax"
    )
    print(f"response: {response}")
    
    return response

# # Login function mein debug ke liye ye add karo:
# @app.post("/login")
# async def login(user: UserLogin):
#     print(f"Total users in memory: {len(memory.buffer)}")  # Ye line add karo
#     print(f"All users: {[u.data.get('email') for u in memory.buffer]}")  # Ye bhi
#     # ... baaki code
    
# ---- Check token endpoint (frontend-friendly) ----
# @app.get("/check-token")
# async def check_token(request: Request):
#     token = request.cookies.get("access_token")
#     if not token or not verify_manual_token(token):
#         return Response({"logged_in": False})
#     return Response({"logged_in": True, "user_id": verify_manual_token(token)})

@app.get("/check-token")
async def check_token(request: Request):
    token = request.cookies.get("access_token")
    if not token or not verify_manual_token(token):
        return {"logged_in": False}
    return {"logged_in": True, "user_id": verify_manual_token(token)}

# ---- Root page (browser redirect for direct visit) ----
@app.get("/")
async def root(request: Request):
    token = request.cookies.get("access_token")
    if not token or not verify_manual_token(token):
        return RedirectResponse("http://127.0.0.1:3002/src/class_1/frontend/signup.html", status_code=302)
    return Response(
        content="Hello World",
        status_code=200,
        media_type="application/json"
    )