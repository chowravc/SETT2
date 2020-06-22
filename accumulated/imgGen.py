import numpy as np
import matplotlib.pyplot as plt
import glob as glob
import skimage
import imageio
import argparse
import random


def decrossI(beta,image):
    #beta is the angle between pol and anl (90 for completely crossed)
    temp= ( np.sin(image)*np.cos(image)*np.sin(beta)-np.sin(image)**2*np.cos(beta)-np.cos(beta))**2
    return temp/temp.max()

def schler(angle):
    return np.sin(2.*angle)**2.
def imgGen(decross):
    beta = (np.pi/2+decross/180*np.pi)
    names = glob.glob('accumulated/*out*.dat')
    frames = [decrossI(beta,np.loadtxt(n)) for n in names]
    
    names = [n.replace('out', 'defect') for n in names]
    
    [imageio.imwrite(n.split('.')[0]+'.jpg',skimage.img_as_ubyte(im)) for n,im in zip(names,frames)]


def imgGenRand(decrossMin,decrossMax):
    decrossMean = (decrossMin+decrossMax)/2
    decrossDiff = decrossMax-decrossMin
    
    names = glob.glob('*out*.dat')
    decross = np.random.rand(len(names))*decrossDiff+(decrossMean-decrossDiff/2)
    betas = np.pi/2+decross/180*np.pi
    frames = [decrossI(beta,np.loadtxt(n)) for (beta,n) in zip(betas,names)]
    
    names = [n.replace('out', 'defect') for n in names]
    
    [imageio.imwrite(n.split('.')[0]+'.jpg',skimage.img_as_ubyte(im)) for n,im in zip(names,frames)]
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('decross',nargs='?',help='delta angle of the decrossed polarizers',type = float,default = 0)
    args=parser.parse_args()
    decross = args.decross
    imgGen(decross)
