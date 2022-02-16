from simuPark.park import Park
import numpy as np
from math import gamma

fn = lambda x, k: (np.power(x + 30 / 60, k - 1) * np.exp(-x - 30 / 60) / gamma(k))

park: Park = Park(
    hoursOpen=1,
    function=fn,
)

park.startDayBase(100000)
