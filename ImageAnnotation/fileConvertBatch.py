import glob
import os
from fileConvert import fileConvert

def fileConvertBatch(targetDir,imgDims, ext='all'):
    
    filePatternCustom = os.path.join(targetDir, '*defect*.dat')
    filePatternTXT = os.path.join(targetDir, '*.txt')
    filePatternDAT = os.path.join(targetDir, '*.dat')
    if ext == 'all':
        files = (glob.glob(filePatternTXT)+glob.glob(filePatternDAT))
    elif ext =='txt':
        files = glob.glob(filePatternTXT)

    elif ext =='dat':
        files = glob(filePatternDAT)

    elif ext =='custom':
        files = glob.glob(filePatternCustom)

    for filename in files:
        fileConvert(filename,headerLines=1,imgSize=imgDims)

if __name__ == "__main__":
    imgDims = [100,100]
    targetDir = "E:/Projects/fake/simulations/fortran\LandauGin/run20190529_144637/data-k-1.00-beta-10.000-mu-0.000"
    fileConvertBatch(targetDir,imgDims)