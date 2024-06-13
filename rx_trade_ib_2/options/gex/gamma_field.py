from typing import cast

import numpy as np
import numpy.typing as npt


def calc_gamma_field(
    total_gamma: npt.NDArray[np.float64],
    price_levels: npt.NDArray[np.float64],
) -> float | None:
    gamma_field_idx = np.argmin(total_gamma)

    if np.min(total_gamma) == total_gamma[0]:
        return None

    return cast(float, price_levels[gamma_field_idx])
