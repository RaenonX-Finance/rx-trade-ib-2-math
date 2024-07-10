from enum import Enum

from rx_trade_ib_2.model.base import IgnoreExtraPydanticModel


class PolygonIoResponseStatus(str, Enum):
    OK = "OK"


class PolygonIoOptionContractType(str, Enum):
    CALL = "call"
    PUT = "put"
    OTHER = "other"


class PolygonIoOptionExerciseStyle(str, Enum):
    AMERICAN = "american"
    EUROPEAN = "european"
    BERMUDAN = "bermudan"


class PolygonIoOptionPxTimeRelevance(str, Enum):
    REALTIME = "REAL-TIME"
    DELAYED = "DELAYED"


class PolygonIoOptionChainDailyBar(IgnoreExtraPydanticModel):
    change: float | None = None
    change_percent: float | None = None
    close: float | None = None
    high: float | None = None
    last_updated: int | None = None  # nanosecond
    low: float | None = None
    open: float | None = None
    previous_close: float | None = None
    volume: float | None = None
    vwap: float | None = None


class PolygonIoOptionChainDetails(IgnoreExtraPydanticModel):
    contract_type: PolygonIoOptionContractType
    exercise_style: PolygonIoOptionExerciseStyle
    expiration_date: str  # YYYY-MM-DD
    shares_per_contract: float
    strike_price: float
    ticker: str


class PolygonIoOptionChainGreeks(IgnoreExtraPydanticModel):
    delta: float | None = None
    gamma: float | None = None
    theta: float | None = None
    vega: float | None = None


class PolygonIoOptionChainUnderlying(IgnoreExtraPydanticModel):
    change_to_break_even: float | None = None
    last_updated: int | None = None  # nanosecond
    price: float | None = None
    ticker: str
    timeframe: PolygonIoOptionPxTimeRelevance | None = None
    value: float | None = None  # index only


class PolygonIoOptionChainResult(IgnoreExtraPydanticModel):
    break_even_price: float | None = None
    day: PolygonIoOptionChainDailyBar
    details: PolygonIoOptionChainDetails
    greeks: PolygonIoOptionChainGreeks
    implied_volatility: float | None = None  # In percent
    open_interest: float
    underlying_asset: PolygonIoOptionChainUnderlying


# https://polygon.io/docs/options/get_v3_snapshot_options__underlyingasset
class PolygonIoOptionChainResponse(IgnoreExtraPydanticModel):
    request_id: str
    results: list[PolygonIoOptionChainResult]
    status: PolygonIoResponseStatus
