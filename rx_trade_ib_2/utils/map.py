from typing import Callable, Iterable, TypeVar

from rx_trade_ib_2.utils.iter import group_order_agnostic

T = TypeVar("T")
TKey = TypeVar("TKey")


def get_grouped_dict(iterable: Iterable[T], get_key: Callable[[T], TKey]) -> dict[TKey, list[T]]:
    return {k: list(g) for k, g in group_order_agnostic(iterable, get_key)}
