import subprocess
import os
import shutil 
import sys
import glob
import stat
import random
import imp
import re
from datAnnotate import datAnnotate
from joblib import Parallel,delayed



def runSim(cfg):

  def genAnnotations(targetLocation,cfg):

    fileConvertPath = os.path.join(cfg['temp']['rootDir'],cfg['paths']['fileConvert'])
    print("Generating xml files")
    sys.path.append(fileConvertPath)
    from fileConvertBatch import fileConvertBatch
    fileConvertBatch(targetLocation,[cfg['simulation']['xDim'],cfg['simulation']['xDim']],'txt')

  def simulate(targetLocation,k,beta,mu,N,endT,seed,cfg):

    startDir = os.getcwd()

    simDir = os.path.join(os.getcwd(),'tmpFolder',str(seed))
    targetLocation = os.path.join(os.getcwd(),targetLocation)
    setupEnvironment(simDir)

    try:
      performSimulation(simDir,k,beta,mu,N,endT,seed,cfg)
      moveFiles(simDir,targetLocation,seed,cfg['simulation']['minTimeLim'])
      genAnnotations(targetLocation,cfg)
      cleanupDirectory(simDir)
    except:
      print(sys.exc_info()[0])
      cleanupDirectory(simDir)

    os.chdir(startDir)
    
  def setupEnvironment(simDir):
    sourceDir = os.path.dirname(os.path.realpath(__file__))
    if os.path.exists(simDir):
      shutil.rmtree(simDir)
    
    os.mkdir(simDir)
    #shutil.copyfile(os.path.join(sourceDir,'fortran','LandauGin','defectT.o'), os.path.join(simDir,'defectT.o'))

    subprocess.run(['gfortran','-O3','-o',os.path.join(sourceDir,'fortran','LandauGin','defect.o'),os.path.join(sourceDir,'lg.f90')])
    shutil.copyfile(os.path.join(sourceDir,'defect.o'), os.path.join(simDir,'defect.o'))
    shutil.copyfile(os.path.join(sourceDir,'imgGen.py'), os.path.join(simDir,'imgGen.py'))

  def performSimulation(simDir,k,beta,mu,N,endT,seed,cfg):
    curDir = os.getcwd()
    os.chdir(simDir)

    #subprocess.run(['sudo','chmod','+x','tmpFolder/defect.o'])
    #subprocess.run(['chmod','+x','tmpFolder/defectT.o'])
    #print('here')
    os.chmod('defect.o',0o777)
    #subprocess.run(['chmod','+x','defect.o'])

    tmp = subprocess.run(['./defect.o',str(k),str(beta),str(mu),str(N),str(endT),str(seed)])

    #shutil.copyfile('imgGen.py',os.path.join(outDir,'imgGen.py'))
    print("Generating Images")
    sys.path.append(simDir)
    from imgGen import imgGenRand
    imgGenRand(50,50)
    print("Generating txt files")
    datAnnotate(simDir)

    from markSim import markSim
    print("Generating Simulation Annotated Images")
    markSim(simDir)
    
    #subprocess.run(['python','imgGen.py'])

    os.chdir(curDir)

  def extractNum(item):
      filename = os.path.basename(item)
      numbers = re.findall("(\d+)",filename)
      if len(numbers)>0:
        numberString = numbers[0]
        number = int(numberString)
      else: number = 1000000 #not a numbered file
      return number

  def moveFiles(simDir,targetLocation,seed,minTime):
    tmp = os.getcwd()
    os.chdir(simDir)
    if not os.path.exists(targetLocation):
      try:
        os.mkdir(targetLocation)
      except:
        print("Failed to generate target directory")
        return
    #subprocess.run(["mv *.dat "+targetLocation])
    #subprocess.run(["mv *.bmp "+targetLocation])
    
    for item in glob.glob('*.dat'):
      number = extractNum(item)
      if number>minTime:
        shutil.move(item,os.path.join(targetLocation,str(seed)+os.path.basename(item)))

    for item in glob.glob('*.txt'):
      number = extractNum(item)
      if number>minTime:
        shutil.move(item,os.path.join(targetLocation,str(seed)+os.path.basename(item)))
    

    imageGlob = glob.glob('*.bmp') + glob.glob('*.jpg')
    for item in imageGlob:
      number = extractNum(item)
      if number>minTime:
        shutil.move(item,os.path.join(targetLocation,str(seed)+os.path.basename(item)))
    os.chdir(tmp)
    

  def cleanupDirectory(simDir):
    return
    shutil.rmtree(simDir)
  def jank(i):
    print(str(i))

  



  if cfg['simulation']['erasePrevious'] and os.path.exists('dataFolder'):
    shutil.rmtree('dataFolder')

  if not os.path.exists('tmpFolder'):
    os.mkdir('tmpFolder')
  tmin = cfg['simulation']['tmin']
  tmax = cfg['simulation']['tmax']
  imSize = cfg['simulation']['xDim']
  endT = cfg['simulation']['endT']
  #Parallel(n_jobs=-1, backend='loky',verbose=11)(delayed(jank)(i) for i in range(0,20))
  Parallel(n_jobs=-1, backend='loky',verbose=11)(delayed(simulate)('dataFolder',1,random.randint(tmin,tmax),0,imSize,endT,random.randint(0,1000000),cfg) for i in range(0,cfg['simulation']['numRuns']))
    #simulate('dataFolder',1,random.randint(tmin,tmax),0,imSize,endT,random.randint(0,100000),cfg)

  cleanupDirectory('tmpFolder')

if __name__ == "__main__":

  simulate('dataFolder',1,10,0,200,300,random.randint(0,100000))
