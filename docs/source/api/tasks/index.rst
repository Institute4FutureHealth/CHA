.. _tasks:

Tasks
=====

Tasks are the external tools to facilitate **Planner** to answer users' query properly. Tasks can be data retrievals, internet search, machine learning algorithm,
translators, and so on.

The tasks can be implemented `locally` or `service-based`. **Locally** means you need to implement all needed codes locally to execute the task successfully (it can be provided as a python library, a github repository, or the full implementation be done in the task).
This is good practice because other contributers can see your codes and models so they can contribute to improve it, get ideas to implement new tasks, or learn how to use it properly
for their end applications. Including local codes can provide trust and help people adjust it based on their needs.

**Service-based** is a way that you have your services served on a server somewhere. Then you provide APIs to use your services. In this case, your task should
simply call the implemented APIs using python libraries like `requests` to call your APIs. It is your responsibility to maintain your task and provide proper documentation for
those who want to use your services (e.g., how to register to your service, if any api key is needed to be acquired, or any privacy and policy considerations).

To get started writing a new task, please take a look at the :ref:`task` documentation and implementation. Looking at existing implemented tasks can also
help understanding how to add new tasks.


.. toctree::
   :maxdepth: 1

   task
   initialize_task
   types
   affect/index
   ask_user
   google_translator
   serpapi
   read_from_datapipe
   playwright/index
