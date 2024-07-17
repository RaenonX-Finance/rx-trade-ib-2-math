from rx_trade_ib_2.model.base import BasePydanticModel


class OptionsGexStatsResponse(BasePydanticModel):
    gamma_field: float | None
    gamma_flip: list[float]
    effectiveness: float | None  # Max GEX / (Average Volume * Spot Px)
