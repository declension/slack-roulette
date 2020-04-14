import re
from typing import List, Text, Dict
from unittest.mock import Mock
from urllib.parse import quote

from chalice.app import Request
from hypothesis import given
from hypothesis.strategies import lists
from slack.web.slack_response import SlackResponse

from app import roulette, app
from chalicelib.roulette import UserId
from chalicelib.slack import LazySlackClient, response_for_members, BULLET
from tests.strategies import safe_id_strategy


@given(lists(safe_id_strategy, min_size=2, max_size=100, unique=True))
def test_response_for_members_has_correct_output(ids: List[UserId]):
    user_ids = {UserId(f"user_{uid}") for uid in ids}
    output = response_for_members(user_ids)
    user_regex = re.compile(r"<@user_\w+>")
    users = user_regex.findall(output)
    assert users, "Couldn't find any usernames in output"
    assert 0 <= len(ids) - len(users) <= 1, "Found wrong number of usernames"


def test_roulette_endpoint():
    mock_client = Mock(LazySlackClient)

    response_data = {
        "ok": True,
        "members": [
            "U023BECGF",
            "U061F7AUR",
            "W012A3CDE"
        ],
        "response_metadata": {
            "next_cursor": "e3VzZXJfaWQ6IFcxMjM0NTY3fQ=="}
    }
    response = SlackResponse(client=mock_client, http_verb="POST", api_url="",
                             req_args={}, data=response_data, headers={},
                             status_code=200)
    app.slack_client = mock_client
    mock_client.conversations_members.return_value = response

    app.current_request = www_request_of(
        data={"channel_id": "1234"},
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    resp = roulette()
    assert resp
    text = resp["text"]
    assert "How about chats between" in text
    assert BULLET in text


def www_request_of(data: Dict[Text, Text], headers=None):
    merged = {"token": "foobar123", "channel_name": "privategroup"}
    merged.update(data)
    body = "&".join(f"{quote(k)}={quote(v)}" for k, v in merged.items())
    return Request(query_params={}, headers=headers or {}, uri_params={},
                   method="POST", body=body.encode("utf-8"), context={},
                   stage_vars={}, is_base64_encoded=False)
