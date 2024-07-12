from typing import cast

import numpy as np
import numpy.typing as npt


def calc_gamma_flip(
    total_gamma: npt.NDArray[np.float64],
    price_levels: npt.NDArray[np.float64],
) -> float | None:
    gamma_flip_idx = np.where(np.diff(np.sign(total_gamma)))[0]

    if len(gamma_flip_idx) == 0:
        return None

    gamma_at_neg = total_gamma[gamma_flip_idx][0]
    gamma_at_pos = total_gamma[gamma_flip_idx + 1][0]
    strike_at_neg = price_levels[gamma_flip_idx][0]
    strike_at_pos = price_levels[gamma_flip_idx + 1][0]

    gamma_flip_price = strike_at_pos - ((strike_at_pos - strike_at_neg) * gamma_at_pos / (gamma_at_pos - gamma_at_neg))

    return cast(float, gamma_flip_price)
