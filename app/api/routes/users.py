from typing import Annotated

from fastapi import APIRouter, Body, HTTPException

from app.core.db import db
from app.models import Error, ErrorCode, ErrorResponse, PullRequestShort, User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/setIsActive",
    response_model=User,
    responses={404: {"description": "Пользователь не найден", "content": ""}},
)
async def set_is_active(
    user_id: Annotated[str, Body()],
    is_active: Annotated[str, Body()],
):
    user = db.users.get(user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error=Error(code=ErrorCode.NOT_FOUND, message="Пользователь не найден")
            ).model_dump(),
        )
    user.is_active = is_active
    return user


@router.get("/getReview")
async def get_review(user_id: str):
    res: list[PullRequestShort] = []
    for pr in db.pull_requests.values():
        if user_id in pr.assigned_reviewers:
            res.append(PullRequestShort(**pr.model_dump()))
    return {"pull_requests": res}
