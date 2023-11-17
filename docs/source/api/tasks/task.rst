.. _task:

Task
====

This class defines a base class named BaseTask. This class serves as a foundation for defining common properties 
and behaviors among various tasks in the system.

.. autoclass:: tasks.task.BaseTask
    :members:
    :exclude-members: execute, parse_input, get_dict, explain, Config, model_config, model_fields

- ``execute``: An abstract method representing the execution of the task. Subclasses must implement this method.

    .. autofunction:: tasks.task.BaseTask.execute
        :no-index:


|



- ``parse_input`` : Parses the input string into a list of strings.

    .. autofunction:: tasks.task.BaseTask.execute
        :no-index:



|


- ``get_dict`` : Generates a dictionary-like representation of the task with details about its name, description, inputs, and dependencies.

    .. autofunction:: tasks.task.BaseTask.get_dict
        :no-index:


|


- ``explain`` : Provides a sample explanation for the task.

    .. autofunction:: tasks.task.BaseTask.explain
        :no-index:




