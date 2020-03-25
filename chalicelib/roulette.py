from random import shuffle
from typing import NewType, Text, Set, Tuple, Iterable

UserId = NewType("UserID", Text)


def choose_pairs(member_ids: Iterable[UserId]) -> Set[Tuple[UserId, UserId]]:
    """Choose pairings of IDs, ensuring no ID is used twice.
    If there are an uneven amount, then one ID will not be counted"""
    available = list(member_ids)
    shuffle(available)
    combos = set()
    while available:
        try:
            fst = available.pop()
            snd = available.pop()
        except IndexError:
            break
        combos.add((fst, snd))
    return combos
