from pathlib import Path

import pytest
from cvrp_metaheuristics.utils.file_utils import read_problem


# 0.00  21.00  58.14  17.49  33.24  48.83
# 21.00   0.00  37.22  19.21  45.28  40.61
# 58.14  37.22   0.00  52.55  75.03  46.86
# 17.49  19.21  52.55   0.00  50.57  58.19
# 33.24  45.28  75.03  50.57   0.00  41.00
# 48.83  40.61  46.86  58.19  41.00   0.00

@pytest.fixture
def cvrp():
    cvrp = read_problem(Path(__file__).resolve().parent / "resources/toy.vrp")
    return cvrp
