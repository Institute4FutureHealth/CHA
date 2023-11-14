DataPipes
=========



This class serves as a basis for creating an interface class used in projects that require data storage and retrieval.




    
- ``store`` : To store data in the system, you can use this function.

    .. autofunction:: datapipes.datapipe.DataPipe.store
        :no-index:


|


- ``retrieve`` : To retrieve data based on a specified key, you can use this function:

    .. py:function:: retrieve(key)

        Retrieve data based on a specified key.

        :param key: The key to identify the data.
        :type key: Any
        :return: The retrieved data.
        :rtype: Any

