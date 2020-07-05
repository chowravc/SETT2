import glob
import os
import random
import shutil
import sys
import yaml

# ------------- datAnnotate imports ----------------

import numpy as np

# ------------- create defects imports --------------

import datetime
import random
from joblib import Parallel, delayed

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

# ------------- fileConvert imports --------------

from xml.dom import minidom

# ------------------------------------------------------------------------------------------
#                                      Origional RunSim Class         
# ------------------------------------------------------------------------------------------

def runSim(home, runName, numImages, imageDims, maxDefects, minDefects, decrossMax, decrossMin):
    """Generate images and data of simulated smectic films with defects for training

    Args:
        home (str): home directory of sett2
        runName (str, unless told otherwise as 'run DD/MM/YY/hh/mm/ss'): the name of the directory the output of this function will be stored in. If it already exists, nothing will be overwritten
        numImages (int, optional): number of images the function should create
        imageDims (list, optional): dimensions of the images to be simulated as [x, y] where both are int
        maxDefects (int, optional): maximum number of defects an image can have
        minDefects (int, optional): minimum number of defects an image can have
        decrossMin (float, optional): minimum "Hourglass-ness" of a defect ADAM LOOK HERE
        decrossMax (float, optional): maximum "Hourglass-ness" of a defect ADAM LOOK HERE

    Writes:
        *_defect*.dat: Writes defect location data files to ../sett2/<runName>
        *_out*.dat: Writes spin data files to ../sett2/<runName>
        *_defect*.jpg: Writes images of the schlieren texture to ../sett2/<runName>
        *_defect*.txt: *defect*.dat converted to txt written to ../sett2/<runName>
        *_defect*SIMMARKED.jpg: Writes images of schlieren texture with annotated defects to ../sett2/<runName>/SIMMARKED
        *_defect*.xml: Writes defect bounding boxes in .xml format for YOLO training to ../sett2/<runName>/out

    Note:
        Creates *out*.dat files storing spins of individual molecules, *defect*.dat with defect locations marked.
        Also creates .jpg files containing the schlieren texture, the same images with annotated defect locaions and
        .xml files with defect locations to be used by YOLO.
    """

    print("Generating Defects")

    # Checks whether a run of the same name already exists.
    if os.path.exists(home+runName):
        print("A previous run of the same name already exists. Please delete it or rename the run.")
        return
    if not os.path.exists(home+runName):
        os.makedirs(home+runName)

    # Creates Defects.
    create_defects(numImages,imageDims,[minDefects,maxDefects])
    mainDir = os.getcwd()
    fileConvertPath = os.path.join(home, 'ImageAnnotation')
    outDir = os.path.join(home, runName)

    # Transfers generated files.
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
    
    # Transferring out generated data.
    datAnnotate(home, runName)
    print("Transfering out.dat files")
    for dat in allODat:
        drive,pathAndFile = os.path.splitdrive(dat)
        filePath, file = os.path.split(pathAndFile)
        filePath = os.path.dirname(dat)
        numPath = os.path.dirname(filePath)
        runNum = numPath.split('_')[-1]
        seedNum = filePath.split('-')[-1]
        simNum = int(file.split('out')[-1].split('.dat')[0])
        
        name = runNum+'_out'+str(simNum)+'.dat'
        newFilename = os.path.join(outDir,name)
        shutil.copyfile(dat,newFilename)
        
    # Copies over imgGen.py to the output directory.
    sys.path.append(outDir)
    os.chdir(outDir)

    print("Generating Images")

    # Creates defect images from data.
    imgGenRand(decrossMin, decrossMax)

    sys.path.append(fileConvertPath)

    print("Generating xml files")

    #Decides the files that will be converted
    fileConvertBatch(outDir, imageDims, 'txt')

    os.chdir(mainDir)

    print("Generating Simulation Annotated Images")
    markSim(home, runName)
    #print("Generating Noisy Training Images")
    #addArtifacts()
    print("Done")

# ------------------------------------------------------------------------------------------
#                                      Data Annotate Class         
# ------------------------------------------------------------------------------------------

def datAnnotate(home, runName):
    """Uses defect.dat files and converts them to text that get used to create bounding boxes.

    Args:
        home (str): home directory of sett2
        runName (str): name of the run

    Writes:
        *defect*.txt: text files containing defect bounding box locations
    """
    reset = os.getcwd()
    os.chdir(home+"/"+runName)
    files = glob.glob('*defect*.dat')
    for file in files:
        fExt = file.split('.')
        fpath = fExt[:-1]
        outFile = '.'.join(fpath)+'.txt'
        data = np.loadtxt(file)

        locs = np.where(abs(data)==1)
        x = locs[0]
        y = locs[1]

        numDefects = x.shape[0]
        f = open(outFile, "w")
        f.write('{}\r\n'.format(numDefects))

        for i in range(numDefects):
            f.write('{} {} {} {}\r\n'.format(y[i]-5,x[i]-5,y[i]+5,x[i]+5))
    os.chdir(reset)

# ------------------------------------------------------------------------------------------
#                                      Create Defects Class         
# ------------------------------------------------------------------------------------------

def create_defects(numImages,dims,numDefects):
    """Uses defect.dat files and converts them to text that get used to create bounding boxes.

    Args:
        numImages (int): number of images to generate
        dims (list): image dimensions in [x, y] where x, y are ints greater than 0
        numDefects (list): range of number of defects in ints [x, y] with y greater than or equal to x

    Writes:
        *defect*.dat and *out*.dat files containing defect location and spin information respectively written to ../sett2/simulations/randomDefects/dataFolder/<runTime>
    """
    baseDir = os.getcwd()
    dims.reverse()

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
    import randomD as rD
    sys.path.append(runDir)
    os.chdir(runDir)

    def process(i,defects):

        outdat = os.path.join(dataDir2,'out%d.dat' %(i))
        defectdat = os.path.join(dataDir2,'defect%d.dat' %(i))
        img = os.path.join(imDir,'image%d.bmp' %(i))
        rD.randomD(decross,dims,defects, [outdat, defectdat, img])

    Parallel(n_jobs=-1)(delayed(process)(i, random.randint(numDefects[0],numDefects[1])) for i in range(0,numImages))

    os.chdir(baseDir)

def safeMake(dir):
    """Safely creates a directory.

    Args:
        dir (str): directory to create

    Writes:
        dir: directory created if it does not exist
    """
    if not os.path.exists(dir):
        os.makedirs(dir)

def safeRemake(dir):
    """Safely remakes a directory.

    Args:
        dir (str): directory to remake

    Writes:
        dir: directory removed and remade as empty
    """
    if os.path.exists(dir):
        shutil.rmtree(dir)

# ------------------------------------------------------------------------------------------
#                                      RandomD Class         
# ------------------------------------------------------------------------------------------

'''
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
    temp= (np.sin(image)*np.cos(image)*np.sin(beta)-np.sin(image)**2*np.cos(beta)-np.cos(beta))**2
    return temp/temp.max()
    
#nDefects = 20

def schler(grid):
    return np.sin(2.*grid)**2

def dGen(grid,x,y,k,off,xDim, yDim):

    ix,iy = np.indices((xDim,yDim))
    grid = np.mod(grid+k*np.arctan2(ix-x,iy-y)+off,2*np.pi)
    return grid
'''
# ------------------------------------------------------------------------------------------
#                                      imgGen Class         
# ------------------------------------------------------------------------------------------


def decrossII(beta,image):
    """ADAM LOOK HERE

    Args:
        beta (float): the angle between polarisor and analyser in degrees (90 for completely crossed)

    Returns:
        out: ADAM LOOK HERE
    """
    temp= (np.sin(image)*np.cos(image)*np.sin(beta)-np.sin(image)**2*np.cos(beta)-np.cos(beta))**2
    out = temp/temp.max()
    return out

def schler(angle):
    """ADAM LOOK HERE

    Args:
        angle (float): the angle of local director at a point

    Returns:
        out: ADAM LOOK HERE
    """
    out = np.sin(2.*angle)**2.
    return out

def imgGen(decross):
    """ADAM LOOK HERE

    Args:
        decross (float): ADAM LOOK HERE

    Writes:
        <image>.jpg
    """
    beta = (np.pi/2 + decross/180*np.pi)
    names = glob.glob('accumulated/*out*.dat')
    frames = [decrossII(beta,np.loadtxt(n)) for n in names]
    
    names = [n.replace('out', 'defect') for n in names]
    
    [imageio.imwrite(n.split('.')[0]+'.jpg',skimage.img_as_ubyte(im)) for n,im in zip(names,frames)]


def imgGenRand(decrossMin,decrossMax):
    """ADAM LOOK HERE

    Args:
        decrossMin (float): ADAM LOOK HERE
        decrossMax (float): ADAM LOOK HERE

    Writes:
        <image>.jpg
    """
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
    """Takes in an image and predictions and returns the image with high confidence predictions annotated.
    
    Args:
        original_img (image): an array of int values
        predictions (dictionary): a dictionary of predictions and characterestics

    Returns:
        newImage (image): an array of int values with bright red dots at prediction locations

    Note:
        Hard-coded to label predictions with confidence over 0.3.
    """

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

    return newImage
    
    
    
def markSim(home, runName):
    """Generates simulation images with marked defect locations.

    Args:
        home (str): home directory of SETT
        runName (str): name of the run

    Writes:
        *defect*SIMMARKED.jpg: annotated image files written to ../sett2/<runName>/SIMMARKED
    """

    reset = os.getcwd()
    os.chdir(home + runName)
    simmarkedFolder = home + runName + '/SIMMARKED/'
    files = glob.glob('*defect*.dat')
    if not os.path.exists(simmarkedFolder):
        os.makedirs(simmarkedFolder)
    for file in files:
        fExt = file.split('.')
        fpath = fExt[:-1]
        fpathList = fpath[0].split('\\')
        fpathName = os.path.basename(fpath[0]).split('.')[0]
        
        #print(fpath)
        imgFile = '.'.join(fpath)+'.jpg'
        outImg = simmarkedFolder+fpathName+'SIMMARKED.jpg'
        data = np.loadtxt(file)
        locs = np.where(abs(data)==1)
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
    os.chdir(reset)

# ------------------------------------------------------------------------------------------
#                           fileConvert and fileConvertBatch Classes         
# ------------------------------------------------------------------------------------------

def fileConvert(filePath, outDir=None, delim = ' ', headerLines = 0, imageTag = '.jpg', imgSize = [250,250]):
    """Converts defect data files to xml files for training.

        Args:
            filePath (str): path of *defect*.dat files
            outDir (str, optional): path where files will be written in filePath
            delim (str, optional): ADAM LOOK HERE
            headerLines (int, optional): header lines of xml file outputted
            imageTag (str, optional): ADAM LOOK HERE
            imageSize (list, optional): image dimensions in [x, y] where both are ints greater than 0

        Writes:
            *defect*.xml: xml files for training neural networks with bounding boxes around defects
    """

    if outDir == None:
        outDir = os.path.join(os.path.split(filePath)[0],'out')
        
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    imgxS = str(imgSize[0])
    imgyS = str(imgSize[1])

    # Import the CSV into numpy array
    defects = np.loadtxt(open(filePath,'rb'), delimiter=delim, skiprows = headerLines)
    defects = defects.astype(int)

    # Generate the xml file
    doc = minidom.Document()

    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)

    # Generate metadata elements and add them to 'annotation'
    folder = doc.createElement('folder')
    folder.appendChild(doc.createTextNode('images'))
    annotation.appendChild(folder)
    filename = doc.createElement('filename')
    filename.appendChild(doc.createTextNode(os.path.basename(filePath).split('.')[0] + imageTag))
    annotation.appendChild(filename)
    segmented = doc.createElement('segmented')
    segmented.appendChild(doc.createTextNode('0'))
    
    width = doc.createElement('width')
    width.appendChild(doc.createTextNode(imgxS))
    height = doc.createElement('height')
    height.appendChild(doc.createTextNode(imgyS))
    depth = doc.createElement('depth')
    depth.appendChild(doc.createTextNode('3'))
    size = doc.createElement('size')
    size.appendChild(width)
    size.appendChild(height)
    size.appendChild(depth)
    annotation.appendChild(size)
    annotation.appendChild(segmented)

    if len(defects.shape)>1:
        for line in defects:
            # Create defect properties
            xmin = doc.createElement('xmin')
            
            ymin = doc.createElement('ymin')
            xmax = doc.createElement('xmax')
            ymax = doc.createElement('ymax')

            # Create branch elements to be used
            objet = doc.createElement('object')
            bndbox = doc.createElement('bndbox')
            name = doc.createElement('name')
            pose = doc.createElement('pose')
            truncated = doc.createElement('truncated')
            difficult = doc.createElement('difficult')
            
            # Add text data to the elements
            name.appendChild(doc.createTextNode('class'))
            pose.appendChild(doc.createTextNode('center'))
            truncated.appendChild(doc.createTextNode('1'))
            difficult.appendChild(doc.createTextNode('0'))
            
            # Define the Bounding box element
            if line.size == 2: # Basic x,y points
                xmin.appendChild(doc.createTextNode(str(line[0]-5)))
                xmax.appendChild(doc.createTextNode(str(line[0]+5)))
                ymin.appendChild(doc.createTextNode(str(line[1]-5)))
                ymax.appendChild(doc.createTextNode(str(line[1]+5)))
            elif line.size == 3:
                xmin.appendChild(doc.createTextNode(str(line[1]-5)))
                xmax.appendChild(doc.createTextNode(str(line[1]+5)))
                ymin.appendChild(doc.createTextNode(str(line[2]-5)))
                ymax.appendChild(doc.createTextNode(str(line[2]+5)))
            elif line.size == 4:
                xmin.appendChild(doc.createTextNode(str(line[0])))
                xmax.appendChild(doc.createTextNode(str(line[2])))
                ymin.appendChild(doc.createTextNode(str(line[1]-1)))
                ymax.appendChild(doc.createTextNode(str(line[3]+1)))
            else:
                continue
            bndbox.appendChild(xmin)
            
            bndbox.appendChild(ymin)
            bndbox.appendChild(xmax)
            bndbox.appendChild(ymax)
            
            # Add the elements to the defect
            objet.appendChild(name)
            objet.appendChild(pose)
            objet.appendChild(truncated)
            objet.appendChild(difficult)
            objet.appendChild(bndbox)

            # Add the defect to the overall list
            annotation.appendChild(objet)
    else:
        line = defects
                    # Create defect properties
        xmin = doc.createElement('xmin')
        ymin = doc.createElement('ymin')
        xmax = doc.createElement('xmax')
        ymax = doc.createElement('ymax')

        # Create branch elements to be used
        objet = doc.createElement('object')
        bndbox = doc.createElement('bndbox')
        name = doc.createElement('name')
        pose = doc.createElement('pose')
        truncated = doc.createElement('truncated')
        difficult = doc.createElement('difficult')
        
        # Add text data to the elements
        name.appendChild(doc.createTextNode('defect'))
        pose.appendChild(doc.createTextNode('center'))
        truncated.appendChild(doc.createTextNode('1'))
        difficult.appendChild(doc.createTextNode('0'))
        
        # Define the Bounding box element
        if line.size == 2: # Basic x,y points

            xmin.appendChild(doc.createTextNode(str(line[0]-5)))
            xmax.appendChild(doc.createTextNode(str(line[0]+5)))
            ymin.appendChild(doc.createTextNode(str(line[1]-5)))
            ymax.appendChild(doc.createTextNode(str(line[1]+5)))
        elif line.size == 3:

            xmin.appendChild(doc.createTextNode(str(line[2]-5)))
            xmax.appendChild(doc.createTextNode(str(line[2]+5)))
            ymin.appendChild(doc.createTextNode(str(line[1]-5)))
            ymax.appendChild(doc.createTextNode(str(line[1]+5)))
        elif line.size == 4:

            xmin.appendChild(doc.createTextNode(str(line[0])))
            xmax.appendChild(doc.createTextNode(str(line[2])))
            ymin.appendChild(doc.createTextNode(str(line[1]-1)))
            ymax.appendChild(doc.createTextNode(str(line[3]+1)))
        #else:
            #continue
        
        bndbox.appendChild(xmax)
        bndbox.appendChild(ymin)
        bndbox.appendChild(xmin)
        bndbox.appendChild(ymax)
        
        # Add the elements to the defect
        objet.appendChild(name)
        objet.appendChild(pose)
        objet.appendChild(truncated)
        objet.appendChild(difficult)
        objet.appendChild(bndbox)

        # Add the defect to the overall list
        annotation.appendChild(objet)

    fileName = os.path.basename(filePath).split('.')[0]+'.xml'

    xml_str = doc.toprettyxml(indent="    ")
    with open(os.path.join(outDir,fileName),"w") as f:
        f.write(xml_str)

def fileConvertBatch(targetDir,imgDims, ext='all'):
    """Takes in files and converts them to xml for detection.

    Args:
        targetDir (str): directory containing files to convert
        imgDims (list): image dimensions in [x, y] where both are ints greater than 0
        ext (str): extension of files to be converted
    """

    filePatternCustom = os.path.join(targetDir, '*defect*.dat')
    filePatternTXT = os.path.join(targetDir, '*.txt')
    filePatternDAT = os.path.join(targetDir, '*.dat')
    if ext == 'all':
        files = (glob.glob(filePatternTXT)+glob.glob(filePatternDAT))
    elif ext =='txt':
        files = glob.glob(filePatternTXT)

    elif ext =='dat':
        files = glob(filePatternDAT)

    elif ext =='custom':
        files = glob.glob(filePatternCustom)

    for filename in files:
        fileConvert(filename,headerLines=1,imgSize=imgDims)