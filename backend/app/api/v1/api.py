from fastapi import APIRouter
from .endpoints import vocabulary, users, learning, tests

api_router = APIRouter()

# 添加各模块的路由
api_router.include_router(
    vocabulary.router,
    prefix="/vocabulary",
    tags=["vocabulary"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)

api_router.include_router(
    learning.router,
    prefix="/learning",
    tags=["learning"]
)

api_router.include_router(
    tests.router,
    prefix="/tests",
    tags=["tests"]
) 