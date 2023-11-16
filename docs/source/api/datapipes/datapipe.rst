DataPipes
=========


The **Data Pipe** is a repository of metadata and data acquired from **Uploaded files such as images and videos** and **Tasks' Results** through the execution of conversational sessions. \
This component is essential because numerous multimodal analysis involve intermediate stages, and their associated data must be retained for future retrieval. 
This class serves as a base class for creating new Data Pipes. Each new Data Pipe should implement the **store** and **retrieve** methods. \
The implementation should generate reasonable keys that can be used for accessing the data. It is recommended to not interfere in the way the data is stored. \
For example, changing the type of the data or the format of the data. If your Data Pipe requires specific format or type, make sure you the conversion inside the Data Pipe
ensuring consistency in the way tasks interact with Data Pipes. Look at `Memory <https://github.com/Mahyar12/CHA/blob/main/datapipes/memory.py>`_ for sample implementation.

    
- ``store`` : Storing intermediate results or needed information inside Data Pipe.

    .. autofunction:: datapipes.datapipe.DataPipe.store
        :no-index:


|


- ``retrieve`` : Retrieving data based on a key. The key is what is returned form `store`:

    .. autofunction:: datapipes.datapipe.DataPipe.retrieve
        :no-index:

