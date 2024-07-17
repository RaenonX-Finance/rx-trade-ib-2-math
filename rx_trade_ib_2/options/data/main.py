from rx_trade_ib_2.options.data.converter import to_gex_stats_request
from rx_trade_ib_2.options.data.thirdparty.polygon.fetch import fetch_data_from_polygon_io
from rx_trade_ib_2.options.data.type.request import OptionChainRequest
from rx_trade_ib_2.options.data.type.response import OptionChainResponse
from rx_trade_ib_2.options.gex.main import calc_gex_stats


def get_option_chain(request: OptionChainRequest) -> OptionChainResponse:
    quote = fetch_data_from_polygon_io(request)
    gex = calc_gex_stats(to_gex_stats_request(quote, request))

    return OptionChainResponse(quote=quote, gex=gex)
