from fastapi import APIRouter

from app.api.routes import pull_requests, team, users

# from app.core.config import settings

api_router = APIRouter()
api_router.include_router(team.router)
api_router.include_router(users.router)
api_router.include_router(pull_requests.router)


# if settings.ENVIRONMENT == "local":
#     api_router.include_router()
