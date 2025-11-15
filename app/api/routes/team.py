from fastapi import APIRouter

from app.core.db import db
from app.exceptions import ConflictException
from app.models import ErrorCode, Team, User

router = APIRouter(prefix="/team", tags=["Teams"])


@router.post("/add", status_code=201, response_model=Team)
async def add_team(team: Team):
    if db.teams.get(team.team_name):
        raise ConflictException(
            code=ErrorCode.TEAM_EXISTS, message=f"{team.team_name} already exists"
        )
    db.teams[team.team_name] = team
    for member in team.members:
        db.users[member.user_id] = User(
            **member.model_dump(),
            team_name=team.team_name,
        )
    return team


@router.get(
    "/get",
    response_model=Team,
)
async def get_team(team_name: str):
    return db.get_team_or_raise_not_found(team_name)
