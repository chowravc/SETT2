"""Generate image and annotations of island data."""

import os
import datetime
import shutil
from PIL import Image
import numpy as np
import yaml
from fileConvert import fileConvert


def GenerateImageData(width, height, max_island, r_max=-1, noise_max=1):
    """
    Generate data and annotations for one image.

    Will width x height image matrix with a random number of islands in the
    range [0, max_island] and num_islands x 4 matrix of annotations specified
    as a bounding box coordinates of xmin, ymin, xmax, ymax.
    """
    w, h = width, height

    # Set sane defaults for maxium radius
    if (r_max < 0):
        r_max = min(w/2-1, h/2-1)

    # Make sure the generated circles will not engulf the image
    assert (r_max < w/2 and r_max < h/2), (
        "Maximum radius is too large for image dimensions.")

    # Initialize data with some noise
    data = np.random.random((h, w)) * noise_max
    # Number of islands to generate
    n_island = np.random.randint(1,max_island)
    # Saving coordinate data to compare with future islands: x, y, radius
    coords = np.zeros((n_island, 3))
    # Annotation data: xmin, ymin, xmax, ymax
    annotations = np.zeros((n_island, 4))

    # Generate n_island islands
    for i in range(n_island):

        # Generate random coords and radius until we have no overlaps
        # TODO Add random eccentricity to circles
        while(True):
            # random coords
            X = np.random.randint(0, h)
            Y = np.random.randint(0, w)
            # random radius
            R = np.random.random() * r_max
            break_out = True
            # Check that we are not overlapping with previous islands
            for j in range(i):
                lower_bound = R + coords[j, 2]
                if ((X-coords[j, 0])**2 + (Y-coords[j, 1])**2
                        < lower_bound**2):
                    break_out = False
            # If we are not overlapping, set coords and break
            if break_out:
                coords[i, 0] = X
                coords[i, 1] = Y
                coords[i, 2] = R
                break

        # Set annotation data
        annotations[i, 0] = max(0, coords[i, 0] - np.ceil(coords[i, 2]))
        annotations[i, 1] = max(0, coords[i, 1] - np.ceil(coords[i, 2]))
        annotations[i, 2] = min(799, coords[i, 0] + np.ceil(coords[i, 2]))
        annotations[i, 3] = min(799, coords[i, 1] + np.ceil(coords[i, 2]))

        # Update image data
        xx, yy = np.mgrid[:h, :w]
        circle = (xx - coords[i, 0]) ** 2 + (yy - coords[i, 1]) ** 2
        data[circle < coords[i, 2]**2] = np.random.random()

    return data, annotations


def GenerateImages(config):
    """Generate images from yaml config."""
    # Read parameters
    num_images = config['num_images']
    w = config['width']
    h = config['height']
    max_island = config['max_island']
    r_max = config['max_radius']
    noise_max = config['max_noise']

    # Generate image data
    print("Generating images...")
    for i in range(num_images):
        data, annotations = GenerateImageData(w, h, max_island,
                                              r_max, noise_max)
        np.savetxt("annotations/island_{0:04d}.csv".format(i), annotations,
                   fmt='%d', delimiter=",",
                   header=str(annotations.shape[0]), comments='')
        fileConvert("annotations/island_{0:04d}.csv".format(i),
                    outDir=os.path.join(os.getcwd(), 'annotations'), delim=",",
                    headerLines=1, imageTag='.tif', imgSize=[800, 800])
        data = (data*255).astype('uint8')
        im = Image.fromarray(data,mode='L')
        im.save("images/island_{0:04d}.tif".format(i))
        os.remove("annotations/island_{0:04d}.csv".format(i))
    print("Done!")


def CreateFolders():
    """Create folders for data."""
    def safeMake(dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def safeRemake(dir):
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.makedirs(dir)

    cwd = os.getcwd()
    now = datetime.datetime.now()
    dataDir = os.path.join(cwd, 'dataFolder')
    # safeRemake(dataDir)
    runDir = os.path.join(dataDir, "run%d%d%d_%d%d%d" %
                          (now.year, now.month, now.day,
                           now.hour, now.minute, now.second))
    safeMake(runDir)
    annDir = os.path.join(runDir, 'annotations')
    imDir = os.path.join(runDir, 'images')
    safeMake(annDir)
    safeMake(imDir)
    os.chdir(runDir)
    return


if __name__ == "__main__":
    with open("config.yml", 'r') as ymlfile:
        config = yaml.safe_load(ymlfile)
    CreateFolders()
    GenerateImages(config)
