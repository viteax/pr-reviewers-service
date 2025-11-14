from fastapi import APIRouter, HTTPException

from app.core.db import db
from app.models import Error, ErrorCode, ErrorResponse, Team

router = APIRouter(prefix="/team", tags=["Teams"])


@router.post("/add", status_code=201, response_model=Team)
async def add_team(team: Team):
    if db.teams.get(team.team_name):
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(
                error=Error(
                    code=ErrorCode.TEAM_EXISTS, message="Команда уже существует"
                )
            ).model_dump(),
        )
    db.teams[team.team_name] = team
    return team


@router.get(
    "/get",
    response_model=Team,
)
async def get_team(team_name: str):
    team = db.teams.get(team_name)
    if not team:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error=Error(code=ErrorCode.NOT_FOUND, message="Команда не найдена")
            ).model_dump(),
        )
    return team
