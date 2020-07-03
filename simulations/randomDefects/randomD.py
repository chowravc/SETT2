import numpy as np
import matplotlib.pyplot as plt
import imageio 
import skimage
import random
import argparse

def randomD(decross,dims,nDefects, fileNames):

    """
        Not 100% sure what this is here for, ADAM TAKE A LOOK

        Args:
           decross (str): ADAM
           dims ([int]): Dimensions of image
           nDefects (int): Number of defects I think?
           fileNames (str): Names of files
          
    """

    xDim = dims[0]
    yDim = dims[1]
    beta = np.pi/2+decross/180*np.pi
    def decrossI(beta,image):
        #beta is the angle between pol and anl (90 for completely crossed)
        temp= ( np.sin(image)*np.cos(image)*np.sin(beta)-np.sin(image)**2*np.cos(beta)-np.cos(beta))**2
        return temp/temp.max()
        
    #nDefects = 20
    grid = np.reshape(np.zeros(xDim*yDim),(xDim,yDim))
    dgrid = np.reshape(np.zeros(xDim*yDim),(xDim,yDim))
    ix,iy = np.indices((xDim,yDim))

    def schler(grid):
        return np.sin(2.*grid)**2
    def dGen(grid,x,y,k,off):
        grid = np.mod(grid+k*np.arctan2(ix-x,iy-y)+off,2*np.pi)
        return grid

    for i in np.arange(nDefects):
        dxp = random.randint(0,xDim-1)
        dyp = random.randint(0,yDim-1)

        dxn = random.randint(0,xDim-1)
        dyn = random.randint(0,yDim-1)

        grid = dGen(grid,dxp,dyp,1,random.random()*2*np.pi)
        grid = dGen(grid,dxn,dyn,-1,random.random()*2*np.pi)
        dgrid[dxp,dyp] =1
        dgrid[dxn,dyn] =-1
        
    imageio.imwrite(fileNames[2],skimage.img_as_ubyte(decrossI(beta, grid)))
    np.savetxt(fileNames[0],grid)
    np.savetxt(fileNames[1],dgrid)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('decross',nargs='?',help='delta angle of the decrossed polarizers',type = float,default = 0)
    parser.add_argument('dims',nargs='?',help='simulation dimensions [x,y]',type = float,default = [100,100])
    args=parser.parse_args()
    
    randomD(args.decross, args.dims, 20)