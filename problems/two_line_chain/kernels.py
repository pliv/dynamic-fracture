import math
from typing import Optional, Union

from wiener_hopf.calculation.base.functions import Function, Kernel
from wiener_hopf.calculation.config.parameters import CONSTANTS


class TwoLineChain:
    def __init__(self, alpha: float, beta: float):
        self.alpha = alpha
        self.beta = beta

        self.kernel_functions: Dict[str, Union[Dict[str, Function], Function]] = {
            "quadratic_term": Function(
                analytic_expression=lambda x: (CONSTANTS["EPSILON"] - 1j * beta * x)
                ** 2
            ),
            "phi_S": {
                "squared": Function(
                    analytic_expression=lambda x: 4 * math.sin(x / 2) ** 2
                ),
                "derivative": Function(analytic_expression=lambda x: math.cos(x / 2)),
            },
            "phi_D": {
                "squared": Function(
                    analytic_expression=lambda x: 4 * math.cos(x / 2) ** 2
                ),
                "derivative": Function(analytic_expression=lambda x: -math.sin(x / 2)),
            },
            "psi_S": {
                "squared": Function(
                    analytic_expression=lambda x: 2 * (alpha + 2 * math.sin(x / 2) ** 2)
                ),
                "derivative": Function(
                    analytic_expression=lambda x: math.sin(x)
                    / math.sqrt(self.kernel_functions["psi_S"]["squared"](x))
                ),
            },
            "psi_D": {
                "squared": Function(
                    analytic_expression=lambda x: 2 * (alpha + 2 * math.cos(x / 2) ** 2)
                ),
                "derivative": Function(
                    analytic_expression=lambda x: -math.sin(x)
                    / math.sqrt(self.kernel_functions["psi_D"]["squared"](x))
                ),
            },
        }

        self.kernel_functions.update(
            {
                "L_S": {
                    "numerator": Function(
                        analytic_expression=lambda x: self.kernel_functions[
                            "quadratic_term"
                        ](x)
                        + self.kernel_functions["phi_S"]["squared"](x),
                        compute_zeros=True,
                    ),
                    "denominator": Function(
                        analytic_expression=lambda x: self.kernel_functions[
                            "quadratic_term"
                        ](x)
                        + self.kernel_functions["psi_S"]["squared"](x),
                        compute_zeros=True,
                    ),
                },
                "L_D": {
                    "numerator": Function(
                        analytic_expression=lambda x: self.kernel_functions[
                            "quadratic_term"
                        ](x)
                        + self.kernel_functions["phi_D"]["squared"](x),
                        compute_zeros=True,
                    ),
                    "denominator": Function(
                        analytic_expression=lambda x: self.kernel_functions[
                            "quadratic_term"
                        ](x)
                        + self.kernel_functions["psi_D"]["squared"](x),
                        compute_zeros=True,
                    ),
                },
            }
        )

        self.kernel_functions["L_S"]["function"] = self.set_kernel_function(
            kernel_name="L_S"
        )
        self.kernel_functions["L_D"]["function"] = self.set_kernel_function(
            kernel_name="L_D"
        )

    def set_kernel_function(self, kernel_name):
        return Function(
            analytic_expression=lambda x: self.kernel_functions[kernel_name][
                "numerator"
            ](x)
            / self.kernel_functions[kernel_name]["denominator"](x),
            zeros=self.kernel_functions[kernel_name]["numerator"].zeros,
            poles=self.kernel_functions[kernel_name]["denominator"].zeros,
        )
