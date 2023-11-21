Response generators
===================

The **Response Generator** is an LLM-based module responsible for preparing the response. It refines the gathered information by the Task Planner, 
converting it into an understandable format and inferring the appropriate response. This module is trained to address `empathy` and `companionship` in conversations. 
Response generator also can use the gathered information to do the final inference to provide appropriate answer.
Notably, in some instances, the Task Planner and the Response Generator may share the same LLM.

.. toctree::
   :maxdepth: 1

   response_generator
   initialize_response_generator
   types