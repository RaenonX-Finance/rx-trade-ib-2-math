from typing import cast

import numpy as np
import numpy.typing as npt


def calc_gamma_field(
    total_gamma: npt.NDArray[np.float64],
    price_levels: npt.NDArray[np.float64],
) -> float | None:
    gamma_field_idx = np.argmin(total_gamma)

    min_net_gamma = np.min(total_gamma)

    # Min at the very left or the right, likely not a valid field
    if min_net_gamma == total_gamma[0] or min_net_gamma == total_gamma[len(total_gamma) - 1]:
        return None

    return cast(float, price_levels[gamma_field_idx])
