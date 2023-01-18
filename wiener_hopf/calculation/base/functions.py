from typing import Any, Callable, Dict, List, Optional

import numpy as np

from wiener_hopf.calculation.config.parameters import CONSTANTS
from wiener_hopf.calculation.processing.interpolation import CubicSpline
from wiener_hopf.calculation.solvers.equation import NonlinearSolver
from wiener_hopf.calculation.utils.custom_exceptions import FalseZeroError


class Function:
    def __init__(
        self,
        array: Optional[List[Optional[float]]] = None,
        analytic_expression: Optional[Callable] = None,
        smoothing: Optional[Callable] = None,
        line_segment: Optional[np.array] = None,
        zeros: List[Optional[float]] = [],
        poles: List[Optional[float]] = [],
        compute_zeros: bool = False,
        smooth_ends: bool = False,
    ):
        self.array = array
        self.analytic_expression = analytic_expression
        self.x = line_segment
        self.zeros = zeros
        self.poles = poles
        self.asymptotics: Dict[str, Optional[Any]] = {}
        self.spline: Optional[CubicSpline] = None
        self.compute_zeros = compute_zeros
        self.zero_condition: Optional[bool] = None

        if self.analytic_expression and self.compute_zeros:
            self.zeros = self.get_zeros()

        if self.array:
            if not self.x:
                raise ValueError
            else:
                self.spline = CubicSpline(self.x, self.array)

    def get_zeros(self):
        zeros = NonlinearSolver.solve(lambda x: self.analytic_expression(x).real)
        self.zero_condition = all(
            [
                abs(self.analytic_expression(z)) <= CONSTANTS["ZERO_THRESHOLD"]
                for z in zeros
            ]
        )
        if not self.zero_condition:
            raise FalseZeroError
        return zeros

    def __call__(self, x: Optional[float], call_type: str = "analytic"):
        # TODO: add call types and raise error if invalide call type is given
        if call_type == "analytic":
            return self.analytic_expression(x)
        else:
            return self.spline(x)


class Kernel(Function):
    pass
