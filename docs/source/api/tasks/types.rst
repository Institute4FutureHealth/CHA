Types
=====




Tasks Types
-----------




This code defines an enumeration class named TaskType using the Enum module in Python. 
Enums are a way to create named constant values that represent distinct elements. 




.. literalinclude:: ../../../../tasks/task_types.py
    :language: python



|


Types
-----


This code defines a dictionary named TASK_TO_CLASS, which maps instances of the TaskType enumeration to 
corresponding classes that inherit from BaseTask. The purpose of this dictionary is to provide a convenient way to 
instantiate specific task classes based on their associated TaskType.




.. literalinclude:: ../../../../tasks/types.py
    :language: python



