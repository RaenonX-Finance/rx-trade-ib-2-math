import logging

import requests

from rx_trade_ib_2.options.data.thirdparty.polygon.type import (
    PolygonIoOptionChainResponse,
    PolygonIoOptionChainResult,
    PolygonIoOptionContractType,
)
from rx_trade_ib_2.options.data.type.data import OptionChainQuoteData, OptionsContractPx, OptionsContractsOfStrike
from rx_trade_ib_2.options.data.type.request import OptionChainRequest
from rx_trade_ib_2.utils.env import Environment
from rx_trade_ib_2.utils.iter import group_order_agnostic

logger = logging.getLogger("uvicorn.error")


def _get_chain_result_group_key(result: PolygonIoOptionChainResult):
    return result.details.strike_price, result.details.expiration_date


def fetch_data_from_polygon_io(request: OptionChainRequest) -> OptionChainQuoteData:
    ticker = request.ticker

    url_suffix = f"&apiKey={Environment.POLYGON_API_KEY}"

    logger.info("Fetching option chain data from polygon.io")
    response_model = PolygonIoOptionChainResponse.model_validate(
        requests.get(f"https://api.polygon.io/v3/snapshot/options/{ticker}?limit=250{url_suffix}").json()
    )
    while response_model.next_url:
        logger.info(f"Fetching option chain data from polygon.io: {response_model.next_url}")
        response_model.merge_in_place(PolygonIoOptionChainResponse.model_validate(
            requests.get(f"{response_model.next_url}{url_suffix}").json()
        ))

    spot_px = request.spot_px or response_model.results[0].underlying_asset.price

    results_to_process = response_model.results

    # Skip processing contracts
    if request.range_percent is not None:
        results_to_process = [
            result for result in results_to_process
            if abs(result.details.strike_price / spot_px - 1) <= request.range_percent / 100
        ]

    # Skip processing contracts
    if request.expiry_days is not None:
        results_to_process = [
            result for result in results_to_process
            if result.details.days_till_expiry <= request.expiry_days
        ]

    contracts: list[OptionsContractsOfStrike] = []
    for (strike, expiry), results in group_order_agnostic(results_to_process, _get_chain_result_group_key):
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
                px_updated=result.day.last_updated / 1E9 if result.day.last_updated else None,
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
