class FourierTransform:
    transform_type: str = "forward"

    @classmethod
    def transform(cls):
        pass


class InverseFourierTransform(FourierTransform):
    transform_type: str = "inverse"


class Cauchy:
    pass
