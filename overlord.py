import yaml
import argparse
import importlib
import os
import shutil
import sys
import imp
import glob
import numpy as np
import pandas as pd
import warnings

def simulate():

    numImages = 1
    imageDims = [250, 200]
    maxDefects = 50
    minDefects = 10
    decrossMin = 50
    decrossMax = 50

    home = os.getcwd()

    print("Running Simulation")
    simString = 'simulations/randomDefects/runSim.py'
    functionName = 'runSim'

    path, exFile = os.path.split(simString)
    fullPath = os.path.join(home, path)
    sys.path.append(fullPath)
    os.chdir(fullPath)

    sim = imp.load_source('packages', exFile)

    method = getattr(sim,functionName)

    method(home, numImages, imageDims, maxDefects, minDefects, decrossMin, decrossMax)

    os.chdir(home)

if __name__ == '__main__':

    simulate()