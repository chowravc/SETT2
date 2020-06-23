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

# ------------- RandomD imports --------------

import matplotlib.pyplot as plt
import imageio 
import skimage
import argparse

# ------------- imgGen imports --------------

# All duplicates

# ------------- markSim imports --------------

import cv2
import pprint as pp
from PIL import Image
import json
# ------------------------------------------------------------------------------------------
#                                      Origional RunSim Class         
# ------------------------------------------------------------------------------------------

# def runSimLocal():
#     with open("config.yml",'r') as ymlfile:
#         cfg = yaml.safe_load(ymlfile)
#     runSim(cfg)



def runSim(home, runName, numImages, imageDims, maxDefects, minDefects, decrossMax, decrossMin):

    print("Generating Defects")

    #Creates Defects
    create_defects(numImages,imageDims,[minDefects,maxDefects])
    mainDir = os.getcwd()
    fileConvertPath = os.path.join(home, 'ImageAnnotation')
    outDir = os.path.join(home, runName)

    if os.path.exists(outDir):
        print("A previous run of the same name already exists. Please delete it or rename the run.")
        return
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    #Transfers generated files
    allDDat = glob.glob('dataFolder/**/**/defect*.dat')
    print("Transfering defect.dat files")
    for dat in allDDat:
        drive,pathAndFile = os.path.splitdrive(dat)
        filePath, file = os.path.split(pathAndFile)
        filePath = os.path.dirname(dat)
        numPath = os.path.dirname(filePath)
        runNum = numPath.split('_')[-1]
        seedNum = filePath.split('-')[-1]
        simNum = int(file.split('defect')[-1].split('.dat')[0])
        name = runNum+'_defect'+str(simNum)+'.dat'
        newFilename = os.path.join(outDir,name)
        shutil.copyfile(dat,newFilename)
        
    allODat = glob.glob('dataFolder/**/**/out*.dat')
    
    datAnnotate(home, runName)
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
        

    #Copies over imgGen.py to the output directory
    shutil.copyfile('imgGen.py',os.path.join(outDir,'imgGen.py'))
    sys.path.append(outDir)
    os.chdir(outDir)

    # from imgGen import imgGenRand

    print("Generating Images")

    #Creates defect images from data
    imgGenRand(decrossMin, decrossMax)


    sys.path.append(fileConvertPath)

    print("Generating xml files")
    # from fileConvertBatch import fileConvertBatch

    #Decides the files that will be converted
    fileConvertBatch(outDir, imageDims, 'custom')

    os.chdir(mainDir)

    print("Generating Simulation Annotated Images")
    markSim(home, runName)
    #print("Generating Noisy Training Images")
    #addArtifacts()
    print("Done")



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

    grid = np.reshape(np.zeros(xDim*yDim),(xDim,yDim))
    dgrid = np.reshape(np.zeros(xDim*yDim),(xDim,yDim))
    ix,iy = np.indices((xDim,yDim))

    for i in np.arange(nDefects):
        dxp = random.randint(0,xDim-1)
        dyp = random.randint(0,yDim-1)

        dxn = random.randint(0,xDim-1)
        dyn = random.randint(0,yDim-1)

        grid = dGen(grid,dxp,dyp,1,random.random()*2*np.pi, xDim, yDim)
        grid = dGen(grid,dxn,dyn,-1,random.random()*2*np.pi, xDim, yDim)
        dgrid[dxp,dyp] =1
        dgrid[dxn,dyn] =-1
        
    imageio.imwrite(fileNames[2],skimage.img_as_ubyte(decrossI(beta, grid, dims)))
    np.savetxt(fileNames[0],grid)
    np.savetxt(fileNames[1],dgrid)

def decrossI(beta,image,dims):
    xDim = dims[0]
    yDim = dims[1]
    #beta is the angle between pol and anl (90 for completely crossed)
    temp= ( np.sin(image)*np.cos(image)*np.sin(beta)-np.sin(image)**2*np.cos(beta)-np.cos(beta))**2
    return temp/temp.max()
    
#nDefects = 20

def schler(grid):
    return np.sin(2.*grid)**2

def dGen(grid,x,y,k,off,xDim, yDim):

    ix,iy = np.indices((xDim,yDim))
    grid = np.mod(grid+k*np.arctan2(ix-x,iy-y)+off,2*np.pi)
    return grid

# ------------------------------------------------------------------------------------------
#                                      imgGen Class         
# ------------------------------------------------------------------------------------------


def decrossII(beta,image):
    #beta is the angle between pol and anl (90 for completely crossed)
    temp= ( np.sin(image)*np.cos(image)*np.sin(beta)-np.sin(image)**2*np.cos(beta)-np.cos(beta))**2
    return temp/temp.max()

def schler(angle):
    return np.sin(2.*angle)**2.
def imgGen(decross):
    beta = (np.pi/2+decross/180*np.pi)
    names = glob.glob('accumulated/*out*.dat')
    frames = [decrossII(beta,np.loadtxt(n)) for n in names]
    
    names = [n.replace('out', 'defect') for n in names]
    
    [imageio.imwrite(n.split('.')[0]+'.jpg',skimage.img_as_ubyte(im)) for n,im in zip(names,frames)]


def imgGenRand(decrossMin,decrossMax):
    decrossMean = (decrossMin+decrossMax)/2
    decrossDiff = decrossMax-decrossMin
    
    names = glob.glob('*out*.dat')
    decross = np.random.rand(len(names))*decrossDiff+(decrossMean-decrossDiff/2)
    betas = np.pi/2+decross/180*np.pi
    frames = [decrossII(beta,np.loadtxt(n)) for (beta,n) in zip(betas,names)]
    
    names = [n.replace('out', 'defect') for n in names]
    
    [imageio.imwrite(n.split('.')[0]+'.jpg',skimage.img_as_ubyte(im)) for n,im in zip(names,frames)]


# ------------------------------------------------------------------------------------------
#                                      markSim Class         
# ------------------------------------------------------------------------------------------
    

def pointing(original_img , predictions):
    newImage = np.copy(original_img)

    for result in predictions:
        top_x = result['topleft']['x']
        top_y = result['topleft']['y']

        btm_x = result['bottomright']['x']
        btm_y = result['bottomright']['y']
        
        x = int((top_x+btm_x)/2)
        y = int((top_y+btm_y)/2)
    
        confidence = result['confidence']
        label = result['label'] + " " + str(round(confidence, 3))
        
        if confidence > 0.3:
            newImage = cv2.circle(newImage, (x, y), 2, (255,0,0), -1)
            #newImage = cv2.putText(newImage, label, (top_x, top_y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL , 0.8, (0, 230, 0), 1, cv2.LINE_AA)
        
    return newImage
    
    
    
def markSim():
    folder = 'accumulated/'
    simmarkedFolder = 'accumulated/SIMMARKED/'
    files = glob.glob(folder+'*defect*.dat')
    
   

    if not os.path.exists(simmarkedFolder):
        os.makedirs(simmarkedFolder)
    
    #print(len(files))
    #filename = 'E:\\Projects\\fake\\simulations\\fortran\\LandauGin\\run20190529_131519\\data-k-1.00-beta-10.000-mu-0.000\\defect74.dat'
    for file in files:
        fExt = file.split('.')
        fpath = fExt[:-1]
        fpathList = fpath[0].split('\\')
        fpathName = os.path.basename(fpath[0]).split('.')[0]
        
        #print(fpath)
        imgFile = '.'.join(fpath)+'.jpg'
        outImg = folder+'SIMMARKED/'+fpathName+'SIMMARKED.jpg'
        data = numpy.loadtxt(file)
        locs = numpy.where(abs(data)==1)
        x = locs[0]
        y = locs[1]

        numDefects = x.shape[0]
        #print(fpathList)
        imgcv = cv2.imread(imgFile)
        for i in range(numDefects):
            imgcv = cv2.circle(imgcv, (y[i], x[i]), 2, (255,0,0), -1)
        im = Image.fromarray(imgcv)
        im.save(outImg)
            #f.write('{} {} {} {}\r\n'.format(y[i]-3,x[i]-3,y[i]+3,x[i]+3));