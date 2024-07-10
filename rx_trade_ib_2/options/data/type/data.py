from rx_trade_ib_2.model.base import BasePydanticModel


class OptionsContractPx(BasePydanticModel):
    ticker: str
    px: float | None = None
    px_updated: float | None = None
    open_interest: int
    iv: float
    delta: float | None = None
    theta: float | None = None
    gamma: float | None = None
    vega: float | None = None


class OptionsContractsOfStrike(BasePydanticModel):
    call: str | None
    put: str | None
    strike: float
    expiry: str  # YYYY-MM-DD


class OptionChainQuoteData(BasePydanticModel):
    ticker: str
    spot_px: float
    option_px: dict[str, OptionsContractPx]
    contracts: list[OptionsContractsOfStrike]
