import re
from typing import List

from hypothesis import given
from hypothesis.strategies import lists

from app import response_for_members, UserId
from tests.strategies import safe_id_strategy


@given(lists(safe_id_strategy, min_size=2, max_size=100, unique=True))
def test_choose_pairs_has_no_duplicates(ids: List[UserId]):
    user_ids = {UserId(f"user_{uid}") for uid in ids}
    output = response_for_members(user_ids)
    user_regex = re.compile(r"<@user_\w+>")
    users = user_regex.findall(output)
    assert users, "Couldn't find any usernames in output"
    assert 0 <= len(ids) - len(users) <= 1, "Found wrong number of usernames"
