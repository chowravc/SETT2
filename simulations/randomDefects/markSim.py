import cv2
import matplotlib.pyplot as plt
import pprint as pp
import numpy
from PIL import Image
import glob
import os
import json


def pointing(original_img , predictions):

    """
        Finds the confidencey, bounding box information, and predicted label of the simulated image.

        Args:
           origional_img (str): Path to image
           predictions (str): The predictions the net has made about the images
          
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
            #newImage = cv2.putText(newImage, label, (top_x, top_y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL , 0.8, (0, 230, 0), 1, cv2.LINE_AA)
        
    return newImage
    
    
    
def markSim(home, runName):

    """
        Image processing for marking simulated images

        Args:
           home (str): Home directory (in this case DefectSimulation)
           runName (str): Name of run - unless told otherwise in the form of 'run DD/MM/YY/hh/mm/ss'
          
    """

    simmarkedFolder = home + runName + '/SIMMARKED/'
    files = glob.glob(runName+'/*defect*.dat')

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

if __name__ == "__main__":
    markSim()