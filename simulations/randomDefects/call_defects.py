import os
import datetime
import runSim
import argparse
import shutil

if not os.path.exists('dataFolder'):
    os.makedirs('dataFolder')
os.chdir('dataFolder')

# path = os.getcwd()
# print ("The current working directory is %s" % path)

runName = "run" + datetime.datetime.now().strftime("%y%m%d_%H%M%S")
if not os.path.exists(runName):
    os.makedirs(runName)
os.chdir(runName)

decross=25

if not os.path.exists('data'):
    os.makedirs('data')
if not os.path.exists('im'):
    os.makedirs('im')

# os.chdir('../..')

dataPath = os.getcwd() + "/data"
imPath = os.getcwd() +  "/im"

for x in range(100):
	parser = argparse.ArgumentParser()
	parser.add_argument('decross',nargs='?',help='delta angle of the decrossed polarizers',type = float,default = 0)
	parser.add_argument('dims',nargs='?',help='simulation dimensions [x,y]',type = float,default = [100,100])
	args=parser.parse_args()


	file1 = "out" + str(x) + ".dat"
	file2 = "defect" + str(x) + ".dat"
	file3 = "Image" + str(x) + ".bmp"

	f1 = open(file1,"w+")
	f2 = open(file2,"w+")
	f3 = open(file3,"w+")

	runSim.randomD(args.decross,args.dims,20,[file1,file2,file3])

	f1.close()
	f2.close()
	f3.close()

	path = os.getcwd()

	shutil.move(path + "/" + file1, dataPath + "/" + file1)
	shutil.move(path + "/" + file2, dataPath + "/" + file2)
	shutil.move(path + "/" + file3, imPath + "/" + file3)


