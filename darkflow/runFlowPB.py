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
        #im.save("your_file.jpeg")


    modelPath = cfg['darkflow']['model']
    path, filename = os.path.split(modelPath)
    name, ext = os.path.splitext(filename)

    if cfg['darkflow']['runTrained']:
        
        pbTarget = os.path.join(cfg['temp']['rootDir'],cfg['paths']['darkflow'],'built_graph', name+'.pb')
        metaTarget = os.path.join(cfg['temp']['rootDir'],cfg['paths']['darkflow'],'built_graph', name+'.meta')
    else:
        pbTarget = os.path.join(os.getcwd(),cfg['darkflow']['pb_file'])
        metaTarget = os.path.join(os.getcwd(),cfg['darkflow']['meta_file'])

    options = {"metaLoad": metaTarget, 
            "pbLoad": pbTarget,
            "gpu": cfg['darkflow']["gpu_usage"],
            "threshold": cfg['darkflow']["threshold"],
            "labels": cfg['darkflow']["labels_file"],
            "json": cfg['darkflow']["json"]
            }
    tfnet = TFNet(options)
    targetDir = cfg['darkflow']["run_directory"]
    #'E:/Projects/fake/data/defectData/corrected'
    print(targetDir)   
    outDir = os.path.join(targetDir,'outIMG')
    print(outDir)
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    '''
    xy = []
    offPath = os.path.isfile(targetdir+'/offsets.txt')
    if exists:
        offsets = np.loadtxt(open(offPath,'rb'))
        offsets = defects.astype(int)
        for line in defects:
            xy.append(line)
            


    else:
        xy.append(0)
        xy.append(0)
        # Keep presets   
    '''    
    filePattern = 	os.path.join(targetDir,'*.'+cfg['darkflow']["image_ext"])
    print(filePattern)
    files = glob.glob(filePattern)
    numFiles = len(files)
    spacing = numFiles/cfg['darkflow']['saveNum']

    imNum = 1
    for filename in files:
    
        (im,result) = processImage(filename,tfnet,box)
        #sections = filename.split("\\")
        imName = os.path.basename(filename)
        #imName = sections[-1]
        if cfg['darkflow']['genMarkedImages']:
            if cfg['darkflow']['saveAll']:
                saveName = os.path.join(outDir,imName)
                im.save(saveName)
            elif imNum % spacing ==0:
                saveName = os.path.join(outDir,imName)
                im.save(saveName)

        
        numDets = len(result)
        
        for i in range(numDets):
            result[i]['confidence'] = float(result[i]['confidence'])
        
        #print(result)
        dataJSON = json.dumps(result)
        prePost = imName.split(".")
        noEnd = prePost[0]
        
        jsonName = os.path.join(outDir,noEnd+".json")
        f = open(jsonName,"w")
        f.write(dataJSON)
        f.close
        imNum = imNum+1
        
            

    #imgcv = cv2.imread("E:\Projects\defectTracker\images\circle_1.jpg")


    #print("something")
    #wait = input("PRESS ENTER TO CONTINUE.")
    #print("something")



















































if __name__ == "__main__":

    box = 0 # 0 draws a box, 1 plots a point


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
        #im.save("your_file.jpeg")

    with open('config.json') as json_config:
        config = json.load(json_config)

    options = {"metaLoad": config["meta_file"], 
            "pbLoad": config["pb_file"],
            "gpu": config["gpu_usage"],
            "threshold": config["threshold"],
            "labels": config["labels_file"],
            "json": config["json"]
            }
    tfnet = TFNet(options)
    targetDir = config["run_directory"]
    #'E:/Projects/fake/data/defectData/corrected'
    print(targetDir)   
    outDir = targetDir+"\\outIMG\\"

    if not os.path.exists(outDir):
        os.makedirs(outDir)
    '''
    xy = []
    offPath = os.path.isfile(targetdir+'/offsets.txt')
    if exists:
        offsets = np.loadtxt(open(offPath,'rb'))
        offsets = defects.astype(int)
        for line in defects:
            xy.append(line)
            


    else:
        xy.append(0)
        xy.append(0)
        # Keep presets   
    '''    
    filePattern = 	targetDir+"\\*."+config["image_ext"]   

    for filename in glob.glob(filePattern):
    
        (im,result) = processImage(filename,tfnet,box)
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






