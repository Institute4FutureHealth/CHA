from typing import Dict
from typing import Type

from response_generators import (
    BaseResponseGenerator,
)
from response_generators import (
    ResponseGeneratorType,
)


RESPONSE_GENERATOR_TO_CLASS: Dict[
    ResponseGeneratorType, Type[BaseResponseGenerator]
] = {ResponseGeneratorType.BASE_GENERATOR: BaseResponseGenerator}
