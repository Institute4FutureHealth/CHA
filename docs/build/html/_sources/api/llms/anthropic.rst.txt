Anthropic
=========





This code implements a class called "AntropicLLM" that inherits from the "BaseLLM" class. 
This class uses the OpenAI Anthropic service to connect to a language model for generating text based on user queries.

The "utils" module is also used, importing the "get_from_dict_or_env" function from it.




- ``validate_environment`` : This method checks if the API key and the Anthropc module exist in the environment.

    .. py:function:: validate_environment(cls, values: Dict)

        Validate that the API key and required Python package exist in the environment.

        This method validates the environment by checking the existence of the API key and required Python packages. 
        It retrieves the API key from either the "anthropic_api_key" key in the "values" dictionary or from the "ANTHROPIC_API_KEY" environment variable. 
        It also imports the required packages and assigns the appropriate values to the class attributes.

        :param cls: The class itself.
        :type cls: type
        :param values: The dictionary containing the values for validation.
        :type value: Dict
        :return: The validated dictionary with updated values.
        :rtype: Dict
        :rise ValueError: If the anthropic python package cannot be imported.



|



- ``get_model_names`` : This method returns the names of the available models.

    .. py:function:: get_model_names(self)

        Get a list of available model names.

        :return: A list of available model names.
        :rtype: List[str]


|



- ``is_max_token`` : This method checks if the number of tokens in a query exceeds the maximum allowed token count for a model.

    .. py:function:: is_max_token(self, model_name, query)

        Check if the token count of the query exceeds the maximum token count for the specified model.

        :param model_name: The name of the model.
        :type model_name: str
        :param query: The query to check.
        :type query: str
        :return: True if the token count exceeds the maximum, False otherwise.
        :rtype: bool


|



- ``parse_response`` : This method processes the response received from the model and returns the final text.

    .. py:function:: parse_response(self, response)

        Parse the response object and return the generated completion text.

        :param response: The response object.
        :type response: object
        :return: The generated completion text.
        :rtype: str


|



- ``prepare_prompt`` : This method prepares the user's input text to be given as input to the model.

    .. py:function:: prepare_prompt(self, prompt)

        Prepare the prompt by combining the human and AI prompts with the input prompt.

        :param prompt: The input prompt.
        :type prompt: str
        :return: The prepared prompt.
        :rtype: Any


|



- ``generate`` : This method generates the text using the Anthropc model based on the query and other inputs provided. It takes the model name and the maximum required token count as inputs.

    .. py:function:: generate(self, query: str, **kwargs: Any)

        Generate a response based on the provided query.

        :param query: The query to generate a response for.
        :type query: str
        :param **kwargs: Additional keyword arguments.
        :type **kwargs: Any
        :return: The generated response.
        :rtype: str
        :rise ValueError: If the model name is not specified or is not supported.





