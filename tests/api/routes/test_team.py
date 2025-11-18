import random

from faker import Faker
from fastapi.testclient import TestClient

from app.core.db import DataBase
from app.models import Team, TeamMember, User


def test_get_team(client: TestClient, fake_db: DataBase):
    team_name = next(iter(fake_db.teams.keys()))
    r = client.get("/team/get", params={"team_name": team_name})
    team = r.json()
    assert team
    assert team == fake_db.teams[team_name].model_dump()


def test_add_team(client: TestClient, fake_db: DataBase):
    faker = Faker("ru")
    team = Team(
        team_name=faker.city(),
        members=[
            TeamMember(
                user_id=f"u{len(fake_db.users) + i}",
                username=faker.user_name(),
                is_active=random.randint(0, 1),
            )
            for i in range(10)
        ],
    )
    r = client.post("/team/add", json=team.model_dump())
    r_team = Team.model_validate(r.json())
    correct_users = [
        User(**member.model_dump(), team_name=team.team_name) for member in team.members
    ]
    users = [
        fake_db.get_user_or_raise_not_found(member.user_id) for member in team.members
    ]

    assert r_team.team_name in fake_db.teams
    assert r_team == team
    assert r_team == fake_db.get_team_or_raise_not_found(r_team.team_name)
    assert users == correct_users
