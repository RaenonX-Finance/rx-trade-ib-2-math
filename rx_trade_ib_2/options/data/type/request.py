from rx_trade_ib_2.model.base import BasePydanticModel


class OptionChainRequest(BasePydanticModel):
    ticker: str
    spot_px: float | None = None
    range_percent: float | None = None
    expiry_days: int | None = None
