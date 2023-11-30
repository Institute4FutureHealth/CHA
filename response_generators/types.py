from typing import Dict
from typing import Type

from response_generators.response_generator import (
    BaseResponseGenerator,
)
from response_generators.response_generator_types import (
    ResponseGeneratorType,
)


RESPONSE_GENERATOR_TO_CLASS: Dict[
    ResponseGeneratorType, Type[BaseResponseGenerator]
] = {ResponseGeneratorType.BASE_GENERATOR: BaseResponseGenerator}
