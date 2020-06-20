import cv2
import matplotlib.pyplot as plt
import pprint as pp
import numpy
from PIL import Image
import glob
import os
import json


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

if __name__ == "__main__":
    markSim()