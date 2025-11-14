from typing import Annotated

from fastapi import APIRouter, Body, HTTPException

from app.core.db import db
from app.models import Error, ErrorCode, ErrorResponse, PullRequest, PullRequestStatus

router = APIRouter(prefix="/pullRequest", tags=["PullRequests"])


@router.post(
    "/create",
    responses={404: {"description": "Пользователь не найден", "content": ""}},
)
async def create_pull_request(
    pull_request_id: Annotated[str, Body()],
    pull_request_name: Annotated[str, Body()],
    author_id: Annotated[str, Body()],
):
    author = db.users.get(author_id)
    if not author:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error=Error(code=ErrorCode.NOT_FOUND, message="Автор не найден")
            ).model_dump(),
        )
    elif pull_request_id in db.pull_requests:
        raise HTTPException(
            status_code=409,
            detail=ErrorResponse(
                error=Error(code=ErrorCode.PR_EXISTS, message="PR уже существует")
            ).model_dump(),
        )

    team = db.teams.get(author.team_name)
    if not team:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error=Error(code=ErrorCode.NOT_FOUND, message="Команда не найдена")
            ).model_dump(),
        )

    assigned_reviewers = []
    for member in team.members:
        if member.is_active and member.user_id != author.user_id:
            assigned_reviewers.append(member.user_id)
        elif len(assigned_reviewers) == 2:
            break
    pr = PullRequest(
        pull_request_id=pull_request_id,
        pull_request_name=pull_request_name,
        author_id=author_id,
        status=PullRequestStatus.OPEN,
        assigned_reviewers=assigned_reviewers,
    )
    db.pull_requests[pr.pull_request_id] = pr
    return {"pr": pr.model_dump(exclude_none=True)}


@router.post(
    "/merge",
    responses={404: {"description": "Пользователь не найден", "content": ""}},
)
async def assign_merged(
    pull_request_id: Annotated[str, Body()],
):
    pr = db.pull_requests.get(pull_request_id)
    if not pr:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error=Error(code=ErrorCode.NOT_FOUND, message="PR не найден")
            ).model_dump(),
        )
    pr.status = PullRequestStatus.MERGED
    return {"pr": pr}


@router.post("/reassign")
async def reassign_reviewer(
    pull_request_id: Annotated[str, Body()],
    old_user_id: Annotated[str, Body()],
):
    pr = db.pull_requests.get(pull_request_id)
    if not pr:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error=Error(code=ErrorCode.NOT_FOUND, message="PR не найден")
            ).model_dump(),
        )
