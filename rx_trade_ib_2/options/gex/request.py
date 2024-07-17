from typing import Self

from pydantic import model_validator

from rx_trade_ib_2.const import LOGGER
from rx_trade_ib_2.model.base import BasePydanticModel


class OptionsGexPriceData(BasePydanticModel):
    expiry: str  # YYYYMMDD
    strike: float

    call_iv: float
    call_gamma: float
    call_oi: int

    put_iv: float
    put_gamma: float
    put_oi: int


class OptionsGexStatsRequest(BasePydanticModel):
    spot_price: float
    options_price: list[OptionsGexPriceData]
    expiry_exclusions: list[str]  # YYYYMMDD

    @model_validator(mode="after")
    def ensure_model(self) -> Self:
        if not self.expiry_exclusions:
            return self

        excluded_expiry = set(self.expiry_exclusions)
        LOGGER.info("GEX calculation to exclude the following expiry: %s", excluded_expiry)

        self.options_price = [
            option_px for option_px in self.options_price
            if option_px.expiry not in excluded_expiry
        ]

        return self

    @property
    def strike_min(self):
        return min(px.strike for px in self.options_price)

    @property
    def strike_max(self):
        return max(px.strike for px in self.options_price)
