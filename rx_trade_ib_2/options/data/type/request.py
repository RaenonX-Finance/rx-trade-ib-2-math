from rx_trade_ib_2.model.base import BasePydanticModel


class OptionChainRequest(BasePydanticModel):
    ticker: str
    spot_px: float | None = None
    avg_volume: float | None = None
    range_percent: float | None = None
    expiry_days: int | None = None
    gex_expiry_exclusions: list[str] | None = None  # YYYYMMDD
