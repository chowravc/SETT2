import shutil
import glob
import os
import sys
import json

with open('config.json') as json_config:
    config = json.load(json_config)

truthPath = os.path.abspath(config["validation_truth_path"]) #should be xml
detectionPath = os.path.abspath(config["validation_detection_path"]) #should be .json
mAPPath = os.path.abspath(config["mAPPath"]) #path to your map folder


mAPTruthPath = os.path.join(mAPPath,"input\\ground-truth\\")
#os.path.abspath("C:/Users/Eric Minor/TrackingML/defectTracker/mAP/input/ground-truth/")
mAPDetectionPath = os.path.join(mAPPath,"input\\detection-results\\")
#os.path.abspath("C:/Users/Eric Minor/TrackingML/defectTracker/mAP/input/detection-results")
mAPScriptsPath = os.path.join(mAPPath, "scripts\\extra\\")


def wipeFolder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)



wipeFolder(mAPTruthPath)
wipeFolder(mAPDetectionPath)


filePattern = 	os.path.join(truthPath,"*.xml")
#print(filePattern)
for filename in glob.glob(filePattern):
    drive,pathAndFile = os.path.splitdrive(filename)
    path, file = os.path.split(pathAndFile)
    newFilename = os.path.join(mAPTruthPath,file)
    shutil.copyfile(filename,newFilename)
    #print(filename)
    
    
filePattern = 	os.path.join(detectionPath,"*.json")
#print(filePattern)
for filename in glob.glob(filePattern):
    drive,pathAndFile = os.path.splitdrive(filename)
    path, file = os.path.split(pathAndFile)
    newFilename = os.path.join(mAPDetectionPath,file)
    shutil.copyfile(filename,newFilename)
	
sys.path.append(mAPScriptsPath)
os.chdir(mAPScriptsPath)
print(os.getcwd())
from convert_dr_darkflow_jsonF import convertJSON
from convert_gt_xmlF import convertXML
convertJSON()
convertXML()

sys.path.append(mAPPath)
os.chdir(mAPPath)

from mAPValDist import mAPVal

mAPVal(20)
