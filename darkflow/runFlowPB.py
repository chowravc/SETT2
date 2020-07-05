from darkflow.net.build import TFNet
import cv2
import matplotlib.pyplot as plt
import pprint as pp
import numpy as np
from PIL import Image
import glob
import os
import json
import time


def runFlowCFG(home, runTrained, gpu, threshold, jsonBool, extension, genMarkedImages, saveAll):
    
    box = 0 # 1 draws a box, 0 plots a point

    def standardize(image):
        print(image.dtype)
        image = image.astype(np.float64)
        imgMean = np.mean(image)
        imgSTD = np.std(image)
        image= (image - imgMean)/(6*imgSTD)
        image = image+0.5
        #image = image*255
        image = np.clip(image,0,1)
        return image
        
    def rgb2gray(rgb):

        r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

        return gray


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
            
            if confidence > 0.1:
                newImage = cv2.circle(newImage, (x, y), 2, (255,0,0), -1)
                newImage = cv2.putText(newImage, label, (top_x, top_y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL , 0.8, (0, 230, 0), 1, cv2.LINE_AA)
            
        return newImage
        
    def processImage(filename, tfnet,box):
        imgcv = cv2.imread(filename)
        #imgcv = rgb2gray(imgcv)
        result = tfnet.return_predict(imgcv)
        #print(result)
        if box ==1:
            newImage = boxing(imgcv, result)
        else:
            newImage = pointing(imgcv, result)
            
        
        im = Image.fromarray(newImage)

        return (im,result)

    modelPath = "cfg/yolo_custom2.cfg"
    darkflow = "/darkflow/"

    meta = "bin/defectT.meta"
    pb = "bin/defectT.pb"

    labels = "one_label.txt"
    saveNum = 10
    targetDir = "../../data/collated/annotations/corrected"

    path, filename = os.path.split(modelPath)
    name, ext = os.path.splitext(filename)
    name = "yolo_custom2"

    if runTrained:
        
        pbTarget = home + darkflow + '/built_graph/' + name + '.pb'
        metaTarget = home + darkflow + '/built_graph/' + name + '.meta'

    else:
        pbTarget = os.path.join(os.getcwd(), pb)
        metaTarget = os.path.join(os.getcwd(), meta)

    options = {"metaLoad": metaTarget, 
            "pbLoad": pbTarget,
            "gpu": gpu,
            "threshold": threshold,
            "labels": labels,
            "json": jsonBool
            }

    tfnet = TFNet(options)

    #print(targetDir)   

    outDir = os.path.join(targetDir,'outIMG')
    #print(outDir)

    if not os.path.exists(outDir):
        os.makedirs(outDir)
    
    filePattern = os.path.join(targetDir,'*.'+ extension)
    print("Looking for images ", filePattern)
    files = glob.glob(filePattern)
    numFiles = len(files)
    print("Detecting defects in " + repr(numFiles) + " images.")
    print()
    spacing = numFiles/saveNum

    imNum = 1
    for filename in files:

        if imNum == 3:
            imgStart = time.time()

        print("Detecting defects in image " + repr(imNum) + " of " + repr(numFiles) + ".")

        (im,result) = processImage(filename,tfnet,box)
        imName = os.path.basename(filename)
        if genMarkedImages:
            if saveAll:
                saveName = os.path.join(outDir,imName)
                im.save(saveName)
            elif imNum % spacing ==0:
                saveName = os.path.join(outDir,imName)
                im.save(saveName)

        numDets = len(result)
        
        for i in range(numDets):
            result[i]['confidence'] = float(result[i]['confidence'])
        
        dataJSON = json.dumps(result)
        prePost = imName.split(".")
        noEnd = prePost[0]
        
        jsonName = os.path.join(outDir,noEnd+".json")
        f = open(jsonName,"w")
        f.write(dataJSON)
        f.close

        if imNum == 3:
            print("Estimated time left: " + repr((numFiles-3)*(time.time() - imgStart)) + " seconds.")

        imNum = imNum + 1
    print("Done")
    print()