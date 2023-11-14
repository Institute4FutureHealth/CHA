Types
=====




Response Generator Types
------------------------




This code defines an enumeration (Enum) named ResponseGeneratorType. 
It inherits from the Enum class in Python's enum module. The purpose of this enumeration is to represent 
a type of response generator, and it has only one allowed value, which is a string with the value "base-generator."


.. code:: python

    from enum import Enum 

    class ResponseGeneratorType(str, Enum):
    BASE_GENERATOR = "base-generator"



|


Types
-----


This code creates a dictionary named RESPONSE_GENERATOR_TO_CLASS. 
Its purpose is to establish a mapping between response generator types (ResponseGeneratorType) and their corresponding 
response generator classes (BaseResponseGenerator).



.. code:: python

    from typing import Dict, Type, Union

    from response_generators.response_generator_types import ResponseGeneratorType
    from response_generators.response_generator import BaseResponseGenerator


    RESPONSE_GENERATOR_TO_CLASS: Dict[ResponseGeneratorType, Type[BaseResponseGenerator]] = {
    ResponseGeneratorType.BASE_GENERATOR: BaseResponseGenerator
    }



