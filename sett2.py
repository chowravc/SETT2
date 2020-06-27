import os
import sys
import imp

def simulate(runName, numImages, imageDims, maxDefects, minDefects, decrossMin, decrossMax):

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