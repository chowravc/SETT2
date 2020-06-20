import glob
import os
import shutil
import sys
import yaml
from datAnnotate import datAnnotate
from addArtifacts import addArtifacts
from create_defects import create_defects


def accumulate():
    with open("config.yml",'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    create_defects(cfg['simulation']['images'], [cfg['simulation']['xDim'],cfg['simulation']['yDim']])
    fileConvertPath = os.path.join(os.getcwd(),cfg['paths']['fileConvert'])
    mainDir = os.getcwd()
    outDir = os.path.join(os.getcwd(),'accumulated')

    #print(outDir)
    if os.path.exists(outDir):
        shutil.rmtree(outDir)
    #if not os.path.exists(outDir):
    os.makedirs(outDir)
        
    allDDat = glob.glob('dataFolder/**/**/defect*.dat')
    print("Transfering defect.dat files")
    for dat in allDDat:
        #print(dat)
        drive,pathAndFile = os.path.splitdrive(dat)
        filePath, file = os.path.split(pathAndFile)
        filePath = os.path.dirname(dat)
        numPath = os.path.dirname(filePath)
        runNum = numPath.split('_')[-1]
        seedNum = filePath.split('-')[-1]
        #print(seedNum)
        simNum = int(file.split('defect')[-1].split('.dat')[0])
        #print(simNum)
        #if simNum>20:
        name = runNum+'_defect'+str(simNum)+'.dat'
        newFilename = os.path.join(outDir,name)
        shutil.copyfile(dat,newFilename)
        
    allODat = glob.glob('dataFolder/**/**/out*.dat')
    print("Generating xml files")
    datAnnotate()
    print("Transfering out.dat files")
    for dat in allODat:
        drive,pathAndFile = os.path.splitdrive(dat)
        filePath, file = os.path.split(pathAndFile)
        filePath = os.path.dirname(dat)
        numPath = os.path.dirname(filePath)
        runNum = numPath.split('_')[-1]
        seedNum = filePath.split('-')[-1]
        #print(seedNum)
        simNum = int(file.split('out')[-1].split('.dat')[0])
        
        #print(simNum)
        #if simNum>20:
        name = runNum+'_out'+str(simNum)+'.dat'
        newFilename = os.path.join(outDir,name)
        shutil.copyfile(dat,newFilename)
        
    shutil.copyfile('imgGen.py',os.path.join(outDir,'imgGen.py'))
    sys.path.append(outDir)
    os.chdir(outDir)
    from imgGen import imgGenRand
    print("Generating Images")
    imgGenRand(cfg['simulation']['decrossMin'],cfg['simulation']['decrossMax'])
    sys.path.append(fileConvertPath)
    from fileConvertBatch import fileConvertBatch
    fileConvertBatch(outDir,[cfg['simulation']['xDim'],cfg['simulation']['yDim']])


    os.chdir(mainDir)
    from markSim import markSim
    print("Generating Simulation Annotated Images")
    markSim()
    print("Generating Noisy Training Images")
    addArtifacts()
    print("Done")

if __name__ == '__main__':
    accumulate()


