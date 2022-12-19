from typing import Dict
from numpy import ndarray, array, sin, sqrt, absolute, inf
from aiaccel.util import aiaccel


def main(p: Dict) -> float:
    """The Schwefel function of 5 dimensions with global minimum of 0 at x =
    4.209687.

    Args:
        p (Dict[str, float]): A parameter dictionary.

    Returns:
        float: Calculated objective value.
    """
    x: ndarray = array(list(p.values()))
    if (absolute(x) > 5).any():
        return inf
    y0 = array([0.0, 0.0, 0.0, 0.0, 0.0])
    y = 100 * x - y0
    f: float = 2094.9144363621604 + (-y * sin(sqrt(absolute(y)))).sum()
    return f * 0.001834960061484341


if __name__ == "__main__":
    run = aiaccel.Run()
    run.execute_and_report(main)
