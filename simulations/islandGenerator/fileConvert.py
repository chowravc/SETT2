import numpy as np
from xml.dom import minidom
import os

def fileConvert(filePath, outDir=None, delim = ' ', headerLines = 0, imageTag = '.jpg', imgSize = [250,250]):
    if outDir == None:
        outDir = os.path.join(os.path.split(filePath)[0],'out')
        
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    imgxS = str(imgSize[0])
    imgyS = str(imgSize[1])
    # Import the CSV into numpy array
    defects = np.loadtxt(open(filePath,'rb'), delimiter=delim, skiprows = headerLines)
    defects = defects.astype(int)

    # Generate the xml file
    doc = minidom.Document()

    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)

    # Generate metadata elements and add them to 'annotation'
    folder = doc.createElement('folder')
    folder.appendChild(doc.createTextNode('images'))
    annotation.appendChild(folder)
    filename = doc.createElement('filename')
    filename.appendChild(doc.createTextNode(os.path.basename(filePath).split('.')[0] + imageTag))
    annotation.appendChild(filename)
    segmented = doc.createElement('segmented')
    segmented.appendChild(doc.createTextNode('0'))
    
    width = doc.createElement('width')
    width.appendChild(doc.createTextNode(imgxS))
    height = doc.createElement('height')
    height.appendChild(doc.createTextNode(imgyS))
    depth = doc.createElement('depth')
    depth.appendChild(doc.createTextNode('3'))
    size = doc.createElement('size')
    size.appendChild(width)
    size.appendChild(height)
    size.appendChild(depth)
    annotation.appendChild(size)
    annotation.appendChild(segmented)

    if len(defects.shape)>1:
        for line in defects:
            # Create defect properties
            xmin = doc.createElement('xmin')
            
            ymin = doc.createElement('ymin')
            xmax = doc.createElement('xmax')
            ymax = doc.createElement('ymax')

            # Create branch elements to be used
            objet = doc.createElement('object')
            bndbox = doc.createElement('bndbox')
            name = doc.createElement('name')
            pose = doc.createElement('pose')
            truncated = doc.createElement('truncated')
            difficult = doc.createElement('difficult')
            
            # Add text data to the elements
            name.appendChild(doc.createTextNode('class'))
            pose.appendChild(doc.createTextNode('center'))
            truncated.appendChild(doc.createTextNode('1'))
            difficult.appendChild(doc.createTextNode('0'))
            
            # Define the Bounding box element
            if line.size == 2: # Basic x,y points
                xmin.appendChild(doc.createTextNode(str(line[0]-5)))
                xmax.appendChild(doc.createTextNode(str(line[0]+5)))
                ymin.appendChild(doc.createTextNode(str(line[1]-5)))
                ymax.appendChild(doc.createTextNode(str(line[1]+5)))
            elif line.size == 3:
                xmin.appendChild(doc.createTextNode(str(line[1]-5)))
                xmax.appendChild(doc.createTextNode(str(line[1]+5)))
                ymin.appendChild(doc.createTextNode(str(line[2]-5)))
                ymax.appendChild(doc.createTextNode(str(line[2]+5)))
            elif line.size == 4:
                xmin.appendChild(doc.createTextNode(str(line[0])))
                xmax.appendChild(doc.createTextNode(str(line[2])))
                ymin.appendChild(doc.createTextNode(str(line[1]-1)))
                ymax.appendChild(doc.createTextNode(str(line[3]+1)))
            else:
                continue
            bndbox.appendChild(xmin)
            
            bndbox.appendChild(ymin)
            bndbox.appendChild(xmax)
            bndbox.appendChild(ymax)
            
            # Add the elements to the defect
            objet.appendChild(name)
            objet.appendChild(pose)
            objet.appendChild(truncated)
            objet.appendChild(difficult)
            objet.appendChild(bndbox)

            # Add the defect to the overall list
            annotation.appendChild(objet)
    else:
        line = defects
                    # Create defect properties
        xmin = doc.createElement('xmin')
        ymin = doc.createElement('ymin')
        xmax = doc.createElement('xmax')
        ymax = doc.createElement('ymax')

        # Create branch elements to be used
        objet = doc.createElement('object')
        bndbox = doc.createElement('bndbox')
        name = doc.createElement('name')
        pose = doc.createElement('pose')
        truncated = doc.createElement('truncated')
        difficult = doc.createElement('difficult')
        
        # Add text data to the elements
        name.appendChild(doc.createTextNode('defect'))
        pose.appendChild(doc.createTextNode('center'))
        truncated.appendChild(doc.createTextNode('1'))
        difficult.appendChild(doc.createTextNode('0'))
        
        # Define the Bounding box element
        if line.size == 2: # Basic x,y points
            xmin.appendChild(doc.createTextNode(str(line[0]-5)))
            xmax.appendChild(doc.createTextNode(str(line[0]+5)))
            ymin.appendChild(doc.createTextNode(str(line[1]-5)))
            ymax.appendChild(doc.createTextNode(str(line[1]+5)))
        elif line.size == 3:
            xmin.appendChild(doc.createTextNode(str(line[1]-5)))
            xmax.appendChild(doc.createTextNode(str(line[1]+5)))
            ymin.appendChild(doc.createTextNode(str(line[2]-5)))
            ymax.appendChild(doc.createTextNode(str(line[2]+5)))
        elif line.size == 4:
            xmin.appendChild(doc.createTextNode(str(line[0])))
            xmax.appendChild(doc.createTextNode(str(line[2])))
            ymin.appendChild(doc.createTextNode(str(line[1]-1)))
            ymax.appendChild(doc.createTextNode(str(line[3]+1)))
        #else:
            #continue
        
        bndbox.appendChild(xmax)
        bndbox.appendChild(ymin)
        bndbox.appendChild(xmin)
        bndbox.appendChild(ymax)
        
        # Add the elements to the defect
        objet.appendChild(name)
        objet.appendChild(pose)
        objet.appendChild(truncated)
        objet.appendChild(difficult)
        objet.appendChild(bndbox)

        # Add the defect to the overall list
        annotation.appendChild(objet)

    fileName = os.path.basename(filePath).split('.')[0]+'.xml'

    xml_str = doc.toprettyxml(indent="    ")
    with open(os.path.join(outDir,fileName),"w") as f:
        f.write(xml_str)


if __name__ == "__main__":
    fileDir = '/home/stian/Documents/Projects/ImageAnnotation/output/test.txt'
    if os.path.isfile(fileDir):
        fileConvert(fileDir,headerLines=1)
    else:
        print(fileDir, ' is not a file')
