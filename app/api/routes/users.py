from typing import Annotated

from fastapi import APIRouter, Body

from app.core.db import db
from app.models import PullRequestShort, User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/setIsActive",
    response_model=User,
    responses={404: {"description": "Пользователь не найден", "content": ""}},
)
async def set_is_active(
    user_id: Annotated[str, Body()],
    is_active: Annotated[bool, Body()],
):
    user = db.get_user_or_raise_not_found(user_id)
    user.is_active = is_active
    return user


@router.get("/getReview")
async def get_review(user_id: str):
    res: list[PullRequestShort] = []
    for pr in db.pull_requests.values():
        if user_id in pr.assigned_reviewers:
            res.append(PullRequestShort(**pr.model_dump()))
    return {
        "user_id": user_id,
        "pull_requests": res,
    }
