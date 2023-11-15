LLMs
====




BaseLLM class sets up a base Pydantic model class with an abstract method generate, which must be implemented by any subclass. 
The BaseModel class provides data validation and parsing functionality, and it can be extended to create more specific models with their own data validation rules.



- ``generate`` : Generate a response based on the provided query.

    .. autofunction:: llms.llm.BaseLLM.generate
        :no-index:















   