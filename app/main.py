from fastapi import FastAPI
from pydantic import BaseModel
from app.routes.resume import router

app=FastAPI()

app.include_router(router)

@app.get("/")
def home():
    return {"message": "resume analyzer Api"}

# @app.get("users/{user_id}")
# def get_user(user_id: int):
#     return {"user_id": user_id}

# @app.get("/users")
# def get_users(name: str):
#     return {"name":name}

# class User(BaseModel):
#     name:str
#     experience:int

# @app.post("/users")
# def users(user:User):
#     return user

