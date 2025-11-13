from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class ErrorCode(str, Enum):
    TEAM_EXISTS = 'TEAM_EXISTS'
    PR_EXISTS = 'PR_EXISTS'
    PR_MERGED = 'PR_MERGED'
    NOT_ASSIGNED = 'NOT_ASSIGNED'
    NO_CANDIDATE = 'NO_CANDIDATE'
    NOT_FOUND = 'NOT_FOUND'


class Error(BaseModel):
    code: ErrorCode
    message: str


class ErrorResponse(BaseModel):
    error: Error


class UserBase(BaseModel):
    user_id: str
    username: str
    is_active: bool


class User(UserBase):
    team_name: str


class TeamMember(UserBase):
    pass


class Team(BaseModel):
    team_name: str
    members: list[TeamMember]


class PullRequestStatus(str, Enum):
    OPEN = 'OPEN'
    MERGED = 'MERGED'


class PullRequestBase(BaseModel):
    pull_request_id: str
    pull_request_name: str
    author_id: str
    status: PullRequestStatus


class PullRequestShort(PullRequestBase):
    pass


class PullRequest(PullRequestBase):
    assigned_reviewers: list[str]
    created_at: datetime | None
    merged_at: datetime | None
