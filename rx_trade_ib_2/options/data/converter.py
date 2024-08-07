from rx_trade_ib_2.options.data.type.data import OptionChainQuoteData
from rx_trade_ib_2.options.data.type.request import OptionChainRequest
from rx_trade_ib_2.options.gex.request import OptionsGexPriceData, OptionsGexStatsRequest


def to_gex_stats_request(
    quote: OptionChainQuoteData,
    request: OptionChainRequest,
) -> OptionsGexStatsRequest:
    return OptionsGexStatsRequest(
        spot_price=quote.spot_px,
        avg_volume=request.avg_volume,
        options_price=[
            OptionsGexPriceData(
                expiry=contract.expiry,
                strike=contract.strike,
                call_iv=quote.option_px[contract.call].iv if contract.call else 0,
                call_gamma=(quote.option_px[contract.call].gamma or 0) if contract.call else 0,
                call_oi=quote.option_px[contract.call].open_interest if contract.call else 0,
                put_iv=quote.option_px[contract.put].iv if contract.put else 0,
                put_gamma=(quote.option_px[contract.put].gamma or 0) if contract.put else 0,
                put_oi=quote.option_px[contract.put].open_interest if contract.put else 0,
            )
            for contract in quote.contracts
        ],
        expiry_exclusions=request.gex_expiry_exclusions or []
    )
