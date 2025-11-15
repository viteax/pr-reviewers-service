from dataclasses import dataclass, field

from app.exceptions import NotFoundException
from app.models import PullRequest, Team, TeamMember, User


@dataclass
class DataBase:
    users: dict[str, User] = field(default_factory=dict)
    pull_requests: dict[str, PullRequest] = field(default_factory=dict)
    teams: dict[str, Team] = field(default_factory=dict)

    def get_user_or_raise_not_found(self, user_id) -> User:
        user = self.users.get(user_id)
        if not user:
            raise NotFoundException("user not found")
        return user

    def get_pull_request_or_raise_not_found(self, pull_request_id) -> PullRequest:
        pr = db.pull_requests.get(pull_request_id)
        if not pr:
            raise NotFoundException("PR not found")
        return pr

    def get_team_or_raise_not_found(self, team_name) -> Team:
        team = db.teams.get(team_name)
        if not team:
            raise NotFoundException("team not found")
        return team


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
