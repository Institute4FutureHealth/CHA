Quick Start
============

To use the CHA in a safe and stable way make sure you have python3.10 and higher. First create a virtual env.

.. code-block:: python

  #create the venv
  python -m venv /path/to/new/virtual/environment
  #activate the venv
  source activate /path/to/new/virtual/environment/bin

Now install the CHA package:

This command only installs the based requirements and later you need to install different packages needed based on tasks, planner, response generator, and llm types you want to use

.. code-block:: bash  
  
  pip install CHA

To make it easier, you can use the following command to install the minimum requirments and ready to go. This will \
install openai, react planner, as well as serpapi (search), and playwright (browser) tasks.

.. code-block:: bash  
  
  pip install 'CHA[minimum]'
  
If you want to install all requirements for all tasks and other components, use the following command:

.. code-block:: bash  
  
  pip install 'CHA[all]'

After installing the package, you can start running our framework with simple code:

.. code-block:: python

  from CHA import CHA

  cha = CHA()
  cha.run_with_interface()

This code will run the default interface. You can route to the following url: 

**http://127.0.0.1:7860**

For more examples go to the Examples page: :ref:`examples`

.. figure:: ../../figs/Interface.png
    :alt: Alt Text
    :align: center

