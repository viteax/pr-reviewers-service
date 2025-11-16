import random
from datetime import datetime
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse

from app.core.db import db
from app.exceptions import ConflictException, NotFoundException
from app.models import ErrorCode, PullRequest, PullRequestStatus

router = APIRouter(prefix="/pullRequest", tags=["PullRequests"])


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_class=JSONResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "user/team not found"},
        status.HTTP_409_CONFLICT: {"description": "pr already exists"},
    },
)
async def create_pull_request(
    pull_request_id: Annotated[str, Body()],
    pull_request_name: Annotated[str, Body()],
    author_id: Annotated[str, Body()],
) -> JSONResponse:
    author = db.get_user_or_raise_not_found(author_id)
    team = db.get_team_or_raise_not_found(author.team_name)

    if pull_request_id in db.pull_requests:
        raise ConflictException(code=ErrorCode.PR_EXISTS, message="PR already exists")

    assigned_reviewers = []
    for member in random.sample(team.members, len(team.members)):
        if member.is_active and member.user_id != author.user_id:
            assigned_reviewers.append(member.user_id)
        if len(assigned_reviewers) == 2:
            break

    pr = PullRequest(
        pull_request_id=pull_request_id,
        pull_request_name=pull_request_name,
        author_id=author_id,
        status=PullRequestStatus.OPEN,
        assigned_reviewers=assigned_reviewers,
    )
    db.pull_requests[pr.pull_request_id] = pr
    return JSONResponse(
        content={"pr": pr.model_dump(exclude_none=True, mode="json")},
        status_code=status.HTTP_201_CREATED,
    )


@router.post(
    "/merge",
    responses={status.HTTP_404_NOT_FOUND: {"description": "pr not found"}},
)
async def assign_merged(pull_request_id: Annotated[str, Body(embed=True)]):
    pr = db.get_pull_request_or_raise_not_found(pull_request_id)
    if pr.status == PullRequestStatus.OPEN:
        pr.merged_at = datetime.now(ZoneInfo("Europe/Moscow"))
    pr.status = PullRequestStatus.MERGED
    return {"pr": pr}


@router.post(
    "/reassign",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "user/team not found"},
        status.HTTP_409_CONFLICT: {"description": "domain data assign conflict"},
    },
)
async def reassign_reviewer(
    pull_request_id: Annotated[str, Body()],
    old_user_id: Annotated[str, Body()],
):
    pr = db.get_pull_request_or_raise_not_found(pull_request_id)
    user = db.get_user_or_raise_not_found(old_user_id)
    team = None

    if pr.status == PullRequestStatus.MERGED:
        raise ConflictException(
            code=ErrorCode.PR_MERGED, message="cannot reassign on merged PR"
        )
    elif old_user_id not in pr.assigned_reviewers:
        raise ConflictException(
            code=ErrorCode.NOT_ASSIGNED, message="reviewer is not assigned to this PR"
        )

    try:
        team = db.get_team_or_raise_not_found(user.team_name)
    except NotFoundException:
        raise ConflictException(
            code=ErrorCode.NO_CANDIDATE,
            message="no active replacement candidate in team",
        )

    replaced_by: str | None = None
    for member in team.members:
        if member.user_id == pr.author_id or not member.is_active:
            continue
        elif member.user_id not in pr.assigned_reviewers:
            replaced_by = member.user_id
            pr.assigned_reviewers[pr.assigned_reviewers.index(old_user_id)] = (
                replaced_by
            )
            break
    if not replaced_by:
        raise ConflictException(
            code=ErrorCode.NO_CANDIDATE,
            message="no active replacement candidate in team",
        )
    return {"pr": pr, "replaced_by": replaced_by}
