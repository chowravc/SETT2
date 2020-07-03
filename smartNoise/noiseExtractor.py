import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
import argparse
import os
import skimage
from PIL import Image
from skimage.transform import AffineTransform, warp
import cv2
import glob as glob
import matplotlib.patches as patches
import yaml


def standardize(image):
	"""Stadardise the average brightness and dynamic range of an image

	Args:
	image (image): input a image as tensor to be standardised

	Returns:
	image: Standardised image

	Note:
	Hard-coded to output a dynamic range of 6 sigmas

	"""
	image = image.astype(np.float64)
	imgMean = np.mean(image)
	imgSTD = np.std(image)
	image= (image - imgMean)/(6*imgSTD)
	image = image+0.5
	image = np.clip(image,0,1)
	return image

class getter:
	"""Needs further inspection
	"""
	def __init__(self,ax,fig):

		self.numClicks = 0
		self.x = [0,0]
		self.y = [0,0]
		self.ax = ax
		self.fig = fig
		self.figsize = fig.get_size_inches()*fig.dpi
		self.rect = patches.Rectangle((1,1),0,0,linewidth=1,edgecolor='r',facecolor='none')
		self.ax.add_patch(self.rect)
		self.fig.canvas.mpl_connect('button_press_event',self.click)
		self.fig.canvas.mpl_connect('motion_notify_event',self.move)

	def click(self,event):

		self.x[self.numClicks] = event.xdata
		self.y[self.numClicks] = event.ydata

		if self.numClicks > 0:
			plt.close()

		self.numClicks = self.numClicks+1

	def move(self,event):

		if self.numClicks >0:

		    mouseX = event.xdata
		    mouseY = event.ydata

		    if mouseX is not None:

		        clickX = self.x[0]
		        clickY = self.y[0]

		        xsort = [mouseX,clickX]
		        ysort = [mouseY,clickY]
		        xsort.sort()
		        ysort.sort()

		        dif = min(xsort[1]-xsort[0],ysort[1]-ysort[0])

		        self.rect.remove()
		        self.rect = patches.Rectangle((xsort[0],ysort[0]),dif,dif,linewidth=1,edgecolor='r',facecolor='none')
		        self.ax.add_patch(self.rect)
		        self.fig.canvas.draw()

def boxZero(image,sideLength):
	"""Creates a box centred at the centre of the image.

	Args:
	image: an image as an array or tensor
	sideLength (int): side length of box centred around the centre of image

	Returns:
	image: image as array or tensor with dark box added
	"""

	center = [i//2 for i in image.shape]
	image[center[0] - sideLength:center[0] + sideLength, center[1] - sideLength:center[1] + sideLength] = 0

	return image

def extractNoise(image,boxSize):
	"""Extracts noise from image from within a box.

	Args:
	image: an image as an array or tensor
	boxSize (int): side length of box centred around the centre of image

	Returns:
	noiseR: noise image as array or tensor
	"""

	imShape = image.shape
	r = imShape[0]
	c = imShape[1]

	if len(imShape) >2:
		image = image[:,:,1]

	imgF = fftpack.fft2(image)
	imgFS = fftpack.fftshift(imgF)
	noiseSF = boxZero(imgFS, boxSize)
	noiseF = fftpack.ifftshift(noiseSF)
	noise = fftpack.ifft2(noiseF)
	noiseR = np.real(noise)

	return noiseR

def skewImage(image,shift):
	"""Skews an image to a direction.

	Args:
	image: an image as an array or tensor
	shift (int): value of shift

	Returns:
	rotated: NEEDS INVESTIGATION
	"""
	transform = AffineTransform(translation=shift)
	shifted = warp(image,transform, mode ='wrap', preserve_range =True)
	shifted = shifted.astype(image.dtype)

	return rotated

def rgb2gray(rgb):
	"""Converts an rgb image tensor to tensor.
	Args:
	rgb: an image as a tensor of rgb (no alpha)

	Returns:
	gray: image as array in grayscale
	"""

	r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
	gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

	return gray

def noiseExtractor(home, noiseSamplePath, crop, cropManual, cropX, cropY):
	"""Validate model on a dataset through mAP

	Args:
	home (str): home directory of sett2
	noiseSamplePath (str): path to noise sample images

	Writes:
	noise: noise image files written to ../sett2/smartNoise/noiseSamples/noiseFiles where base is the directory containing sett2

	Note:
	Put data image .tif files ../sett2/smartNoise/noiseSamples to extract noise
	"""
	filepath = home + noiseSamplePath
	doCrop = crop
	paths = glob.glob(filepath+'/*.bmp')

	iterator = 1
	for path in paths:     
		image = skimage.img_as_float(plt.imread(path))
		dims = image.shape

	if doCrop:
	    if cropManual:
	        if iterator == 1:
	            
	            fig,ax = plt.subplots()
	            imgplot = ax.imshow(image)
	            getter1 = getter(ax,fig)
	            plt.show()

	            x = getter1.x
	            y = getter1.y

	            x.sort()
	            y.sort()

	            for i in range(0,len(x)):
	                x[i] = int(x[i])

	            for i in range(0,len(y)):
	                y[i] = int(y[i])
	            first = 0

	            xLen = abs(x[1]-x[0])
	            yLen = abs(y[1]-y[0])
	            minLen = min(xLen,yLen)

	            x[1] = x[0] +minLen
	            y[1] = y[0] +minLen
	    else:
	        x = cropX
	        y = cropY
	        
	else:
	    
	    x = [0,dims[0]]
	    y = [0,dims[1]]

	if len(dims)>2:

	    image = rgb2gray(image)

	croppedImg = image[y[0]:y[1],x[0]:x[1]]
	image = croppedImg

	noise = extractNoise(image,100)
	noise = standardize(noise)

	h,w = noise.shape
	im = Image.fromarray(noise*255)

	outFolder = filepath+'/noiseFiles/'
	if not os.path.exists(outFolder):
	    os.makedirs(outFolder)

	if im.mode != 'RGB':
	    im = im.convert('RGB')
	im.save(outFolder+'noise'+str(iterator)+'.jpg')
	iterator = iterator+1