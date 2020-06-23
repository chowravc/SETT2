# Note: Though named defect tracker, this module is SETT2

### System for Enhancing simulated images, Training darkflow models, and Tracking ver. 2

## Setup


The system has been tested using anaconda with python 3.6 on both linux and windows.
to get requirements run:
```
pip install -r requirements.txt
```

All requirements should now be installed and SETT2 will be ready for usage.

## Basic SETT2 usage
SETT2 is a module designed to be run by importing functions and run in an external python file.
Create a python file in the same directory as this folder. Import sett with the following command.
```
import defectSimulation.sett2 as sett2
```
Run functions within sett2.
```
numImages = 10
imageDims = [250, 200]
maxDefects = 50
minDefects = 10
decrossMin = 50
decrossMax = 50

sett2.simulate(numImages, imageDims, maxDefects, minDefects, decrossMin, decrossMax)
```
## Functionality
