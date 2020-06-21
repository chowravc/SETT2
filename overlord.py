import os
import sys
import imp

def simulate():

    numImages = 1
    imageDims = [250, 200]
    maxDefects = 50
    minDefects = 10
    decrossMin = 50
    decrossMax = 50

    simString = 'simulations/randomDefects/runSim.py'
    functionName = 'runSim'

    home = os.getcwd()

    print("Running Simulation")

    path, exFile = os.path.split(simString)
    fullPath = os.path.join(home, path)
    sys.path.append(fullPath)
    os.chdir(fullPath)

    sim = imp.load_source('packages', exFile)

    runSimulation = getattr(sim,functionName)

    runSimulation(home, numImages, imageDims, maxDefects, minDefects, decrossMin, decrossMax)

    os.chdir(home)

if __name__ == '__main__':

    simulate()