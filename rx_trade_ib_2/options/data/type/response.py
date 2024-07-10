from rx_trade_ib_2.model.base import BasePydanticModel
from rx_trade_ib_2.options.data.type.data import OptionChainQuoteData
from rx_trade_ib_2.options.gex.response import OptionsGexStatsResponse


class OptionChainResponse(BasePydanticModel):
    quote: OptionChainQuoteData
    gex: OptionsGexStatsResponse
