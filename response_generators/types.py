from typing import Dict, Type, Union

from response_generators.response_generator_types import ResponseGeneratorType
from response_generators.response_generator import BaseResponseGenerator


RESPONSE_GENERATOR_TO_CLASS: Dict[ResponseGeneratorType, Type[BaseResponseGenerator]] = {
  ResponseGeneratorType.BASE_GENERATOR: BaseResponseGenerator
}
