from string import ascii_letters, digits
from typing import TypeVar, Sequence, Iterable, List

from hypothesis.strategies import text, SearchStrategy, sets

safe_id_strategy = text(ascii_letters + digits, min_size=3, max_size=3)
T = TypeVar("T")


def even_sets() -> SearchStrategy:
    def even_sized(xs: Sequence) -> bool:
        return len(xs) % 2 == 0

    return sets(safe_id_strategy, min_size=2).filter(even_sized)


def both(acc: Iterable[T], tup: Sequence[T]) -> List[T]:
    """Accumulate both items from a 2-tuple (or other sequence)"""
    new_acc = list(acc)
    new_acc.extend([tup[0], tup[1]])
    return new_acc
