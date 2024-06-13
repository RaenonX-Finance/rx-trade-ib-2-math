from datetime import UTC, datetime

import numpy as np
import pandas as pd

from rx_trade_ib_2.options.gex.gamma_field import calc_gamma_field
from rx_trade_ib_2.options.gex.gamma_flip import calc_gamma_flip
from rx_trade_ib_2.options.gex.request import OptionsGexStatsRequest
from rx_trade_ib_2.options.gex.response import OptionsGexStatsResponse
from rx_trade_ib_2.options.model import calc_net_gamma_at_price


def calc_gex_stats(request: OptionsGexStatsRequest) -> OptionsGexStatsResponse:
    today_date = datetime.now(UTC).date()

    df = pd.json_normalize([obj.dict() for obj in request.options_price])

    df["expiry"] = pd.to_datetime(df["expiry"], format="%Y%m%d")

    df["call_gex"] = df["call_gamma"] * df["call_oi"] * 100 * request.spot_price ** 2 * 0.01
    df["put_gex"] = df["put_gamma"] * df["put_oi"] * 100 * request.spot_price ** 2 * 0.01 * -1

    df["total_gex"] = (df["call_gex"] + df["put_gex"])

    price_levels = np.linspace(request.strike_min, request.strike_max, 60)

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
    for level in price_levels:
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

        total_gamma.append(df["call_net_gamma"].sum() - df["put_net_gamma"].sum())

    total_gamma = np.array(total_gamma)

    return OptionsGexStatsResponse(
        gamma_field=calc_gamma_field(total_gamma, price_levels),
        gamma_flip=calc_gamma_flip(total_gamma, price_levels),
    )
