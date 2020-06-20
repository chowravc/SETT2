import numpy
import glob


def datAnnotate():
    folder = 'accumulated/'
    files = glob.glob(folder+'*defect*.dat')
    #print(len(files))
    #filename = 'E:\\Projects\\fake\\simulations\\fortran\\LandauGin\\run20190529_131519\\data-k-1.00-beta-10.000-mu-0.000\\defect74.dat'
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
        #print(outFile)
        f = open(outFile, "w")
        f.write('{}\r\n'.format(numDefects))

        for i in range(numDefects):
            f.write('{} {} {} {}\r\n'.format(y[i]-5,x[i]-5,y[i]+5,x[i]+5))


    #print(x.shape[0])