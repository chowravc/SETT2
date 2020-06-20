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

def executeFile(filePath,functionName,cfg):
    #this function will execute a script, using the folder
    # the script is located in as the working directory
    path, exFile = os.path.split(filePath)
    mainDir = os.getcwd()
    fullPath = os.path.join(mainDir,path)
    sys.path.append(fullPath)
    os.chdir(fullPath)

    sim = imp.load_source('packages', exFile)
    method = getattr(sim,functionName)
    method(cfg)

    os.chdir(mainDir)

def executeConfig(configName):
    mainDir = os.getcwd()
    with open(configName,'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    saveDir = 'runData\simulationTest'
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    cfg["temp"] = {}
    cfg["temp"]["rootDir"] = mainDir

    print("Running Simulation")
    simString = 'simulations/randomDefects/runSim.py'
    functionName = 'runSim'

    executeFile(simString,functionName,cfg)

    print(cfg['temp']['rootDir'])
    os.chdir(cfg['temp']['rootDir'])

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("config",nargs='?',type = str, default='config.yml', help='config file to execute')
    parser.add_argument("--reeval", dest='reeval', default='False', action='store_const', const=True, help='config file to execute')
    args= parser.parse_args()
    config = args.config

    with open(config,'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    executeConfig(config)