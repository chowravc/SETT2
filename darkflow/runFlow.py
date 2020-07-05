from darkflow.net.build import TFNet
import cv2
import matplotlib.pyplot as plt
import pprint as pp
import numpy as np
from PIL import Image
import glob
import os
import json


def runFlowCFG(cfg):
    def boxing(original_img , predictions):
    newImage = np.copy(original_img)

    for result in predictions:
        top_x = result['topleft']['x']
        top_y = result['topleft']['y']

        btm_x = result['bottomright']['x']
        btm_y = result['bottomright']['y']
    
        confidence = result['confidence']
        label = result['label'] + " " + str(round(confidence, 3))
        
        if confidence > 0.3:
            newImage = cv2.rectangle(newImage, (top_x, top_y), (btm_x, btm_y), (255,0,0), 3)
            #newImage = cv2.putText(newImage, label, (top_x, top_y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL , 0.8, (0, 230, 0), 1, cv2.LINE_AA)
        
    return newImage
	
    def processImage(filename, tfnet):
        imgcv = cv2.imread(filename)
        result = tfnet.return_predict(imgcv)
        #print(result)
        newImage = boxing(imgcv, result)
        im = Image.fromarray(newImage)
        return (im,result)
        #im.save("your_file.jpeg")

    

    options = {"model": cfg['darkflow']["model"], 
            "load": -1,
            "gpu": 1.0,
            "threshold": 0.1,
            "labels": "one_label.txt",
            "json": True
            }
    tfnet = TFNet(options)
    targetDir = 'E:/Projects/fake/defectTracker/matlab/imagesCLEAN'
    print(targetDir)   
    outDir = targetDir+"\\out\\"

    if not os.path.exists(outDir):
        os.makedirs(outDir)
        
        
    filePattern = 	targetDir+"\\*.jpg"   

    for filename in glob.glob(filePattern):
    
        (im,result) = processImage(filename,tfnet)
        sections = filename.split("\\")
        imName = sections[-1]
        im.save(outDir+imName)
        
        numDets = len(result)
        
        for i in range(numDets):
            result[i]['confidence'] = float(result[i]['confidence'])
        
        #print(result)
        dataJSON = json.dumps(result)
        prePost = imName.split(".")
        noEnd = prePost[0]
        
        f = open(outDir+noEnd+".json","w")
        f.write(dataJSON)
        f.close

















































    
if __name__ == "__main__":
    def boxing(original_img , predictions):
    newImage = np.copy(original_img)

    for result in predictions:
        top_x = result['topleft']['x']
        top_y = result['topleft']['y']

        btm_x = result['bottomright']['x']
        btm_y = result['bottomright']['y']
    
        confidence = result['confidence']
        label = result['label'] + " " + str(round(confidence, 3))
        
        if confidence > 0.3:
            newImage = cv2.rectangle(newImage, (top_x, top_y), (btm_x, btm_y), (255,0,0), 3)
            #newImage = cv2.putText(newImage, label, (top_x, top_y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL , 0.8, (0, 230, 0), 1, cv2.LINE_AA)
        
    return newImage
	
	
	
	
def processImage(filename, tfnet):
    imgcv = cv2.imread(filename)
    result = tfnet.return_predict(imgcv)
    #print(result)
    newImage = boxing(imgcv, result)
    im = Image.fromarray(newImage)
    return (im,result)
    #im.save("your_file.jpeg")


options = {"model": "cfg/yolo_custom2.cfg", 
           "load": -1,
           "gpu": 1.0,
		   "threshold": 0.1,
		   "labels": "one_label.txt",
           "json": True
		   }
tfnet = TFNet(options)
targetDir = 'E:/Projects/fake/defectTracker/matlab/imagesCLEAN'
print(targetDir)   
outDir = targetDir+"\\out\\"

if not os.path.exists(outDir):
    os.makedirs(outDir)
    
    
filePattern = 	targetDir+"\\*.jpg"   

for filename in glob.glob(filePattern):
 
    (im,result) = processImage(filename,tfnet);
    sections = filename.split("\\")
    imName = sections[-1]
    im.save(outDir+imName)
    
    numDets = len(result)
    
    for i in range(numDets):
        result[i]['confidence'] = float(result[i]['confidence'])
    
    #print(result)
    dataJSON = json.dumps(result)
    prePost = imName.split(".")
    noEnd = prePost[0]
    
    f = open(outDir+noEnd+".json","w")
    f.write(dataJSON)
    f.close
               

#imgcv = cv2.imread("E:\Projects\defectTracker\images\circle_1.jpg")


#print("something")
#wait = input("PRESS ENTER TO CONTINUE.")
#print("something")






