import os
import numpy
import glob

def datAnnotate(home, runName):
    reset = os.getcwd()
    os.chdir(home+"/"+runName)
    files = glob.glob('*defect*.dat')
    for file in files:
        fExt = file.split('.')
        fpath = fExt[:-1]
        #print(fpath)
        outFile = '.'.join(fpath)+'.txt'
        data = numpy.loadtxt(file)

        locs = numpy.where(abs(data)==1)
        x = locs[0]
        y = locs[1]

        numDefects = x.shape[0]
        f = open(outFile, "w")
        f.write('{}\r\n'.format(numDefects))

        for i in range(numDefects):
            f.write('{} {} {} {}\r\n'.format(y[i]-5,x[i]-5,y[i]+5,x[i]+5))
    os.chdir(reset)