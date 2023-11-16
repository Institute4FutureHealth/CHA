Types
=====




Response Generator Types
------------------------




This code defines an enumeration (Enum) named ResponseGeneratorType. 
It inherits from the Enum class in Python's enum module. The purpose of this enumeration is to represent 
a type of response generator, and it has only one allowed value, which is a string with the value "base-generator."


.. literalinclude:: ../../../../response_generators/response_generator_types.py
    :language: python



|


Types
-----


This code creates a dictionary named RESPONSE_GENERATOR_TO_CLASS. 
Its purpose is to establish a mapping between response generator types (ResponseGeneratorType) and their corresponding 
response generator classes (BaseResponseGenerator).



.. literalinclude:: ../../../../response_generators/types.py
    :language: python



