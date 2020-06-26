How to use 

use the command "pip install -r requirements.txt" in the LandauGin folder to install dependencies
modify accumulate.py to make fileConvertPath point to your ImageAnnotation folder. If you don't have ImageAnnotation,
clone it from https://github.com/mlfilms/ImageAnnotation.git

run
.\call_defect.sh

That command will generate a new folder containing the simulation results

run the commands
cd dataFolder
python accumulate.py

This will create a folder "accumulated" which contains the data from each simulation in the most recent set. The data will also be processed
to produce xml annotations, text annotations, images from the simulation, and images from the simulation with markings from the simulation 
detector

To change how many simulation runs occur in a set, modify the numRuns variable in param.py in the LandauGin folder
All changes to code made in teh dataFolder will be overwritten by the files in the LandauGin folder each time .\call_defect.sh is run



Training a darkflow model
clone https://github.com/mlfilms/defectTracker.git
follow the readme instructions in the defectTracker folder to setup an anaconda environment for running tensorflow
make sure to pip install -r requirements.txt in the defectTracker folder
Follow readme instructions on how to train a model
the annotation folder is LandauGin/dataFolder/accumulated/out
the dataset folder is LandauGin/dataFolder/accumulated
make sure to input the absolute path.

Once the model is trained, copy the .pb and .meta files from the darkflow/build_graph folder to the bin folder. You should also rename the files.
Modify runFlowPB.py to point to the new .pb and .meta files
