from functools import reduce
from typing import Set

from hypothesis import given
from hypothesis.strategies import sets

from chalicelib.roulette import choose_pairs, UserId
from tests.strategies import safe_id_strategy, even_sets, both


@given(even_sets())
def test_choose_pairs_includes_everyone_when_even(ids: Set[UserId]):
    pairs = choose_pairs(ids)
    # IDs can appear either in the first or second part of the tuple...
    all_ids = reduce(both, pairs)
    assert ids == set(all_ids), "Some IDs were forgotten!"


@given(sets(safe_id_strategy))
def test_choose_pairs_has_no_duplicates(ids: Set[UserId]):
    pairs = choose_pairs(ids)
    all_ids = reduce(both, pairs, [])
    assert 0 <= len(ids) - len(all_ids) <= 1, f"Got {len(all_ids)}: {all_ids}"
