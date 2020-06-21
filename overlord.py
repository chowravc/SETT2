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

def simulate():
    mainDir = os.getcwd()

    cfg = {'meta': {'runName': 'simulationTest', 'saveRun': False}, 'paths': {'simRunner': 'simulations/randomDefects/runSim.py', 'simFunc': 'runSim', 'fileConvert': 'ImageAnnotation'}, 'simulation': {'images': 1, 'numDefects': 20, 'minDefects': 10, 'maxDefects': 50, 'xDim': 250, 'yDim': 200, 'decrossMax': 50, 'decrossMin': 50}}

    saveDir = os.path.join('runData',cfg['meta']['runName']) #
    if cfg['meta']['saveRun']:
        if not os.path.exists(saveDir):
            os.makedirs(saveDir)
        
        with open(os.path.join(saveDir,'config.yml'), 'w') as yaml_file:
            yaml.dump(cfg, yaml_file, default_flow_style=False)

    cfg["temp"] = {}
    cfg["temp"]["rootDir"] = os.getcwd()

    print("Running Simulation")
    simString = 'simulations/randomDefects/runSim.py'
    functionName = 'runSim'

    #this function will execute a script, using the folder
    # the script is located in as the working directory
    path, exFile = os.path.split(simString)
    mainDir = os.getcwd()
    fullPath = os.path.join(mainDir,path)
    sys.path.append(fullPath)
    os.chdir(fullPath)

    sim = imp.load_source('packages', exFile)
    print()
    print(sim)
    print()
    method = getattr(sim,functionName)
    method(cfg)

    os.chdir(mainDir)

    os.chdir(mainDir)

if __name__ == '__main__':

    simulate()