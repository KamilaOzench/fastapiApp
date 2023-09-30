from fastapi import FastAPI

from src.users.router import router as users_router
from src.todos.router import router as todos_router

world = FastAPI()

world.include_router(users_router)
world.include_router(todos_router)
