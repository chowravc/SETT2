import numpy as np
import os
import matplotlib.pyplot as plt
import skimage

detRes = os.path.join('input','detection-results','2019-06-12_r4_0800.txt')
gtPath = os.path.join('input','ground-truth','2019-06-12_r4_0800.txt')
csvPath = os.path.join('..','imageData','rmap','rmap','CSV','2019-06-12_r4_0800.dat')

imgPath = '2019-06-12_r4_0800.tif'

defects = np.loadtxt(detRes, delimiter=' ', usecols=(2,3,4,5))
#print(defects)
image = skimage.img_as_float(plt.imread(imgPath))
#fig,ax = plt.subplots()
imgplot = plt.imshow(image, cmap='gray')

xs = []
ys = []
for row in defects:
    x = (row[0]+row[2])/2
    y = (row[1]+row[3])/2
    xs.append(x)
    ys.append(y)
    #print(x)


#defects2 = np.loadtxt(csvPath, delimiter=' ', usecols=(1,2,3,4))
defects2 = np.loadtxt(csvPath, delimiter=' ', usecols=(1,2))

xs2 = []
ys2 = []
for row in defects2:
    x = row[0]
    y = row[1]
    xs2.append(x)
    ys2.append(y)






#plt.plot(xs,ys,'.r')
plt.plot(ys2,xs2,'.b')
    #print(row)

plt.show()