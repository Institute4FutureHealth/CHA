Interface
=========



This class uses the pydantic library as a base model.




- ``validate_environment method`` : This method is a model injection that runs before validating the model. This method checks whether the gradio library is installed in the environment or not. 
  If not, it throws a value error. Otherwise, it saves the value of gr in the model vocabulary.

   .. py:function:: validate_environment(cls, values: Dict)
      
      Validate that the API key and Python package exist in the environment.

      This function checks if the `gradio` Python package is installed in the environment. If the package is not found, it raises a `ValueError` with an appropriate error message.

      :param cls: The class to which this method belongs.
      :type cls: type
      :param values: A dictionary containing the environment values.
      :type values: Dict
      :return: The updated `values` dictionary with the `gradio` package imported.
      :rtype: Dict
      :rise ValueError: If the `gradio` package is not found in the environment.


|


- ``prepare_interface method`` : This method creates a user interface for a chatbot using the gradio library.

   .. py:function:: prepare_interface(self, respond, reset, available_tasks=[], share=False)

      Prepare the Gradio interface for the chatbot.

      This method sets up the Gradio interface for the chatbot. 
      It creates various UI components such as a textbox for user input, a checkbox for enabling/disabling chat history, a dropdown for selecting tasks, 
      and a clear button to reset the interface. The interface is then launched and stored in the `self.interface` attribute.

      :param self: The instance of the class.
      :type self: object
      :param respond: The function to handle user input and generate responses.
      :type respond: function
      :param reset: The function to reset the chatbot state.
      :type reset: function
      :param available_tasks: A list of available tasks. Defaults to an empty list.
      :type available_tasks: list, optional
      :param share: Flag indicating whether to enable sharing the interface. Defaults to False.
      :type share: bool, optional
      :return: None


|


- ``close method`` : This method closes the user interface and frees the related resources.

   .. py:function:: def close(self)

      Close the Gradio interface.

      This method closes the Gradio interface associated with the chatbot. 
      It calls the `close` method of the interface object stored in the `self.interface` attribute.

      :param self: The instance of the class.
      :type self: object
      :return: None



