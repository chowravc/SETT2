import cv2
import os
import glob
from PIL import Image
import numpy as np



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

		im = Image.open(filename)

		imageName = filename.split(".")[0].split("\\")[-1]

		iN1 = outputFolder + imageName + "_1." + imgExt
		iN2 = outputFolder + imageName + "_2." + imgExt
		iN3 = outputFolder + imageName + "_3." + imgExt
		iN4 = outputFolder + imageName + "_4." + imgExt

		width, height = im.size
		xmid = width // 2
		ymid = height // 2

		im1 = im.crop((0, 0, xmid, ymid))
		im2 = im.crop((xmid, 0, width, ymid))
		im3 = im.crop((0, ymid, xmid, height))
		im4 = im.crop((xmid, ymid, width, height))

		im1.save(iN1)
		im2.save(iN2)
		im3.save(iN3)
		im4.save(iN4)

		i += 1

def tileImage(tilingLevel, imgCorrectedFolder, imgExt):
	"""Break enchanced images into 4 tiles.

    Args:
        tilingLevel (int): number of times to do tiling.
        imgCorrectedFolder (str): folder containing corrected images
        imgExt (str): extension of image files to tile without the dot

    Writes:
        *.<ext>: tiled data image files written to <base>/data/collated/annotations/corrected/<tile_level> where base is the directory containing sett2

    Note:
        If folder exists, tiling will fail

    """

	level = 0

	tile = "tile_"

	outputFolder = imgCorrectedFolder

	while level < tilingLevel:

		level += 1

		print()
		print("Tiling level " + repr(level))

		inputFolder = outputFolder
		outputFolder = inputFolder + tile + repr(level) + "/"

		os.mkdir(outputFolder)

		doTile(inputFolder, outputFolder, level, imgExt)