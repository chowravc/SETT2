import os
import sys
import imp



def simulate(runName, numImages, imageDims, maxDefects, minDefects, decrossMin, decrossMax):
    """This runs a simulation to generate trianing data based on the parameters passed

        :param runName: Used as the folder name for saving generated images
        :type runName: str, unless told otherwise in the form of 'run DD/MM/YY/hh/mm/ss'
        :param numImages: the number of images to generate
        :type numImages: int, optional
        :param imageDims: dimensions of images to create 
        :type imageDims: int pairs, optional
        :param maxDefects: The maximum amount of defects a generated image can have
        :type maxDefects: int, optional
        :param minDefects: The minimum amount of defects that can be present in a generated image
        :type minDefects: int, optional
        :param decrossMin: An unused prameter for something - will add use later - ADAM LOOK HERE
        :type decrossMin: float, optional
        :param decrossMax: An unused prameter for something - will add use later - ADAM LOOK HERE
        :type decrossMax: float, optional
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

def extractSmartNoise():
    """
            This meathod calls the noiseExtractor.py file to extract noise from sample images.
    """

    print("Extracting Smart Noise")

    path = cfg['paths']['noiseExtractor']
    noiseExtraction = imp.load_source('packages', os.path.join(path,'noiseExtractor.py'))
    noiseExtraction.noiseExtractor(cfg)