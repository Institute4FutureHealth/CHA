Initialize datapipe
===================





- ``initialize_datapipe`` : This function that initializes and returns an instance of a data pipe class based on the specified 'datapipe' string and optional keyword arguments.


    .. py:function:: initialize_datapipe("memory")

        Initialize and return an instance of a data pipe based on the specified 'datapipe' type.

        :param datapipe: A string specifying the type of data pipe to initialize (default is "memory").
        :type datapipe: str , optional
        :param kwargs: Optional keyword arguments to be passed to the data pipe constructor.
        :type kwargs: Any
        :raise ValueError: If the specified 'datapipe' type is not valid, with a message listing valid types.
        :return: DataPipe: An instance of the selected data pipe class.
        :rtype: DataPipe






