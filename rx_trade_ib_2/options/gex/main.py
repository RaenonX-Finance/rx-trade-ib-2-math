from datetime import datetime

import numpy as np
import pandas as pd

from rx_trade_ib_2.const import LOGGER, TZ_US_EXCHANGE
from rx_trade_ib_2.options.gex.gamma_field import calc_gamma_field
from rx_trade_ib_2.options.gex.gamma_flip import calc_gamma_flip
from rx_trade_ib_2.options.gex.net_gamma import calc_net_gamma_at_price
from rx_trade_ib_2.options.gex.request import OptionsGexStatsRequest
from rx_trade_ib_2.options.gex.response import OptionsGexStatsResponse


def calc_gex_stats(request: OptionsGexStatsRequest) -> OptionsGexStatsResponse:
    today_date = datetime.now(TZ_US_EXCHANGE).date()

    df = pd.json_normalize([obj.model_dump() for obj in request.options_price])

    df["expiry"] = pd.to_datetime(df["expiry"], format="%Y%m%d")

    df["call_gex"] = df["call_gamma"] * df["call_oi"] * 100 * request.spot_price ** 2 * 0.01
    df["put_gex"] = df["put_gamma"] * df["put_oi"] * 100 * request.spot_price ** 2 * 0.01 * -1

    df["total_gex"] = (df["call_gex"] + df["put_gex"])

    price_levels = np.array(sorted(set(price_data.strike for price_data in request.options_price)))
    level_count = len(price_levels)

    # 0 DTE options, will have DTE = 1. Otherwise, they get excluded
    df["eq_years_till_expiry"] = np.max(
        [
            np.array([
                np.busday_count(today_date, expiry.date())
                for expiry in df["expiry"]
            ]),
            np.full(len(df["expiry"]), 1)
        ],
        axis=0,
    ) / 262

    total_gamma = []

    # For each spot level, calc gamma exposure at that point
    for (idx, level) in enumerate(price_levels, start=1):
        df["call_net_gamma"] = df.apply(
            lambda row: calc_net_gamma_at_price(
                level,
                row["strike"],
                row["call_iv"],
                row["eq_years_till_expiry"],
                "call",
                row["call_oi"]
            ),
            axis=1
        )

        df["put_net_gamma"] = df.apply(
            lambda row: calc_net_gamma_at_price(
                level,
                row["strike"],
                row["put_iv"],
                row["eq_years_till_expiry"],
                "put",
                row["put_oi"]
            ),
            axis=1
        )

        net_gamma = df["call_net_gamma"].sum() - df["put_net_gamma"].sum()
        LOGGER.info(
            f"Calculating net gamma of {level:>10.2f} ({idx:>4} / {level_count:>4} - {idx / level_count:>7.2%}): "
            f"${net_gamma:>23,.2f}"
        )
        total_gamma.append(net_gamma)

    total_gamma = np.array(total_gamma)

    return OptionsGexStatsResponse(
        gamma_field=calc_gamma_field(total_gamma, price_levels),
        gamma_flip=calc_gamma_flip(total_gamma, price_levels).tolist(),
    )
