from itertools import groupby
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")
TKey = TypeVar("TKey")


def group_order_agnostic(iterable: Iterable[T], get_key: Callable[[T], TKey]):
    return groupby(sorted(iterable, key=get_key), get_key)
