from typing import Any, Callable, Dict, List, Optional

import numpy as np

from wiener_hopf.calculation.processing.interpolation import CubicSpline
from wiener_hopf.calculation.solvers.equation import NonlinearSolver


class Function:
    def __init__(
        self,
        array: Optional[List[Optional[float]]] = None,
        analytic_expression: Optional[Callable] = None,
        line_segment: Optional[np.array] = None,
        zeros: List[Optional[float]] = [],
        poles: List[Optional[float]] = [],
        compute_zeros: bool = False,
    ):
        self.array = array
        self.analytic_expression = analytic_expression
        self.x = line_segment
        self.zeros = zeros
        self.poles = poles
        self.asymptotics: Dict[str, Optional[Any]] = {}
        self.spline: Optional[CubicSpline] = None
        self.compute_zeros = compute_zeros

        if self.analytic_expression and self.compute_zeros:
            self.zeros = self.get_zeros()

        if self.array:
            if not self.x:
                raise ValueError
            else:
                self.spline = CubicSpline(self.x, self.array)

    def get_zeros(self):
        return NonlinearSolver.solve(self.analytic_expression)


class Kernel(Function):
    pass
