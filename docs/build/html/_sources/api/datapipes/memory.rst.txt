Memory
======




This class inherits from DataPipe and provides methods to store and retrieve data using unique keys.



- ``store`` : To store data in the system, you can use this function.
    
    .. py:function:: store(self, data)

        Store data using a generated key and return the key.

        This method stores the provided data in the chatbot's data dictionary using a generated key. 
        The generated key is a UUID (Universally Unique Identifier). The stored data can later be accessed using this key.

        :param self: The instance of the class.
        :type self: object
        :param data: The data to be stored.
        :type data: Any
        :return: The generated key associated with the stored data.
        :rtype: str


|


- ``retrieve`` : To retrieve data based on a specified key, you can use this function.

    .. py:function:: retrieve(self, key)

        Retrieve data associated with the given key.

        This method retrieves the data associated with the provided key from the chatbot's data dictionary. 
        If the key does not exist in the dictionary, it raises a `ValueError` with an appropriate error message.

        :param self: The instance of the class.
        :type self: object
        :param key: The key associated with the data to be retrieved.
        :type key: str
        :return: The data associated with the provided key.
        :rtype: Any
        :rise ValueError: If the key does not exist in the data dictionary.








