from typing import Callable, List

from scipy.optimize import fsolve

from wiener_hopf.calculation.config.parameters import CONSTANTS


class NonlinearSolver:
    xmin = CONSTANTS["EQUATIONS"]["XMIN"]
    xmax = CONSTANTS["EQUATIONS"]["XMAX"]
    N = CONSTANTS["EQUATIONS"]["N"]

    @classmethod
    def solve(cls, function: Callable) -> List[float]:
        """
        Find all zeros of function using Rolle's theorem
        """
        dx = (cls.xmax - cls.xmin) / cls.N
        x2 = cls.xmin
        y2 = function(x2)
        roots = []
        for i in range(1, cls.N + 1):
            x1 = x2
            y1 = y2
            x2 = cls.xmin + i * dx
            y2 = function(x2)
            if y1 * y2 <= 0:
                roots = roots + list(fsolve(function, (x2 * y1 - x1 * y2) / (y1 - y2)))
        return list(set(roots))
