import numpy as np
import numpy.typing as npt

from rx_trade_ib_2.utils.average import get_windowed_average


def calc_gamma_flip(
    total_gamma: npt.NDArray[np.float64],
    price_levels: npt.NDArray[np.float64],
) -> list[float]:
    smoothed_total_gamma = get_windowed_average(total_gamma, 5)

    gamma_flip_idx = np.where(np.diff(np.sign(smoothed_total_gamma)))[0]

    if len(gamma_flip_idx) == 0:
        return []

    gamma_at_neg = smoothed_total_gamma[gamma_flip_idx][-1]
    gamma_at_pos = smoothed_total_gamma[gamma_flip_idx + 1][-1]
    strike_at_neg = price_levels[gamma_flip_idx][-1]
    strike_at_pos = price_levels[gamma_flip_idx + 1][-1]

    # Gamma curve tends to be going above/below 0 quite frequently after getting into negative territory,
    # therefore returning the last only

    return [float(strike_at_pos - ((strike_at_pos - strike_at_neg) * gamma_at_pos / (gamma_at_pos - gamma_at_neg)))]
