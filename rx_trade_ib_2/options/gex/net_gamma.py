import numpy as np
from scipy.stats import norm

from rx_trade_ib_2.options.type import OptionType


# Black-Scholes European-Options Gamma
def calc_net_gamma_at_price(
    spot_price: float,
    strike: float,
    vol: float,
    eq_years_till_expiry: float,
    option_type: OptionType,
    open_interest: int
):
    if eq_years_till_expiry == 0 or vol == 0:
        return 0

    dp = (
            (np.log(spot_price / strike) + (0.5 * vol ** 2) * eq_years_till_expiry) /
            (vol * np.sqrt(eq_years_till_expiry))
    )
    dm = dp - vol * np.sqrt(eq_years_till_expiry)

    match option_type:
        case "call":
            gamma = norm.pdf(dp) / (spot_price * vol * np.sqrt(eq_years_till_expiry))
        case "put":
            # Gamma is same for calls and puts. This is just to cross-check
            gamma = strike * norm.pdf(dm) / (spot_price ** 2 * vol * np.sqrt(eq_years_till_expiry))
        case _:
            raise RuntimeError(f"Unknown option type: {option_type}")

    return open_interest * 100 * spot_price ** 2 * 0.01 * gamma
