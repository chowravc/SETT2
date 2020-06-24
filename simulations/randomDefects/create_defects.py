#!/bin/bash
import sys
import os
import datetime
import shutil
import random
import joblib
from joblib import Parallel,delayed

def create_defects(numImages,dims,numDefects):
    baseDir = os.getcwd()
    dims.reverse()
    def safeMake(dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
    def safeRemake(dir):
        if os.path.exists(dir):
            shutil.rmtree(dir)
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
    from randomD import randomD

    def process(i,defects):
        #print(i)
        outdat = os.path.join(dataDir2,'out%d.dat' %(i))
        defectdat = os.path.join(dataDir2,'defect%d.dat' %(i))
        img = os.path.join(imDir,'image%d.bmp' %(i))
        randomD(decross,dims,defects, [outdat,defectdat,img])
    print(joblib.__version__)
    Parallel(n_jobs=-1)(delayed(process)(i, random.randint(numDefects[0],numDefects[1])) for i in range(0,numImages))

    '''
    for i in range(0,numImages):
        print(i)
        outdat = os.path.join(dataDir2,'out%d.dat' %(i))
        defectdat = os.path.join(dataDir2,'defect%d.dat' %(i))
        img = os.path.join(imDir,'image%d.bmp' %(i))
        randomD(decross,dims,numDefects[0]+i, [outdat,defectdat,img])
    '''
    os.chdir(baseDir)
if __name__ == "__main__":
    create_defects(10,[300,300],[10,40])

