Anthropic
=========





This code implements a class called "AntropicLLM" that inherits from the "BaseLLM" class. 
This class uses the OpenAI Anthropic service to connect to a language model for generating text based on user queries.

The "utils" module is also used, importing the "get_from_dict_or_env" function from it.




- ``validate_environment`` : This method checks if the API key and the Anthropc module exist in the environment.

    .. autofunction:: llms.anthropic.AntropicLLM.validate_environment
        :no-index:



|



- ``get_model_names`` : This method returns the names of the available models.

    .. autofunction:: llms.anthropic.AntropicLLM.get_model_names
        :no-index:


|



- ``is_max_token`` : This method checks if the number of tokens in a query exceeds the maximum allowed token count for a model.

    .. autofunction:: llms.anthropic.AntropicLLM.is_max_token
        :no-index:


|



- ``parse_response`` : This method processes the response received from the model and returns the final text.

    .. autofunction:: llms.anthropic.AntropicLLM.parse_response
        :no-index:


|



- ``prepare_prompt`` : This method prepares the user's input text to be given as input to the model.

    .. autofunction:: llms.anthropic.AntropicLLM.prepare_prompt
        :no-index:


|



- ``generate`` : This method generates the text using the Anthropc model based on the query and other inputs provided. It takes the model name and the maximum required token count as inputs.

    .. autofunction:: llms.anthropic.AntropicLLM.generate
        :no-index:





