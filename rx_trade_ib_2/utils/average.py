import numpy as np
import numpy.typing as npt


def get_windowed_average(data: npt.NDArray[np.float64], period: int) -> npt.NDArray[np.float64]:
    # `mode` of `valid` makes it moving average
    return np.convolve(data, np.ones(period) / period, mode="same")
