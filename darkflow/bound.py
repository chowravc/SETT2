import cv2
from darkflow.net.build import TFNet
import matplotlib.pyplot as plt

#To show this as svg images

# define the model options and run

options = {
    'model': 'cfg/tiny-yolo-voc-3c.cfg',
    'load': 620,                             # 750 is the step number. Can be found in the ckpt folder
    'threshold': 0.01,                       # this number can be higher if the performance is better
    'gpu': 0.0                               # Dont use this if you have no gpu
}

tfnet = TFNet(options)

# read the color image and covert to RGB

img = cv2.imread('images/image_000018.jpg', cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# use YOLO to predict the image
result = tfnet.return_predict(img)

img.shape

# the label below is shown "ace"
print(result)

# pull out some info from the results
for r in result:
	tl = (r['topleft']['x'], r['topleft']['y'])
	br = (r['bottomright']['x'], r['bottomright']['y'])
	label = r['label']
	img = cv2.rectangle(img, tl, br, (255, 0, 0), 1)


# add the box and label and display it
#img = cv2.rectangle(img, tl, br, (0, 255, 0), 1) # draw a ractangle onto an image
#img = cv2.circle(img, tl, 1, (255, 0, 0), -1)
#img = cv2.putText(img, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2) # add laebl name
plt.imshow(img)
plt.show()