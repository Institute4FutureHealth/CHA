Open AI
=======






This code defines a class called "OpenAILLM" that inherits from the "BaseLLM" base class and provides specific functionalities for an LLM related to OpenAI.



- ``validate_environment`` : Validate that the API key and required Python package exist in the environment.

    .. py:function:: validate_environment(cls, values: Dict)

        This method is defined as a validation model for the class and checks the required environment values for using OpenAILLM. 
        If the "openai_api_key" key exists in the input, its value is assigned to the "api_key" variable. Additionally, it checks the existence of the openai library, and if it's not found, it raises an error.

        :param cls: The class itself.
        :type cls: type
        :param values: The dictionary containing the values for validation.
        :type value: Dict
        :return: The validated dictionary with updated values.
        :rtype: Dict
        :rise ValueError: If the anthropic python package cannot be imported.


|


- ``get_model_names`` : This method returns a list of the available model names in OpenAILLM.

    .. py:function:: get_model_names(self)

        Get a list of available model names.

        :return: A list of available model names.
        :rtype: List[str]


|


- ``is_max_token`` : This method checks if the number of tokens in the model exceeds the maximum limit. 

    .. py:function:: is_max_token(self, model_name, query)

        Check if the token count of the query exceeds the maximum token count for the specified model.

        It calculates the number of tokens from tokenizing the input query and compares it with the maximum allowed tokens for the model. 
        If the number of tokens is greater than the maximum, it returns True.

        :param model_name: The name of the model.
        :type model_name: str
        :param query: The query to check.
        :type query: str
        :return: True if the token count exceeds the maximum, False otherwise.
        :rtype: bool


|



- ``parse_response`` : This method parses the received response from the model and returns the content of the first message.

    .. py:function:: parse_response(self, response)

        Parse the response object and return the generated completion text.

        :param response: The response object.
        :type response: object
        :return: The generated completion text.
        :rtype: str



|



- ``prepare_prompt`` : This method prepares the input text in a suitable format for sending to the model. 

    .. py:function:: prepare_prompt(self, prompt)

        Prepare the prompt by combining the human and AI prompts with the input prompt.

        :param prompt: The input prompt.
        :type prompt: str
        :return: The prepared prompt.
        :rtype: Any



|



- ``generate`` : This method is used to generate output from the model. It first determines the desired model name and continues if it exists in the list of available models.

    .. py:function:: generate(self, query: str, **kwargs: Any)

        Generate a response based on the provided query.

        :param query: The query to generate a response for.
        :type query: str
        :param **kwargs: Additional keyword arguments.
        :type **kwargs: Any
        :return: The generated response.
        :rtype: str
        :rise ValueError: If the model name is not specified or is not supported.





