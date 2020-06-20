import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import tkinter as tk
import argparse
import pims

from skimage import data, color

import sys
import matplotlib.animation as animation
import os
def crop(image,startR,startC,square):
    image = color.rgb2grey(image)
    # return image[startR:startR+square,startC:startC+square]
    return image

 
#take filenames of stack

parser =argparse.ArgumentParser(description='Simple Height Measurement of Newtons Ring')
parser.add_argument('videofilenamepath', help='The tiff stack name')
args = parser.parse_args()

(vfilepath,vfilename)=os.path.split(args.videofilenamepath)
#open and store images for use in the application

dataSize=300
cropSize = 600
imageShape = [800,1280]

print("Reading in the video frames...")
#frames = pims.Bioformats(args.stackname)

frames = pims.ImageSequence(args.videofilenamepath+'*.tif', process_func=lambda y: crop(y,imageShape[0]//2-cropSize//2,imageShape[1]//2-cropSize//2,cropSize))
#frames = frames[1000:1200]

print("Done reading in the video frames...")
global pause
pause = True
defects = []
#define simple animation function:
f,(a1,a2) = plt.subplots(nrows=1,ncols=2)
def animate(i):

    frame = frames[i]
    a1.clear()
    a2.clear()
    a1.imshow(frame,cmap='gray')
    a2.imshow(frame,cmap='gray')
#Run GUI

class App_Window:
    def __init__(self,parent):
        #tk.Tk.__init__(self,parent)
        self.parent = parent
        self.frame = tk.Frame(self.parent)
        self.initialize()

    def initialize(self):
        self.go=False
        self.indx = 0
        self.dNum = 0
        self.dList = []
        self.ZoomPoint = 0
        self.bBoxMain = None
        self.bBoxMainP = None
        self.bBoxZoom = None
        self.dX = None
        self.dY= None
        self.cMain = tk.Canvas(self.parent,width=1000,height=00)
        self.cMain.pack()
        self.canvasFig = Figure(figsize=(11,7),dpi=120)
        self.FigSubPlot=self.canvasFig.add_subplot(111)
        self.FigSubPlot.set_axis_off()
        self.imageax = self.FigSubPlot.imshow(frames[0],cmap='gray')
        self.zoomFig = Figure(figsize=(5,5))
        self.zoomSubFig=self.zoomFig.add_subplot(111)
        self.fSlice = frames[0][40:80,40:80]
        self.zImageax = self.zoomSubFig.imshow((self.fSlice-self.fSlice.min())/(self.fSlice.max()-self.fSlice.min()),cmap='gray',vmin=0,vmax=1)
        self.zoomSubFig.set_axis_off()

        self.canvasMain =FigureCanvasTkAgg(self.canvasFig,self.frame)
        self.canvasMain.show()
        self.canvasZoom=FigureCanvasTkAgg(self.zoomFig,self.frame)
        self.canvasZoom.show()
        self.canvasMain.get_tk_widget().pack(side=tk.LEFT)
        self.canvasZoom.get_tk_widget().pack(side=tk.LEFT)
        self.canvasMain.mpl_connect('button_press_event', self.DefectPoint)
        self.canvasZoom.mpl_connect('button_press_event', self.DefectPointSave)
        self.canvasZoom.mpl_connect('key_press_event',self.key)
        #toolbar = NavigationToolbar2TkAgg(self.canvasMain,self.frame)
        #toolbar.update()
        #self.canvasMain._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH, expand=1)
        self.button2 = tk.Button(self.frame,text="next", command= self.next).pack(side=tk.TOP)
        self.button3 = tk.Button(self.frame,text="quit", command= self.close_windows).pack(side=tk.TOP)
        self.frame.pack()
    #def animate_init(self):
    #    self.anim = animation.FuncAnimation(self.canvasFig,animate,interval=20)
    #    print 'test'
    #def animate(self, i):
    #    self.imageax.clear() 
    #    self.imageax.imshow(frames[i],cmap='gray')
    #    self.imageax.draw()
    #    self.imageax.show()
    #    print 'test' 
    def print(self):
        print('print')
    def next(self):

        global frames
        #np.savetxt('output/{}.dat'.format(frames[self.indx].frame_no),np.array(self.dList))
        np.savetxt('output/' + os.path.basename(frames._filepaths[self.indx]).split('.')[0] + '.dat',np.array(self.dList))
        self.indx=self.indx+1
        print('index: {}'.format(frames[self.indx].frame_no))
        try:
            [p.remove() for p in reversed(self.FigSubPlot.patches)]
        except:
            print('no patches')
        bBoxZoom = None
        bBoxMain = None
        self.imageax.set_data(frames[self.indx])
        self.canvasMain.draw()
        self.dNum = 0
        self.dList = []
    def stop(self):
        global pause
        pause= False

    def key(self,event):
        print('pressed'.format((event.key)))
        if (event.key == 's'):
            self.dNum = self.dNum+1
            self.dList.append([self.dNum,self.dX,self.dY])

            self.bBoxMainP = matplotlib.patches.Rectangle((self.dX-10,self.dY-10),20,20,edgecolor='r',facecolor='none')
            self.FigSubPlot.add_patch(self.bBoxMainP)
            self.canvasMain.draw()

        print(self.dList)

    def DefectPoint(self,event):
        row = int(round(event.ydata))
        col = int(round(event.xdata))
        print('clicked at {}, {}'.format(event.xdata,event.ydata))
        self.fSlice = frames[self.indx][row-20:row+20,col-20:col+20]

        if self.bBoxZoom is not None:
            self.bBoxZoom.remove()
            self.bBoxZoom = None
        self.zImageax.set_data( (self.fSlice-self.fSlice.min())/ (self.fSlice.max()-self.fSlice.min()) )
        self.canvasZoom.draw()
        self.ZoomPoint = event

    def DefectPointSave(self,event):
        row = int(round(event.ydata))
        col = int(round(event.xdata))
        print('clicked at {}, {}'.format(event.xdata,event.ydata))
        save = 'n'
        try:
            self.bBoxZoom.remove()
            self.bBoxMain.remove()
        except:
            print('no patches in zoom')
        self.bBoxZoom = matplotlib.patches.Rectangle((col-2,row-2),4,4,edgecolor='r',facecolor='none')
        self.dX =self.ZoomPoint.xdata-20+col
        self.dY =self.ZoomPoint.ydata-20+row
        self.zoomSubFig.add_patch(self.bBoxZoom)
        self.canvasZoom.draw()


        #if (save == 'y'):
        #    self.dNum = self.dNum+1
        #    self.dList.append([self.dNum,row,col])


    def close_windows(self):
        print(self)
        np.savetxt('output/out.dat',np.array(self.dList),fmt='%1.0f')
        self.parent.destroy()
        sys.exit()

root = tk.Tk()
    
MainWindow=App_Window(root)
root.mainloop()
plt.close('all')
