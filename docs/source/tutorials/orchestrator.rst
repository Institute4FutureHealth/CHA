.. _orchestrator:

Example of a sample Orchestrator execution flow in the openCHA Framework
=========================================================================

In this tutorial, we demonstrate the generated prompt for a simple example involving two tasks: Internet search and webpage information extraction. The user's query, "How to improve my sleep," is directed to the Task Planner, and through various stages, it is transformed into executable tasks by the Task Executor.

Initial Planning Stage
----------------------

The initial planning stage involves the Tree of Thought Planner developing strategies to address the query. The prompt structure and its evaluation are as follows:

.. table:: Tree of Thought Planning first planning stage.
   :class: special-table
   :widths: auto
   :name: tab:planner_prompt1

   +----------------------------------------------------------------------------------------------------------+
   | As a knowledgeable and empathetic health assistant, your primary objective is to provide the user with   |
   | precise and valuable information regarding their health and well-being. Utilize the available tools      |
   | effectively to answer health-related queries. Here are the tools at your disposal:                       |
   |                                                                                                          |
   | **google_search**:                                                                                       |
   | Uses google to search the internet for the requested query and returns the url of the top website.       |
   | This tool have the following outputs:                                                                    |
   | It returns a json object containing key: **url**. For example: {'url': 'http://google.com'}              |
   |                                                                                                          |
   | **extract_text**: Extract all the text on the current webpage                                            |
   | This tool have the following outputs:                                                                    |
   | An string containing the text of the scraped webpage.                                                    |
   |                                                                                                          |
   | MetaData: This contains the names of data files of different types, such as images, audio, video,        |
   | and text. You can pass these files to tools when needed.                                                 |
   |                                                                                                          |
   | History: The history of previous chats happened. Review the history of any previous responses relevant   |
   | to the current query.                                                                                    |
   |                                                                                                          |
   | PreviousActions: the list of actions that have already been performed. You should start planning,        |
   | knowing that these actions are performed.                                                                |
   |                                                                                                          |
   | Question: The input question that you must answer.                                                       |
   |                                                                                                          |
   | Considering previously actions and their results, use the tools and provided information, first suggest  |
   | three creative strategies with detailed explanation consisting of sequences of tools to properly answer  |
   | the user query. Make sure the strategies are comprehensive enough and use proper tools. The tools        |
   | constraints should be always satisfied. After specifying the strategies, mention the pros and cons of    |
   | each strategy. In the end, decide the best strategy and write the detailed tool executions step by step. |
   | start your final decision with 'Decision:'.                                                              |
   |                                                                                                          |
   | Begin!                                                                                                   |
   |                                                                                                          |
   | USER: How to improve my sleep?                                                                           |
   +----------------------------------------------------------------------------------------------------------+

Second Planning Stage: Code Generation
--------------------------------------

The second stage of planning where the LLM is instructed to generate Python code that the Orchestrator can execute based on the chosen strategy, along with the necessary inputs.

.. table:: Tree of Thought Planning second planning stage: generating the task execution code part 1.
   :class: special-table
   :widths: auto
   :name: tab:planner_prompt2

   +----------------------------------------------------------------------------------------------------------+
   | Decision:                                                                                                |
   |                                                                                                          |
   | I will go with Strategy 1 as it provides the most recent and relevant information available on the       |
   | internet, which is crucial for improving sleep.                                                          |
   |                                                                                                          |
   | Now, let's proceed with the detailed tool executions for Strategy 1:                                     |
   |                                                                                                          |
   | 1. Use the "google_search" tool to find the top websites with tips to improve sleep.                     |
   |                                                                                                          |
   | 2. Once we have the top website, we can use the "extract_text" tool to extract the relevant information  |
   | about improving sleep from the webpage.                                                                  |
   |                                                                                                          |
   | Let's start with step 1.                                                                                 |
   |                                                                                                          |
   | Tools:                                                                                                   |
   |                                                                                                          |
   | **google_search**: Uses google to search the internet for the requested query and returns the url of the |
   | top website.                                                                                             |
   |                                                                                                          |
   | The input to this tool should be a list of data representing:                                            |
   |                                                                                                          |
   | 1-It should be a search query.                                                                           |
   |                                                                                                          |
   | This tool will return the following data:                                                                |
   |                                                                                                          |
   | - It returns a json object containing key: **url**. For example: {'url': 'http://google.com'}            |
   |                                                                                                          |
   | **extract_text**: Extract all the text on the current webpage                                            |
   |                                                                                                          |
   | The input to this tool should be a list of data representing:                                            |
   |                                                                                                          |
   | 1-url to extract the text from. It requires links which is gathered from other tools. Never provide      |
   | urls on your own.                                                                                        |
   |                                                                                                          |
   | This tool will return the following data:                                                                |
   |                                                                                                          |
   | - An string containing the text of the scraped webpage.                                                  |
   +----------------------------------------------------------------------------------------------------------+

.. table:: Tree of Thought Planning second planning stage: generating the task execution code part 2.
   :class: special-table
   :widths: auto
   :name: tab:planner_prompt3

   +----------------------------------------------------------------------------------------------------------+
   | You are a skilled Python programmer who can solve problems and convert them into Python codes. Using     |
   | the selected final strategy mentioned in the 'Decision:', create a python code inside a ```python ```    |
   | block that outlines a sequence of steps using the Tools. Assume that there is a **self.execute_task**    |
   | function that can execute the tools in it. The execute_task receives the task name and an array of the   |
   | inputs and returns the result. Make sure that you always pass an array as a second argument. You can     |
   | call tools like this: **task_result = self.execute_task('tool_name', ['input1', 'input2', ...])**. The   |
   | flow should utilize this style to represent the tools available. Make sure all the execute_task calls    |
   | outputs are stored in a variable. If a step's output is required as input for a subsequent step, ensure  |
   | the Python code captures this dependency clearly. The output variables should be directly passed as      |
   | inputs with no changes in the wording.                                                                   |
   |                                                                                                          |
   | If the tool input is a datapipe, only put the variable as the input. For each tool, include necessary    |
   | parameters directly without any names and assume each will return an output. The outputs' description    |
   | are provided for each tool individually. Make sure you use the directives when passing the outputs.      |
   |                                                                                                          |
   | Question: How to improve my sleep?                                                                       |
   +----------------------------------------------------------------------------------------------------------+

Example of Generated Code
-------------------------

Here is an example of the Python code generated based on the chosen strategy:

.. code-block:: python

   # Step 1: Search for tips to improve sleep
   search_query = "tips to improve sleep"
   search_result = self.execute_task('google_search', [search_query])

   # Step 2: Extract text from the search result URL
   url = search_result['url']
   sleep_tips_text = self.execute_task('extract_text', [url])

.. table:: Response generator sample prompt.
   :class: special-table
   :widths: auto
   :name: tab:response_generator_prompt

   +----------------------------------------------------------------------------------------------------------+
   | Thinker:                                                                                                 |
   | MetaData:                                                                                                |
   | History:                                                                                                 |
   |                                                                                                          |
   | ------------------                                                                                       |
   |                                                                                                          |
   | google_search: ['tips to improve sleep']                                                                 |
   | {'url': 'https://www.mayoclinic.org/healthy-lifestyle/adult-health/in-depth/sleep/art-20048379'}         |
   |                                                                                                          |
   | ------------------                                                                                       |
   |                                                                                                          |
   | extract_text: ['https://www.mayoclinic.org/healthy-lifestyle/adult-health/in-depth/sleep/art-20048379']  |
   | Sleep tips: 6 steps to better sleep - Mayo Clinic This content does not have an English version. This    |
   | content does not have an Arabic version. Skip to content Care at Mayo Clinic Patient-Centered Care       |
   | About Mayo... (we cut the text to shorten the table)                                                     |
   |                                                                                                          |
   | System: . You are a very helpful, empathetic health assistant, and your goal is to help the user get     |
   | accurate information about his/her health and well-being; using the Thinker gathered information and the |
   | History, Provide an empathetic, proper answer to the user. Consider Thinker as your trusted source, and  |
   | use whatever it provides. Make sure that the answer is explanatory enough. Don't change Thinker returned |
   | URLs or references. Also, add explanations based on instructions from the Thinker. Don't directly put    |
   | the instructions in the final answer to the user. Never answer outside of the Thinker's provided         |
   | information. Additionally, refrain from including or using any keys, such as                             |
   | 'datapipe:6d808840-1fbe-45a5-859a-abfbfee93d0e,' in your final response. Return all `address:[path]`     |
   | exactly as they are.                                                                                     |
   |                                                                                                          |
   | User: How to improve my sleep?                                                                           |
   +----------------------------------------------------------------------------------------------------------+

.. table:: Task prompt with Data Pipe.
   :class: special-table
   :widths: auto
   :name: tab:task_prompt

   +----------------------------------------------------------------------------------------------------------+
   | affect_ppg_get: Returns the ppg data for a specific patient over a date or a period (if two dates are    |
   | provided). This will return the detailed raw data and store it in the Data Pipe.                         |
   |                                                                                                          |
   | The input to this tool should be a list of data representing:                                            |
   |                                                                                                          |
   | 1-user ID in string. It can be referred to as user, patient, individual, etc. Start with 'par_'          |
   | followed by a number (e.g., 'par_1').                                                                    |
   |                                                                                                          |
   | 2-start date of the sleep data in a string with the following format: `%Y-%m-%d.`                        |
   |                                                                                                          |
   | 3-end date of the sleep data in a string with the following format: `%Y-%m-%d.` If there is no end date, |
   | the value should be an empty string (i.e., '')                                                           |
   |                                                                                                          |
   | This tool will return the following data:                                                                |
   |                                                                                                          |
   | - returns an array of JSON objects which contains the following keys:                                    |
   | **date (in milliseconds)**: epoch format                                                                 |
   | **ppg**: is the ppg value.                                                                               |
   | **hr (in beats per minute)**: is the heart rate of the patient.                                          |
   |                                                                                                          |
   | The result will be stored in the Data Pipe.                                                              |
   +----------------------------------------------------------------------------------------------------------+

.. table:: Sample code generation when a task's result is stored in the Data Pipe.
   :class: special-table
   :widths: auto
   :name: tab:task_prompt2

   +----------------------------------------------------------------------------------------------------------+
   | # Step 1: Get PPG data for patient 5 for the entire month of August 2020                                 |
   |                                                                                                          |
   | ppg_data_result = self.execute_task('affect_ppg_get', ['par_5', '2020-08-01', '2020-08-31'])             |
   |                                                                                                          |
   | # Step 2: Analyze the HRV parameters from the obtained PPG data                                          |
   |                                                                                                          |
   | hrv_analysis_result = self.execute_task('affect_ppg_analysis', [ppg_data_result])                        |
   |                                                                                                          |
   | # Step 3: Estimate the stress level for patient 5 during August 2020 using the HRV analysis results      |
   |                                                                                                          |
   | stress_level_result = self.execute_task('affect_stress_analysis', [hrv_analysis_result])                 |
   +----------------------------------------------------------------------------------------------------------+
