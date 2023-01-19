from typing import Any, Dict, Optional

from wiener_hopf.calculation.config.asymptotic_fields import ASYMPTOTIC_FIELDS
from wiener_hopf.calculation.utils.custom_exceptions import AsymptoticFieldError


class Property:
    @staticmethod
    def get_asymptotics(coefs: Dict[str, Any]) -> Asymptotics:
        return Asymptotics(coefs)

    @staticmethod
    def set_singularity(point: float) -> Singularity:
        pass


class Asymptotics:
    def __init__(self, coefs: Dict[str, Any]):
        self.coefs = coefs

        if any([key not in ASYMPTOTIC_FIELDS for key in self.coefs]):
            raise AsymptoticFieldError

        def add_singularity(self):
            pass


class Singularity:
    def __init__(self,singularity_type:str):
        self.type:str = singularity_type
        self.analyticty: Optional[str] = None # plus or minus
