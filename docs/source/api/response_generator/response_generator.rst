Response generators
===================




Base class for a response generator, providing a foundation for generating responses using a language model.


- ``generate`` : Generate response

    .. py:function:: generate(self, prefix: str = "", query: str = "", thinker: str = "", **kwargs: Any,)

        Generate a response based on the input prefix, query, and thinker.

        :param prefix: Prefix to be added to the response.
        :type prefix: str
        :param query: User's input query.
        :type query: str
        :param thinker: Thinker's generated answer.
        :type thinker: str
        :param kwargs: Additional keyword arguments.
        :type kwargs: Any
        :return: Generated response.
        :rtype: str




