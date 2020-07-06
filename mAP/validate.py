import shutil
import glob
import os
import sys
import json
import imp

def validateRun(home, mAP, validationTruthPath, validationDetectionPath):
	"""Validate a trained model on a test set with xml true files and json detection files, result in mAP.

    Args:
        home (str): home directory of SETT
        mAP (str): mAP directory
        validationTruthPath (str): path to true xml files UPDATE
        validationDetectionPath (str): path to detected json files UPDATE

    Writes:
        results: results of validation

    Note:
        UPDATE
    """

    truthPath = os.path.join(home, validationTruthPath) #should be xml
    detectionPath = os.path.join(home, validationDetectionPath) #should be .json
    mAPPath = os.path.join(home, mAP) #path to your map folder

    mAPTruthPath = os.path.join(mAPPath,"input/ground-truth/")

    mAPDetectionPath = os.path.join(mAPPath,"input/detection-results/")

    mAPScriptsPath = os.path.join(mAPPath, "scripts/extra/")

    def wipeFolder(folder):
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

    #wipeFolder(mAPTruthPath)
    #wipeFolder(mAPDetectionPath)

    filePattern = os.path.join(truthPath,"*.xml")
    #print(os.getcwd())
    #print(filePattern)
    #print(filePattern)
    for filename in glob.glob(filePattern):
        drive,pathAndFile = os.path.splitdrive(filename)
        path, xmlFile = os.path.split(pathAndFile)
        newFilename = os.path.join(mAPTruthPath,xmlFile)
        shutil.copyfile(filename,newFilename)
        
    filePattern = 	os.path.join(detectionPath,"*.json")
    for filename in glob.glob(filePattern):
        drive,pathAndFile = os.path.splitdrive(filename)
        path, JSONFile = os.path.split(pathAndFile)
        newFilename = os.path.join(mAPDetectionPath,JSONFile)
        shutil.copyfile(filename,newFilename)
        
    sys.path.append(mAPScriptsPath)
    os.chdir(mAPScriptsPath)
    #print(os.getcwd())
    #from convert_dr_darkflow_jsonF import convertJSON
    #from convert_gt_xmlF import convertXML
    #convertJSON()
    #convertXML()

    sim = imp.load_source('packages', os.path.join(mAPScriptsPath,'convert_dr_darkflow_jsonF.py'))
    method = getattr(sim,'convertJSON')
    method()
    print("(for JSON)")

    sim = imp.load_source('packages', os.path.join(mAPScriptsPath,'convert_gt_xmlF.py'))
    method = getattr(sim,'convertXML')
    method()
    print("(for XML)")

    sys.path.append(mAPPath)
    os.chdir(mAPPath)

    #from mAPValDist import mAPVal
    #print("end Val")
    sim = imp.load_source('packages', os.path.join(mAPPath,'mAPValDist.py'))
    method = getattr(sim,'mAPVal')
    method(20)