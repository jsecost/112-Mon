import cs112_f22_week8_linter
from cmu_112_graphics import *
import csv
import os

def loadImagesPaths(app):
    imagesNamePathDict = dict()
    for (root,dirs,files) in os.walk(app.assetsFolderPath):
        for file in files:
            name_Ext = file.split(".")
            if name_Ext[1] == "png":
                path = root + "/" + file
                imagesNamePathDict[name_Ext[0]] = app.loadImage(path)
    return imagesNamePathDict

def loadAssets(app):
    app.img = loadImagesPaths(app)

