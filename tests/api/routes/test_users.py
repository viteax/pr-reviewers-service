from fastapi import status
from fastapi.testclient import TestClient

from app.core.db import DataBase
from app.models import PullRequestShort, User


def test_set_is_active(client: TestClient, fake_db: DataBase) -> None:
    user_id = "u3"
    is_active = True

    r = client.post(
        "/users/setIsActive",
        json={
            "user_id": user_id,
            "is_active": is_active,
        },
    )
    user = User.model_validate(r.json())
    assert user
    assert user.user_id == user_id
    assert user.is_active == is_active


def test_set_is_active_validation_error(client: TestClient, fake_db: DataBase) -> None:
    user_id = "u3"
    is_active = "323"

    r = client.post(
        "/users/setIsActive",
        json={
            "user_id": user_id,
            "is_active": is_active,
        },
    )
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_set_is_active_not_found_error(client: TestClient, fake_db: DataBase) -> None:
    user_id = "non_exist_user"
    is_active = "1"

    r = client.post(
        "/users/setIsActive",
        json={
            "user_id": user_id,
            "is_active": is_active,
        },
    )
    assert r.status_code == status.HTTP_404_NOT_FOUND


def test_get_review(client: TestClient, fake_db: DataBase) -> None:
    user_id = "u162"
    r = client.get("/users/getReview", params={"user_id": user_id})
    data = r.json()

    us_id = data["user_id"]
    pull_requests = data["pull_requests"]
    correct_pull_requests = []
    for pr in fake_db.pull_requests.values():
        if user_id in pr.assigned_reviewers:
            correct_pull_requests.append(
                PullRequestShort(**pr.model_dump()).model_dump()
            )

    assert us_id == user_id
    assert pull_requests == correct_pull_requests
    assert pull_requests != []


def test_get_review_not_exist_user(client: TestClient, fake_db: DataBase) -> None:
    user_id = "not_exist_user_id"
    correct_pull_requests = []

    r = client.get("/users/getReview", params={"user_id": user_id})
    data = r.json()

    us_id = data["user_id"]
    pull_requests = data["pull_requests"]

    assert us_id == user_id
    assert pull_requests == correct_pull_requests
