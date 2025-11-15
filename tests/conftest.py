import random
from collections.abc import Generator
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from faker import Faker
from fastapi.testclient import TestClient

from app.core.db import db
from app.main import app
from app.models import PullRequest, PullRequestStatus, Team, TeamMember, User

TEAMS_COUNT = 20
USERS_COUNT = 200
PR_COUNT = 1000

faker = Faker("ru")


@pytest.fixture
def fake_db():
    users_per_team = USERS_COUNT // TEAMS_COUNT
    for i in range(TEAMS_COUNT):
        team = Team(
            team_name=faker.city(),
            members=[
                TeamMember(
                    user_id=f"u{i * users_per_team + j}",
                    username=faker.user_name(),
                    is_active=random.randint(0, 1),
                )
                for j in range(1, users_per_team + 1)
            ],
        )
        db.teams[team.team_name] = team
        for member in team.members:
            db.users[member.user_id] = User(
                **member.model_dump(),
                team_name=team.team_name,
            )
    for i in range(PR_COUNT):
        pr = PullRequest(
            pull_request_id=f"pr-{i}",
            author_id=f"u{random.randint(1, USERS_COUNT)}",
            pull_request_name=faker.file_name(),
            status=random.choice(
                [
                    PullRequestStatus.OPEN,
                    PullRequestStatus.MERGED,
                ]
            ),
            assigned_reviewers=[],
        )
        if pr.status == PullRequestStatus.MERGED:
            pr.merged_at = datetime.now(ZoneInfo("Europe/Moscow"))
        author = db.get_user_or_raise_not_found(pr.author_id)
        team = db.get_team_or_raise_not_found(author.team_name)
        for member in random.sample(team.members, len(team.members)):
            if member.is_active and member.user_id != author.user_id:
                pr.assigned_reviewers.append(member.user_id)
            if len(pr.assigned_reviewers) == 2:
                break
        db.pull_requests[pr.pull_request_id] = pr
    return db


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
