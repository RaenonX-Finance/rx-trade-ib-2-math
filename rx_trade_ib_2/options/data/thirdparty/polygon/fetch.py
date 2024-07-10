import requests

from rx_trade_ib_2.options.data.thirdparty.polygon.type import (
    PolygonIoOptionChainResponse,
    PolygonIoOptionChainResult, PolygonIoOptionContractType,
)
from rx_trade_ib_2.options.data.type.data import OptionChainQuoteData, OptionsContractPx, OptionsContractsOfStrike
from rx_trade_ib_2.options.data.type.request import OptionChainRequest
from rx_trade_ib_2.utils.env import Environment
from rx_trade_ib_2.utils.iter import group_order_agnostic


def _get_chain_result_group_key(result: PolygonIoOptionChainResult):
    return result.details.strike_price, result.details.expiration_date


def fetch_data_from_polygon_io(request: OptionChainRequest) -> OptionChainQuoteData:
    ticker = request.ticker

    response = requests.get(
        f"https://api.polygon.io/v3/snapshot/options/{ticker}?limit=250&apiKey={Environment.POLYGON_API_KEY}"
    )
    response_model = PolygonIoOptionChainResponse.model_validate(response.json())

    spot_px = request.spot_px or response_model.results[0].underlying_asset.price

    contracts: list[OptionsContractsOfStrike] = []
    for (strike, expiry), results in group_order_agnostic(response_model.results, _get_chain_result_group_key):
        call: PolygonIoOptionChainResult = next(
            (result for result in results if result.details.contract_type == PolygonIoOptionContractType.CALL),
            None)
        put: PolygonIoOptionChainResult = next(
            (result for result in results if result.details.contract_type == PolygonIoOptionContractType.PUT),
            None
        )

        contracts.append(OptionsContractsOfStrike(
            call=call.details.ticker if call else None,
            put=put.details.ticker if put else None,
            strike=strike,
            expiry=expiry
        ))

    return OptionChainQuoteData(
        ticker=ticker,
        spot_px=spot_px,
        option_px={
            result.details.ticker: OptionsContractPx(
                ticker=result.details.ticker,
                # FIXME: Could be incorrect, inquiring
                px=result.day.close,
                # FIXME: Could be incorrect, inquiring
                px_updated=result.day.last_updated,
                open_interest=result.open_interest,
                # IV could be empty, not sure how to handle it, so keeping 0 for now
                iv=result.implied_volatility / 100 if result.implied_volatility else 0,
                delta=result.greeks.delta,
                theta=result.greeks.theta,
                gamma=result.greeks.gamma,
                vega=result.greeks.vega,
            )
            for result in response_model.results
        },
        contracts=contracts,
    )
