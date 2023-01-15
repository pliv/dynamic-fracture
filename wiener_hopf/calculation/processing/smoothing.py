from wiener_hopf.calculation.config.parameters import CONSTANTS
from typing import Callable

class Smoothener:
    end:float = CONSTANTS["INTEGRATION"]["END"]
    offset:float = CONSTANTS["INTEGRATION"]["EXTENSION"]

    @classmethod
    def smooth_out(cls,f_primary:Callable,f_secondary:Callable, positive_side:bool=True):
        near_end = cls.end-cls.offset
        far_end = cls.end+cls.offset
        if not positive_side:
            near_end = -near_end
            far_end = -far_end

        return lambda x: ((x-near_end)*f_secondary(x)-(x-far_end)*f_primary(x))/(far_end - near_end)
