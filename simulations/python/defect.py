'''FrankDefect Code: Use the metropolis algorithm to generate a system of annealing liquid crystal smectic defects'''

import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

def stateGen(N):
    '''Generates random state on an NxN grid
    '''
    state = np.random.uniform(0,2*np.pi,size=(N,N))
    return state
def frankNN(xVec, yVec, X,K=1):
    '''calculate the frank free energy at site i,j
    xVec = [state[i-1,j],state[i,j],state[i+1,j]
    yVec = xVec sub j<->i
    '''
    
def hamXY(xVec,yVec,g=1):
    return -g*(np.sum(np.cos(np.diff(xVec)))+np.sum(np.cos(np.diff(yVec))))

def metro(prevState,N,beta):
    '''metropolis algorithm
    1. Takes in state S
    2. Randomally flips site S
    3. Calculate energy diff
    4. Takes it if it meets criteria
    '''
    state = prevState.copy()
    for i in range(N):
        for j in range(N):
            theta = state[i,j]
            thetaP = theta+np.random.uniform(-2,2)
            xNN = [state[(i-1)%N,j],theta,state[(i+1)%N,j]] 
            xNNP = [state[(i-1)%N,j],thetaP,state[(i+1)%N,j]] 
            yNN = [state[i,(j-1)%N],theta,state[i,(j+1)%N]] 
            yNNP = [state[i,(j-1)%N],thetaP,state[i,(j+1)%N]] 
            delE =hamXY(xNN,yNN)- hamXY(xNNP,yNNP)
            #print(delE)
            #Decide to switch or not
            if delE <0:
                state[i,j]=thetaP
            elif np.random.rand() < np.exp(-delE*beta):
                state[i,j]=thetaP
    return state
def schler(state):
    '''take given state and return schieren state
    '''
    return np.sin(state)**2
def showState(state):
    '''Plot given grid'''
    N = state.shape[0]
    fig,ax =plt.subplots()
    X, Y = np.meshgrid(range(N), range(N))
    ax.pcolormesh(X, Y, state, cmap=plt.cm.gray);
    plt.show()
def showStateHR(state):
    '''Plot given grid'''
    N = state.shape[0]
    fig,ax =plt.subplots()
    plotGrid = np.linspace(0,N,300)
    XX,YY = np.meshgrid(plotGrid,plotGrid)
    X,Y = np.meshgrid(range(N),range(N))
    configHighRes = griddata((X.ravel(),Y.ravel()),state.ravel(),(plotGrid[None,:],plotGrid[:,None]),method='linear')

    ax.pcolormesh(XX, YY, configHighRes, cmap=plt.cm.gray);
    plt.show()
   
def configPlot(f,config,i,N,n_):
    X,Y = np.meshgrid(range(N),range(N))
    sp = f.add_subplot(3,3,n_)
    plt.setp(sp.get_yticklabels(),visible=False)
    plt.setp(sp.get_xticklabels(),visible=False)
    plt.pcolormesh(X,Y,schler(config),cmap=plt.cm.gray);
    plt.title('Time=%d'%i);plt.axis('tight')

def configPlotHighRes(f,config,i,N,n_):
    plotGrid = np.linspace(0,N,300)
    X,Y = np.meshgrid(range(N),range(N))
    configHighRes = griddata((X.ravel(),Y.ravel()),config.ravel(),(plotGrid[None,:],plotGrid[:,None]))
    XX,YY = np.meshgrid(plotGrid,plotGrid)
    sp = f.add_subplot(3,3,n_)
    plt.setp(sp.get_yticklabels(),visible=False)
    plt.setp(sp.get_xticklabels(),visible=False)
    plt.pcolormesh(XX,YY,schler(configHighRes),cmap=plt.cm.gray);
    plt.title('Time=%d'%i);plt.axis('tight')


def simulate():
    N, temp = 64,.4
    l = []
    state = stateGen(N)
    f = plt.figure(figsize=(15,15),dpi=80)
    configPlot(f,state,0,N,1)
    timeSteps = 1001
    for i in range(timeSteps):
        if i%10 == 1:
            print(i)
        state=metro(state,N,1./temp)
        if i ==1:       
            configPlotHighRes(f, state,i,N,2)
            l.append(state)
            #print(state)
            print(l)
        if i ==4:       
            configPlotHighRes(f, state,i,N,3);
            l.append(state)
        if i ==32:       
            configPlotHighRes(f, state,i,N,4);
            l.append(state)
        if i ==100:       
            configPlotHighRes(f, state,i,N,5);
            l.append(state)
        if i ==1000:       
            configPlotHighRes(f, state,i,N,6);
            l.append(state)
    return l
