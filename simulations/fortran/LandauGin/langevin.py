import numpy as np
import matplotlib.pyplot as plt
import random as rand

def YNoise(T):
   l = rand.random()-.5 #should be -.5 to .5
   return l*2*np.pi*T

def PNoise(T):
    l = rand.random()-.5
    return np.sqrt(24*T)*l


