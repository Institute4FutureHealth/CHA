Interface
=========



This class uses the pydantic library as a base model.




- ``validate_environment`` : This method is a model injection that runs before validating the model. This method checks whether the gradio library is installed in the environment or not.
  If not, it throws a value error. Otherwise, it saves the value of gr in the model vocabulary.

   .. autofunction:: interface.base.Interface.validate_environment
        :no-index:


|


- ``prepare_interface`` : This method creates a user interface for a chatbot using the gradio library.

   .. autofunction:: interface.base.Interface.prepare_interface
        :no-index:


|


- ``close`` : This method closes the user interface and frees the related resources.

   .. autofunction:: interface.base.Interface.close
        :no-index:



