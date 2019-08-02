import pytest
import numpy as np
from collections import namedtuple


@pytest.fixture(scope="module")
def plt_data():
    # data for plotting
    PlottingData = namedtuple("plotting_data", ["uu", "data", "idx"])
    uu = np.linspace(0, np.pi, 128)
    data = np.cos(uu - 0.5) * np.cos(uu.reshape(-1, 1) - 1.0)
    return PlottingData(uu=uu, data=data, idx=data.shape[0] // 2)
