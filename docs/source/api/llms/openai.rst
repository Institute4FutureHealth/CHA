Open AI
=======






This code defines a class called "OpenAILLM" that inherits from the "BaseLLM" base class and provides specific functionalities for an LLM related to OpenAI.



- ``validate_environment`` : Validate that the API key and required Python package exist in the environment.

    .. autofunction:: llms.openai.OpenAILLM.validate_environment
        :no-index:


|


- ``get_model_names`` : This method returns a list of the available model names in OpenAILLM.

    .. autofunction:: llms.openai.OpenAILLM.get_model_names
        :no-index:


|


- ``is_max_token`` : This method checks if the number of tokens in the model exceeds the maximum limit. 

    .. autofunction:: llms.openai.OpenAILLM.is_max_token
        :no-index:


|



- ``parse_response`` : This method parses the received response from the model and returns the content of the first message.

    .. autofunction:: llms.openai.OpenAILLM.parse_response
        :no-index:



|



- ``prepare_prompt`` : This method prepares the input text in a suitable format for sending to the model. 

    .. autofunction:: llms.openai.OpenAILLM.prepare_prompt
        :no-index:



|



- ``generate`` : This method is used to generate output from the model. It first determines the desired model name and continues if it exists in the list of available models.

    .. autofunction:: llms.openai.OpenAILLM.generate
        :no-index:





