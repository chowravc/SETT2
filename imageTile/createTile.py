import cv2
import os
import glob
from PIL import Image
import numpy as np

def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

def doTile(inputFolder, outputFolder, level, imgExt):
	"""Break selected image into 4 tiles.

    Args:
        inputFolder (str): image input directory
        outputFolder (str): image output directory
        level (int): current level of tiling
        imgExt (str): extension of image files to tile without the dot

    Writes:
        *.<ext>: tiled data image files written to <base>/data/collated/annotations/corrected/<tile_level> where base is the directory containing sett2

    Note:
        If folder exists, tiling will fail

    """

	filePattern = os.path.join(inputFolder,"*." + imgExt)
	i = 1

	for filename in glob.glob(filePattern):

		#print("Image " + repr(i) + ".")

		im = np.array(Image.open(filename))
		#im = Image.open(filename)

		if im.max() > 255:
			im = (np.array(Image.open(filename))//16).astype('uint8')

		imageName = filename.split(".")[0].split("\\")[-1]

		iN1 = outputFolder + imageName + "_1." + imgExt
		iN2 = outputFolder + imageName + "_2." + imgExt
		iN3 = outputFolder + imageName + "_3." + imgExt
		iN4 = outputFolder + imageName + "_4." + imgExt

		width, height = len(im[0]), len(im)
		xmid = width // 2
		ymid = height // 2

		im1 = im[0:ymid, 0:xmid]
		im2 = im[0:ymid, xmid:width]
		im3 = im[ymid:height, 0:xmid]
		im4 = im[ymid:height, xmid:width]

		cv2.imwrite(iN1, im1)
		cv2.imwrite(iN2, im2)
		cv2.imwrite(iN3, im3)
		cv2.imwrite(iN4, im4)

		i += 1

def tileImage(tilingLevel, imgFolder, imgExt):
	"""Break enchanced images into 4 tiles.

    Args:
        tilingLevel (int): number of times to do tiling.
        imgCorrectedFolder (str): folder containing corrected images
        imgExt (str): extension of image files to tile without the dot

    Writes:
        *.<ext>: tiled data image files written to <base>/data/collated/annotations/<tile_level> where base is the directory containing sett2

    Note:
        If folder exists, tiling will fail

    """

	level = 0

	tile = "tile_"

	outputFolder = imgFolder

	while level < tilingLevel:

		level += 1

		print()
		print("Tiling level " + repr(level))

		inputFolder = outputFolder
		outputFolder = inputFolder + tile + repr(level) + "/"

		os.mkdir(outputFolder)

		doTile(inputFolder, outputFolder, level, imgExt)