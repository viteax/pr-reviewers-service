from dataclasses import dataclass, field

from app.models import PullRequest, Team, TeamMember, User


@dataclass
class DataBase:
    users: dict[str, User] = field(default_factory=dict)
    pull_requests: dict[str, PullRequest] = field(default_factory=dict)
    teams: dict[str, Team] = field(default_factory=dict)


db = DataBase()
db.users["string"] = User(
    user_id="string",
    username="string",
    is_active=False,
    team_name="string",
)
db.teams["string"] = Team(
    team_name="string",
    members=[
        TeamMember(
            user_id="string",
            username="string",
            is_active=True,
        ),
        TeamMember(
            user_id="u1",
            username="Vito",
            is_active=False,
        ),
        TeamMember(
            user_id="u2",
            username="Lucky",
            is_active=True,
        ),
        TeamMember(
            user_id="u3",
            username="Sancho",
            is_active=True,
        ),
    ],
)
