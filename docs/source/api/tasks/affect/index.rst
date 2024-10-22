Affect
==========

This folder contains the implementation of Affect dataset connection and analysis. Different tasks access the right data, perform needed analysis
and return the results.
To use Affect in CHA, please download the sample dataset from
`data.zip <https://drive.google.com/file/d/1VRb79cbNgWX0Xn-jylzFVQfudd5bKFnz/view>`_.
Next, unzip the file, and then add DATA_DIR to your environment pointing to your folders.

.. code-block:: bash

  export DATA_DIR="path/to/folder"

.. toctree::
   :maxdepth: 1

   base
   activity_get
   activity_analysis
   sleep_get
   sleep_analysis
