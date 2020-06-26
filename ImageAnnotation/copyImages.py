from shutil import copyfile
import os

i = 400
path = '/home/stian/Documents/remote/2019-06-12/'
dataSet = '2019-06-12'
dataRound = 'r2'

sourceDir = os.path.join(path,dataRound)
destDir = os.path.join(path,dataRound,'annotations')
# destDir = '/home/stian/Desktop/testVid'

if not os.path.isdir(destDir):
  os.mkdir(destDir)

while i <=6000:
  if i < 1000:
    imgFile = dataRound + '_0' + str(i) + '.tif'
  else:
    imgFile = dataRound + '_' + str(i) + '.tif' 
  sourcePath = os.path.join(sourceDir,imgFile)
  destPath = os.path.join(destDir,dataSet + '_' +imgFile)
  if os.path.isfile(sourcePath):
    copyfile(sourcePath,destPath)
  i = i + 300

