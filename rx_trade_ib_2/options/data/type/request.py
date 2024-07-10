from rx_trade_ib_2.model.base import BasePydanticModel


class OptionChainRequest(BasePydanticModel):
    ticker: str
    spot_px: float | None = None
