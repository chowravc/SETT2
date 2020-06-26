import glob
import os
import shutil
import sys
from datAnnotate import datAnnotate

#
fileConvertPath = 'C:/Users/Eric Minor/TrackingML/defectTracker/ImageAnnotation'
mainDir = os.getcwd()
outDir = os.path.join(os.getcwd(),'accumulated');

#print(outDir)
if os.path.exists(outDir):
    shutil.rmtree(outDir)
#if not os.path.exists(outDir):
os.makedirs(outDir)
    
allDDat = glob.glob('**/**/defect*.dat')
print("Transfering defect.dat files")
for dat in allDDat:
    drive,pathAndFile = os.path.splitdrive(dat)
    filePath, file = os.path.split(pathAndFile)
    filePath = os.path.dirname(dat)
    numPath = os.path.dirname(filePath)
    runNum = numPath.split('_')[-1]
    seedNum = filePath.split('-')[-1]
    #print(seedNum)
    simNum = int(file.split('defect')[-1].split('.dat')[0])
    #print(simNum)
    if simNum>20:
        name = seedNum+'_defect'+str(simNum)+'.dat'
        newFilename = os.path.join(outDir,name)
        shutil.copyfile(dat,newFilename)
    
allODat = glob.glob('**/**/out*.dat')
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
    if simNum>20:
        name = seedNum+'_out'+str(simNum)+'.dat'
        newFilename = os.path.join(outDir,name)
        shutil.copyfile(dat,newFilename)
    
shutil.copyfile('imgGen.py',os.path.join(outDir,'imgGen.py'))
sys.path.append(outDir)
os.chdir(outDir)
from imgGen import imgGen
print("Generating Images")
imgGen()
sys.path.append(fileConvertPath)
from fileConvertBatch import fileConvertBatch
fileConvertBatch(outDir,[200,200])


os.chdir(mainDir)
from markSim import markSim
print("Generating Simulation Annotated Images")
markSim()
print("Done")

