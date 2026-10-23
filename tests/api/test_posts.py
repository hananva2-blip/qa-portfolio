import allure
import pytest
from jsonschema import validate

pytestmark = [pytest.mark.api, allure.feature("API")]

POST_SCHEMA = {
    "type": "object",
    "required": ["id", "userId", "title", "body"],
    "properties": {
        "id": {"type": "integer"},
        "userId": {"type": "integer"},
        "title": {"type": "string", "minLength": 1},
        "body": {"type": "string"},
    },
}


@pytest.mark.parametrize("post_id", [1, 50, 100])
def test_get_post_matches_schema(api, post_id):
    response = api.get(f"/posts/{post_id}")

    assert response.status_code == 200
    validate(response.json(), POST_SCHEMA)
    assert response.json()["id"] == post_id


def test_missing_post_returns_404(api):
    assert api.get("/posts/99999").status_code == 404


def test_create_post_echoes_body(api):
    new_post = {"userId": 1, "title": "QA portfolio", "body": "created by a test"}

    response = api.post("/posts", json=new_post)

    body = response.json()
    assert response.status_code == 201
    assert {key: body[key] for key in new_post} == new_post
    assert "id" in body


def test_filter_posts_by_user(api):
    posts = api.get("/posts", params={"userId": 2}).json()

    assert posts, "expected at least one post"
    assert all(post["userId"] == 2 for post in posts)


def test_response_time_under_two_seconds(api):
    response = api.get("/posts/1")

    assert response.elapsed.total_seconds() < 2
