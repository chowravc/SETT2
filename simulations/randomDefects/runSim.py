import glob
import os
import random
import shutil
import sys
import yaml
#from addArtifacts import addArtifacts
# from create_defects import create_defects

# ------------- datAnnotate imports ----------------

import numpy as np
# ------------- create defects imports --------------

import datetime
import random
from joblib import Parallel,delayed
# from randomD import randomD


# ------------- RandomD imports --------------

import matplotlib.pyplot as plt
import imageio 
import skimage
import argparse

# ------------------------------------------------------------------------------------------
#                                      Origional RunSim Class         
# ------------------------------------------------------------------------------------------

# def runSimLocal():
#     with open("config.yml",'r') as ymlfile:
#         cfg = yaml.safe_load(ymlfile)
#     runSim(cfg)

def runSim():
    with open("config.yml",'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    numImages = cfg['simulation']['images']
    imageDims = [cfg['simulation']['xDim'],cfg['simulation']['yDim']]
    maxDefects = cfg['simulation']['maxDefects']
    minDefects = cfg['simulation']['minDefects']


    print("Generating Defects")
    create_defects(numImages,imageDims,[minDefects,maxDefects])
    fileConvertPath = os.path.join(cfg['temp']['rootDir'],cfg['paths']['fileConvert'])
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
    print("Generating xml files")
    from fileConvertBatch import fileConvertBatch
    fileConvertBatch(outDir,[cfg['simulation']['xDim'],cfg['simulation']['yDim']],'txt')


    os.chdir(mainDir)
    from markSim import markSim
    print("Generating Simulation Annotated Images")
    markSim()
    #print("Generating Noisy Training Images")
    #addArtifacts()
    print("Done")

if __name__ == '__main__':
    runSimLocal()


# ------------------------------------------------------------------------------------------
#                                      Data Annotate Class         
# ------------------------------------------------------------------------------------------


def datAnnotate():
    folder = 'accumulated/'
    files = glob.glob(folder+'*defect*.dat')
    #print(len(files))
    #filename = 'E:\\Projects\\fake\\simulations\\fortran\\LandauGin\\run20190529_131519\\data-k-1.00-beta-10.000-mu-0.000\\defect74.dat'
    for file in files:
        fExt = file.split('.')
        fpath = fExt[:-1]
        #print(fpath)
        outFile = '.'.join(fpath)+'.txt'
        data = np.loadtxt(file)

        locs = np.where(abs(data)==1)
        x = locs[0]
        y = locs[1]

        numDefects = x.shape[0]
        #print(outFile)
        f = open(outFile, "w")
        f.write('{}\r\n'.format(numDefects))

        for i in range(numDefects):
            f.write('{} {} {} {}\r\n'.format(y[i]-5,x[i]-5,y[i]+5,x[i]+5))

# ------------------------------------------------------------------------------------------
#                                      Create Defects Class         
# ------------------------------------------------------------------------------------------

def create_defects(numImages,dims,numDefects):
    baseDir = os.getcwd()
    dims.reverse()

    os.makedirs(dir)

    decross = 50
    iterations = 10

    now = datetime.datetime.now()

    dataDir = os.path.join(os.getcwd(),'dataFolder')
    safeRemake(dataDir)

    runDir = os.path.join(dataDir,"run%d%d%d_%d%d%d" %(now.year,now.month,now.day,now.hour,now.minute,now.second))
    safeMake(runDir)



    dataDir2 = os.path.join(runDir,'data')
    imDir = os.path.join(runDir,'im')
    safeMake(dataDir2)
    safeMake(imDir)
    shutil.copyfile('randomD.py',os.path.join(runDir,'randomD.py'))
    sys.path.append(runDir)
    os.chdir(runDir)

    def process(i,defects):
        #print(i)
        outdat = os.path.join(dataDir2,'out%d.dat' %(i))
        defectdat = os.path.join(dataDir2,'defect%d.dat' %(i))
        img = os.path.join(imDir,'image%d.bmp' %(i))
        randomD(decross,dims,defects, [outdat,defectdat,img])

    Parallel(n_jobs=-1)(delayed(process)(i, random.randint(numDefects[0],numDefects[1])) for i in range(0,numImages))

    os.chdir(baseDir)

def safeMake(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
def safeRemake(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)

# ------------------------------------------------------------------------------------------
#                                      RandomD Class         
# ------------------------------------------------------------------------------------------

def randomD(decross,dims,nDefects, fileNames):
    xDim = dims[0]
    yDim = dims[1]
    beta = np.pi/2+decross/180*np.pi


def decrossI(beta,image):
    #beta is the angle between pol and anl (90 for completely crossed)
    temp= ( np.sin(image)*np.cos(image)*np.sin(beta)-np.sin(image)**2*np.cos(beta)-np.cos(beta))**2
    return temp/temp.max()
    
#nDefects = 20
grid = np.reshape(np.zeros(xDim*yDim),(xDim,yDim))
dgrid = np.reshape(np.zeros(xDim*yDim),(xDim,yDim))
ix,iy = np.indices((xDim,yDim))

def schler(grid):
    return np.sin(2.*grid)**2
def dGen(grid,x,y,k,off):
    grid = np.mod(grid+k*np.arctan2(ix-x,iy-y)+off,2*np.pi)
    return grid


for i in np.arange(nDefects):
    dxp = random.randint(0,xDim-1)
    dyp = random.randint(0,yDim-1)

    dxn = random.randint(0,xDim-1)
    dyn = random.randint(0,yDim-1)

    grid = dGen(grid,dxp,dyp,1,random.random()*2*np.pi)
    grid = dGen(grid,dxn,dyn,-1,random.random()*2*np.pi)
    dgrid[dxp,dyp] =1
    dgrid[dxn,dyn] =-1
imageio.imwrite(fileNames[2],skimage.img_as_ubyte(decrossI(beta, grid)))
np.savetxt(fileNames[0],grid)
np.savetxt(fileNames[1],dgrid)

