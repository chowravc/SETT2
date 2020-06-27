import os
import sys
import imp

def simulate(runName, numImages, imageDims, maxDefects, minDefects, decrossMin, decrossMax):
    """Create images of a simulated liquid crystal films with defects.
    Creates *out*.dat files storing spins of individual molecules, *defect*.dat with defect locations marked.
    Also creates .jpg files containing the schlieren texture, the same images with annotated defect locaions and
    .xml files with defect locations to be used by YOLO.

    Parameters
    ----------
    runName : (str) the name of the directory the output of this function will be stored in. If it already exists, nothing will be overwritten.
    numImages : (int) number of images the function should create.
    imageDims : (list) dimensions of the images to be simulated. [x, y]
    maxDefects : (int) maximum number of defects an image can have.
    minDefects : (int) minimum number of defects an image can have.
    decrossMin : (int) minimum "Hourglass-ness" of a defect. UPDATE
    decrossMax : (int) maximum "Hourglass-ness" of a defect. UPDATE

    Returns
    -------
    None

    Notes
    -----


    See also
    --------
    
    """

    simString = 'simulations/randomDefects/runSim.py'
    functionName = 'runSim'

    home = os.getcwd() + '/defectSimulation/'

    print("Running Simulation")

    path, exFile = os.path.split(simString)
    fullPath = os.path.join(home, path)
    sys.path.append(fullPath)
    os.chdir(fullPath)

    sim = imp.load_source('packages', exFile)

    runSimulation = getattr(sim,functionName)

    runSimulation(home, runName, numImages, imageDims, maxDefects, minDefects, decrossMin, decrossMax)

    os.chdir(home)

def extractSmartNoise(crop, cropManual, cropX, cropY):
    
    path = "/smartNoise/"
    noiseSamplePath = "/smartNoise/noiseSamples/"
    
    home = os.getcwd() + '/defectSimulation/'

    print("Extracting Smart Noise")
    
    functionPath = home + path
    
    noiseExtraction = imp.load_source('packages', os.path.join(functionPath,'noiseExtractor.py'))
    
    noiseExtraction.noiseExtractor(home, noiseSamplePath, crop, cropManual, cropX, cropY)