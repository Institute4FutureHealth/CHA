How to Contribute
=================

We are immensely grateful for your enthusiasm in joining our open-source project, CHA (Conversational Health Agent).
Your contributions have the potential to be the driving force behind transformative healthcare applications,
ushering in a new era of innovation in healthcare research.

Whether you represent a healthcare research team seeking to harness the power of CHA for your unique applications or
you're an inspired developer ready to bring groundbreaking ideas to life, the avenues for involvement are diverse and filled with opportunities.
Together, we can shape the future of healthcare and make a lasting impact on the world of healthcare technology.
Your journey with CHA begins here, and the possibilities are boundless.

Getting Started
---------------

Familiarize Yourself with CHA:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before contributing, it's essential to understand the framework and its capabilities.
First of all we recommend you reading our `Paper <https://arxiv.org/abs/2310.02374>`_ or :ref:`introduction` section to get a high level idea of how it works and what are the main components.
Then we encourage you to take a look at our code base. We have provided a comprehensive documentation on all implemented parts in the :ref:`api` section.

Installation and Setup:
^^^^^^^^^^^^^^^^^^^^^^^^

For those without extensive development experience, we've designed CHA to be user-friendly. Most configurations are pre-set, making it easy to start using the framework.
Follow our :ref:`quick_start` guide to get up and running quickly. Also you can take a look at current :ref:`examples` to get ideas on how to start your journey.


Contribution Opportunities
--------------------------

Healthcare Specialists and Research Teams:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Healthcare specialists and research teams have the opportunity to enhance CHA by effortlessly introducing new :ref:`tasks` or creating unique :ref:`examples` by combining existing tasks.
We've streamlined this process by offering clear instructions and, in numerous instances, requiring the implementation of just a single function.
Your contributions will significantly bolster healthcare applications with minimal effort on your part.

Inspired Developers and Researchers:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For visionary developers and researchers, CHA is a boundless realm of opportunities.
Our framework features fully customizable components, inviting you to explore, experiment, and amplify CHA's potential.

In the ever-evolving landscape of healthcare technology, we thrive at the forefront, where creativity and innovation are the cornerstones of our journey.
Beyond contributing, you'll find a multitude of research avenues awaiting your exploration, paving the way for groundbreaking advancements in healthcare.
Join us in shaping the future of healthcare technology, where your ingenuity is the catalyst for success.

Research and Development Ideas
------------------------------

There are many research and development tracks that we have in mind that may give you some ideas:

**Powerful Thinkers**:

Exploration of novel Task Planners lies at the core of our endeavor. These Task Planners serve as the cognitive hub of CHAs,
aimed to comprehend user queries and orchestrate the optimal sequence of tasks to deliver personalized responses. The art of task selection holds paramount significance in our pursuit.

**Empathy**:

Empathy stands as a pivotal element within the realm of forthcoming healthcare technologies, enriching user engagement and fostering trust when interacting with CHAs. A promising avenue
for research involves the integration of novel Result Generators, with the aim of delivering personalized outcomes in a genuinely empathetic manner.
This represents a crucial frontier in our quest to enhance the healthcare experience.

**Better Prompting**:

As we progress, the significance of prompts becomes increasingly pivotal in shaping the future of interactions with Large Language Models (LLMs).
Numerous research studies have affirmed that well-crafted prompts can substantially enhance the reliability and accuracy of LLM responses,
all while ensuring adherence to specific guidelines and instructions.

Consider, for instance, the scenario where user health data is collected for crafting the final response.
Here, the proper interpretation of this data, along with its seamless incorporation or referencing as needed, can significantly enrich the information provided to the user.
Transforming user inquiries into refined prompts destined for the Task Planner, shaping user-collected data into apt prompts,
and infusing prompts with empathy-inducing qualities are but a few instances of research pathways within the realm of Promptist investigations.

**Explore New Applications**:

The realm of application-specific research holds great promise as the next exhilarating frontier in research and development.
Within our CHA framework, it bears early fruit by either introducing fresh tasks or utilizing existing ones to address prevalent healthcare challenges.

For instance, one practical application involves enabling users to engage in simple reference-based question answering for health-related queries.
Leveraging the power of Google Search tasks (such as SERPAPI), CHA can scour the internet to pinpoint highly regarded websites housing the desired answers.
If necessary, utilizing the Playwright extract_text task, CHA can extract text from webpages, ensuring the delivery of reliable responses.
Furthermore, CHA can present users with the webpage link for further exploration.

In more intricate scenarios, researchers can implement a CT image classifier, adept at identifying tumors, and seamlessly integrate it with CHA to craft an
interactive medical image reporting system. These examples underscore the immense potential for innovation and problem-solving within the healthcare landscape
using our framework.

**Your New Idea**:

It is important to note that these are some general ideas and the sky is unlimited. We fully encourage and support new ideas and we are willing
to help and contribute in new ideas. You can contact us by email to setup meetings so that we can discuss new ideas.


Documentation and Citation
--------------------------

To maintain the trustworthiness and reliability of CHA, it's vital to keep everything well-documented and properly cited.
We encourage all contributors to:

- Document their code thoroughly, making it easy for others to understand and use.

- Cite any papers or repositories they integrate into CHA within the documentation. This sharing of knowledge ensures transparency and fosters trust within the healthcare community.

- Continuously update and improve the documentation to reflect the latest changes and enhancements.

Join Our Community
------------------

We believe in the power of collaboration. Join our community of developers, researchers, and healthcare specialists to exchange ideas, share experiences, and collectively work towards a brighter future in healthcare.

By contributing to CHA, you're not only making healthcare applications more accessible and innovative but also becoming part of a dynamic and forward-thinking community.
Together, we can shape the future of healthcare technology.



Start Contributing
------------------

To implement the CHA in a safe and stable way make sure you have python3.10 and higher. First create a virtual env.

.. code-block:: python

  #create the venv
  python -m venv /path/to/new/virtual/environment
  #activate the venv
  source activate /path/to/new/virtual/environment/bin

Now install the CHA packages for development:

.. code-block:: bash

  pip install 'CHA[develop]'

This will install all needed dependencies for development which includes `sphinx` for documentaiont, `pytest` for managing tests, and
`pre-commit` to ensure coding style integrity.

For detailed documentation of the codes and guidelines on how to implement new codes, go to :ref:`api` page.
For your new codes, please create a new branch from development branch. Follow best practices on writing clean codes. We provided a pre-commit
that cleans your code and makes it unified in style with other codebase. Before each commit you should run the following command:

.. code-block:: bash

  pre-commit run --all-files

This command will change your code styles. In many cases the command will fix the style issues. But there might be cases that needs you to
fix the code manually. You should make sure this command returs passed or skipped for all the lines and no Failed. Then you can go ahead and commit and push
your codes.

.. code-block:: bash

  git add -A
  git commit -m "your message"
  git push origin your_branch_name


How To Document
^^^^^^^^^^^^^^^

We are using sphinx for document generation. For each new file you are making, you are required to create the same file inside the docs (under exact same folders)
with rst extention. In the docs in most cases you just need to write the following text:

.. code-block:: RST

  Your Page Headline
  ==================

  .. autoclass:: address.to.your.code.block

You can look at docs/source/api/tasks/task.rst for example.

After adding your file, you need to add it to the index.rst of the containing folder or the upper folder under the toctree annotation.
This way the sphinx will index your file. Now you just need to start documenting your code on your python file. You can look at the tasks/task.py
for sample documentation. We have two types of documentation: class documentaion and function documentation.

The class documentation have the following format:

.. code-block:: python

  """
    **Description:**

      Put your description here

    Attributes:
      attribute1: description of the attribute1
      attribute2: description of the attribute2

  """

For each class, we have a class description and attribute descriptions. Class description in which you provide the general information regarding you class
, you can provide links to your github repos or papers. Attribute descriptions contains explanation for each attribute you have. make sure the spacing and
tabs are the same as the example, otherwise the documentation may be miscompiled.

For the function documentation we have the following format:

.. code-block:: python

  """
    Description for the function and how you are implementing it.

  Args:
    arg1 (type): arg1 description.
  Return:
    return_type: explanation for the return value.
  Raise:
    NotImplementedError: Subclasses must implement the execute method.

  """

For each function, you need to put the doc at the first line of the function so that the sphinx will compile them into proper documentation.

After you finished writing down your documentations, run the following commands:

.. code-block:: bash

  #direct to the docs folder
  cd docs
  #compile the files
  make html

After the docs are compiled, you will see successful compilation. You should be able to see a build folder inside the docs folder after compiling.
You can open the docs/build/html/index.html in your browser to see the final version and check if your document is showing properly.

Tests Are Required
^^^^^^^^^^^^^^^^^^^

Unit tests are a must for every code you write. Especially when it comes to tasks, you should add task test for all the functions you are implementing.
This will help you test your tasks apart from the whole framework to make sure that when correct inputs are provided, your tasks will work properly.
The tests are located under tests folder under the respective subfolder. Create a python test file with proper name. Then start writing your tests.
Your tests should try to test all different cases for your tasks especially edge cases. Like if no input is provided, or the input type is wrong.
Try to throughly test your task to reduce the risk of errors when others start using your task in their applications. We are using pytest for testing
the codes.

Before each pull request, you should make sure all tests will pass otherwise your pull request will be rejected. To run all the tests, you can use
the following command:

.. code-block:: bash

  #Make sure you are in the CHA folder and the tests folder is there
  pytest tests

So as a summary, the final steps for pushing your code will be something like following:

.. code-block:: bash

  pre-commit run --all-files
  pytest tests
  git add -A
  git commit -m "your message"
  git push origin your_branch_name

After pushing into your branch, and you are sure that you did everything right, please go ahead and do a pull request. Try to write some
explanation on what you code do, this will help us understand your code and approve your changes faster.
