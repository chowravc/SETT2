import os
import sys
import imp



def simulate(runName, numImages, imageDims, maxDefects, minDefects, decrossMin, decrossMax):
    """This runs a simulation to generate trianing data based on the parameters passed

        :param runName: Used as the folder name for saving generated images
        :type runName: str, unless told otherwise in the form of 'run DD/MM/YY/hh/mm/ss'
        :param numImages: the number of images to generate
        :type numImages: int, optional
        :param imageDims: dimensions of images to create 
        :type imageDims: int pairs, optional
        :param maxDefects: The maximum amount of defects a generated image can have
        :type maxDefects: int, optional
        :param minDefects: The minimum amount of defects that can be present in a generated image
        :type minDefects: int, optional
        :param decrossMin: An unused prameter for something - will add use later - ADAM LOOK HERE
        :type decrossMin: float, optional
        :param decrossMax: An unused prameter for something - will add use later - ADAM LOOK HERE
        :type decrossMax: float, optional
    """

    # Args:
    #     runName (str): the name of the directory the output of this function will be stored in. If it already exists, nothing will be overwritten
    #     numImages (int): number of images the function should create
    #     imageDims (list): dimensions of the images to be simulated as [x, y]
    #     maxDefects (int): maximum number of defects an image can have
    #     minDefects (int): minimum number of defects an image can have
    #     decrossMin (int): minimum "Hourglass-ness" of a defect UPDATE
    #     decrossMax (int): maximum "Hourglass-ness" of a defect UPDATE

    # Writes:
    #     *_defect*.dat: Writes defect location data files to ../sett2/<runName>
    #     *_out*.dat: Writes spin data files to ../sett2/<runName>
    #     *_defect*.jpg: Writes images of the schlieren texture to ../sett2/<runName>
    #     *_defect*.txt: *defect*.dat converted to txt written to ../sett2/<runName>
    #     *_defect*SIMMARKED.jpg: Writes images of schlieren texture with annotated defects to ../sett2/<runName>/SIMMARKED
    #     *_defect*.xml: Writes defect bounding boxes in .xml format for YOLO training to ../sett2/<runName>/out

    # Note:
    #     Creates *out*.dat files storing spins of individual molecules, *defect*.dat with defect locations marked.
    #     Also creates .jpg files containing the schlieren texture, the same images with annotated defect locaions and
    #     .xml files with defect locations to be used by YOLO.

    simString = 'simulations/randomDefects/runSim.py' # Path containing the runSim module.
    functionName = 'runSim' # Name of function being instantiated in runSim.

    home = os.getcwd() + '/defectSimulation/' # Home directory of sett2.

    print("Running Simulation")

    path, exFile = os.path.split(simString) # Splitting path and runSim.py.
    fullPath = os.path.join(home, path) # Creating full path for runSim.py.
    sys.path.append(fullPath) # Adding simulation directory to PATH.
    os.chdir(fullPath) # Changing directory to simulation.

    # Importing the module runSim.
    sim = imp.load_source('packages', exFile)

    # Importing the function in runSim.
    runSimulation = getattr(sim,functionName)

    # Calling function to simulate.
    runSimulation(home, runName, numImages, imageDims, maxDefects, minDefects, decrossMin, decrossMax)

    # Changing directory back to home.
    os.chdir(home)

def extractSmartNoise(crop, cropManual, cropX, cropY):
    """Extract noise .jpg files from experimental images as .bmp files

    Args:
        crop (bool): Decide whether the experimental images should be cropped before extracting noise
        cropManual (bool): Decide whether all images should be cropped manually with individual limits
        cropX (int): crop width used when cropManual is False
        cropY (int): crop height used when cropManual is False

    Writes:
        noise*.jpg: Noise image files written to ../sett2/smartNoise/noiseSamples/noiseFiles

    Note:
        Input .bmp experimental images in the folder ..sett2/smartNoise/noiseSamples and decide 
        the region being used with cropping parameters. Noise will be extracted and images will be created 
        at ../sett2/smartNoise/noiseSamples/noiseFiles as .jpg files.

    """

    # Path containing the noiseExtractor module in sett2.
    path = "/smartNoise/"

    # Path containing .bmp experimental images.
    noiseSamplePath = "/smartNoise/noiseSamples/"

    # Home directory of sett2.
    home = os.getcwd() + '/defectSimulation/'

    print("Extracting Smart Noise")

    # Path of noiseExtractor function.
    functionPath = home + path
    
    # Importing the module noiseExtractor.
    noiseExtraction = imp.load_source('packages', os.path.join(functionPath,'noiseExtractor.py'))
    
    # Calling function noiseExtractor.
    noiseExtraction.noiseExtractor(home, noiseSamplePath, crop, cropManual, cropX, cropY)


def enchanceImages(runName, imgMean, imgStd, gaussian, doSmartNoise, smartNoise, numCircles, addGrid, gridRange, stds):
	"""Enchance simulation images with various types of noise (including smart noise), bright circles, grids and standardisation to be used for training

    Args:
        runName (str): decides the simulation run that will have its images enchanced
        imgMean (list): choose the mean intensity an image can have; a list of two floats [x, y] with x lesser than or equal to y and both lesser than 1
        imgStd (list): choose the range of intensity ranges an image can have; a list of two floats [x, y] with x lesser than or equal to y and both strictly greater than 0
        gaussian (list): range of gaussian in units of sigma; a list of two floats [x, y] with x lesser than y
        doSmartNoise (bool): choose whether or not to add smart noise to simulated images
        smartNoise (list): range of intensity of smart noise; a list of two floats [x, y] with x lesser than or equal to y
        numCircles (int): choose how many bright circles to add to the simulated images; 0 to not add any
        addGrid (bool): splits the image into four random quadrants with random intensities
        gridRange (float): range over which quadrants can be brightened or dimmed
        stds (int): choose the intensity range an image can have

    Writes:
        *_defect*.jpg: enchanced simulation image files written to ../sett2/<runName>/enchanced

    Note:
        To run this with smartNoise, first extractSmartNoise() needs to be run and noise files must be generated

    """
	print("Enhancing Simulation Images")

	# Home directory of sett2.
	home = os.getcwd() + '/defectSimulation/'

	# Path to addArtifacts.py
	path = home + "/artifacts/"

	# Path to smart noise image files.
	smartNoisePath = "smartNoise/noiseSamples/noiseFiles"

	# Loading addArtifacts.py.
	artifacts = imp.load_source('packages', os.path.join(path,'addArtifacts.py'))

	# Calling function addArtifacts.
	artifacts.addArtifacts(home, runName, imgMean, imgStd, gaussian, doSmartNoise, smartNoisePath, smartNoise, numCircles, addGrid, gridRange, stds)


def correctImages(imgExt, selectBox, autoBox, crop, stds):
	"""Enchance data images with various types of noise (including smart noise) and standardisation to prepare them for running model

    Args:
        imgExt (str): extension of images to be corrected
        selectBox (bool): selects a box to base correction on
        autoBox (bool): uses crop to automatically box part of image
        crop (list): [[x1, x2], [y1, y2]] selects x and y crop limits for autoBox
        stds (float): decides dynamic range of the image

    Writes:
        *.<ext>: corrected data image files written to <base>/data/collated/annotations/corrected where base is the directory containing sett2

    Note:
        First run this function to generate the directory structure to place images into

    """
	print("Correcting Images")

	# Home directory of sett2.
	home = os.getcwd() + '/defectSimulation/'

	# Path to smart noise.
	path = home + "/smartNoise/"

	# Default data image folder.
	imgFolder = "../data/collated/annotations"

	# Loading correctImages.py.
	correct = imp.load_source('packages', os.path.join(path,'correctImages.py'))

	# Calling function correctImages.
	correct.correctImagesCFG(home, imgFolder, imgExt, selectBox, autoBox, crop, stds)