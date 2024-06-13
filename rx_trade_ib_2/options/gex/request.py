from rx_trade_ib_2.model.base import BasePydanticModel


class OptionsGexPriceData(BasePydanticModel):
    expiry: str
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

    @property
    def strike_min(self):
        return min(px.strike for px in self.options_price)

    @property
    def strike_max(self):
        return max(px.strike for px in self.options_price)
