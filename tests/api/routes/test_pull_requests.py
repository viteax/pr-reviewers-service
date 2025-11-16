from fastapi.testclient import TestClient

from app.core.db import DataBase
from app.models import PullRequest, PullRequestStatus


def test_create_pull_request(client: TestClient, fake_db: DataBase):
    pull_request_id = "pr-100000"
    pull_request_name = "add read feature"
    author_id = "u3"

    r = client.post(
        "/pullRequest/create",
        json={
            "pull_request_id": pull_request_id,
            "pull_request_name": pull_request_name,
            "author_id": author_id,
        },
    )
    pr = PullRequest.model_validate(r.json()["pr"])

    assert pr == fake_db.get_pull_request_or_raise_not_found(pull_request_id)


def test_merge(client: TestClient, fake_db: DataBase):
    pull_request_id = "pr-10"

    r = client.post(
        "/pullRequest/merge",
        json={"pull_request_id": pull_request_id},
    )
    pr = PullRequest.model_validate(r.json()["pr"])

    assert pr.status == PullRequestStatus.MERGED
    assert (
        fake_db.get_pull_request_or_raise_not_found(pull_request_id).status
        == PullRequestStatus.MERGED
    )


def test_reassign(client: TestClient, fake_db: DataBase):
    pull_request_id = f"pr-{len(fake_db.pull_requests) + 1}"
    old_user_id = "u3"

    fake_db.pull_requests[pull_request_id] = PullRequest(
        pull_request_id=pull_request_id,
        pull_request_name="add feature",
        author_id="u1",
        assigned_reviewers=["u2", old_user_id],
        status=PullRequestStatus.OPEN,
    )

    r = client.post(
        "/pullRequest/reassign",
        json={
            "pull_request_id": pull_request_id,
            "old_user_id": old_user_id,
        },
    )
    data = r.json()
    pr = PullRequest.model_validate(data["pr"])
    replaced_by = data["replaced_by"]

    assert pr == fake_db.get_pull_request_or_raise_not_found(pull_request_id)
    assert old_user_id not in pr.assigned_reviewers
    assert replaced_by in pr.assigned_reviewers
    assert replaced_by != pr.author_id
