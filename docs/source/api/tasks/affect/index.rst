Affect
==========

This folder contains the implementation of Affect dataset connection and analysis. Different tasks access the right data, perform needed analysis
and return the results.

To use Affect sleep and activities data in CHA, please download the sample dataset from
`data.zip <https://drive.google.com/file/d/1VRb79cbNgWX0Xn-jylzFVQfudd5bKFnz/view?usp=drive_link>`_.
Next, unzip the file, and then copy the extracted “data” folder into the CHA directory (you may need to create this folder).

To use Affect PPG data in CHA, please download the sample dataset from
`PPG.zip <https://drive.google.com/file/d/18xbbDpQtBMq1jka-86Au4J-gdLQS4LY9/view?usp=sharing>`_.
Next, unzip the file, and then copy the extracted “data” folder into the CHA directory (you may need to create this folder). Also to be able
to use the pre-trained models for the stress analysis, download the following zip file:
`AffectStressCheckpoints.zip <https://drive.google.com/file/d/1wp43DbBREfD7-4pj87T3dkY-nVinyuUA/view?usp=sharing>`_.
unzip the file, and then copy the extracted “models” folder into the CHA directory (you may need to create this folder).


.. toctree::
   :maxdepth: 1

   base
   activity_get
   activity_analysis
   sleep_get
   sleep_analysis
   ppg_get
   ppg_analysis
   stress_analysis
