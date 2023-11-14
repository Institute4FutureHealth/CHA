Initialize task
===============





This code defines a function named initialize_task that is responsible for initializing a task based on the provided task name. 
It uses a dictionary named TASK_TO_CLASS to map task names to their corresponding task classes. 
The selected task class is then instantiated with the provided keyword arguments, and the resulting task instance is returned.


- ``initialize_task`` : Initializes a task based on the provided task name.

    .. py:function:: initialize_task(task: str = "serpapi", **kwargs: Any)

        Initialize a task based on the provided task name.

        :param task: The name of the task to initialize.
        :type task: str
        :param kwargs: Additional keyword arguments for customizing task initialization.
        :type kwargs: Any
        :return: An instance of the initialized task.
        :rtype: BaseTask
        :rise ValueError: If the provided task name is unknown.




