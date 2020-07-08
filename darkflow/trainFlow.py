from darkflow.net.build import TFNet
import cv2
import json
import os
import shutil
import sys


def trainFlowCFG(home, runName, darkflowPath, saveRun, model, load, batch, epoch, gpu, learningRate, annotation, labels, dataset):
    ckptPath = 'ckpt'
    checkpointPath = 'ckpt/checkpoint'
    
    if not os.path.exists(ckptPath):
        os.makedirs(ckptPath)

    if not os.path.exists(checkpointPath):
        os.makedirs(checkpointPath)

    #dataset is the image folder
    options = {"model": model,
            "load": load,
            "batch": batch,
            "epoch": epoch,
            "gpu": gpu,
            "train": True,
            "lr": float(learningRate),
            "annotation": annotation,
            "labels": labels,
            "dataset": dataset}
            
    tfnet = TFNet(options)
    print("Options loaded.")
    tfnet.train()
    print("Train completed. Saving run. Please wait...")
    tfnet.savepb()
    print("Saved pb.")

    if saveRun:
        modelPath = model
        path, filename = os.path.split(modelPath)
        name, ext = os.path.splitext(filename)

    pathPB = os.path.join(home, darkflowPath, 'built_graph', name+'.pb')
    pathMeta = os.path.join(home, darkflowPath,'built_graph', name+'.meta')
    savePathPB = os.path.join(home, runName, runName+'.pb')
    savePathMeta = os.path.join(home, runName, runName+'.meta')
    shutil.copyfile(pathPB,savePathPB)
    shutil.copyfile(pathMeta,savePathMeta)