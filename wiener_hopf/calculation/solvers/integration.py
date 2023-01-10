from scipy.integrate import quad

from wiener_hopf.calculation.config.parameters import CONSTANTS


class CauchyIntegral:
    end = CONSTANTS["INTEGRATION"]["END"] + CONSTANTS["INTEGRATION"]["EXTENSION"]

    @classmethod
    def compute(cls, function, k, singular=True):
        end = cls.end
        if function.analytic_expression:
            f = lambda x: function.analytic_expression(x)
        else:
            f = lambda x: function.spline(x)
        if singular:
            main_integral = quad(
                lambda x: f(x), -cls.end, cls.end, weight="cauchy", wvar=k
            )
        else:
            main_integral = quad(lambda x: f(x) / (x - k), -cls.end, cls.end)

        right_tail_integral = 1  # TODO: take into account asymptotics at infinity
        left_tail_integral = 1  # TODO: take into account asymptotics at infinity

        return main_integral + right_tail_integral + left_tail_integral

    @classmethod
    def compute_tail_integrals(cls, function):
        pass
