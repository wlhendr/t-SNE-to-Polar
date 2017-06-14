from matplotlib import pyplot as plt
from scipy.spatial import distance
import pandas as pd
import numpy as np
from numpy.random import rand
from tsne import bh_sne
import math
from skbio.stats.distance import mantel
import time

def cartesianToPolar(Tuple):
    #Tuple[0] = X
    #Tuple[1] = Y
    dist = np.sqrt(Tuple[0]**2 + Tuple[1]**2)
    theta = np.arctan2(Tuple[1], Tuple[0])
    return(dist, theta)

def polarToCartesian(Tuple):
    #Tuple[0] = dist
    #Tuple[1] = theta
    x = Tuple[0] * np.cos(Tuple[1])
    y = Tuple[0] * np.sin(Tuple[1])
    return(x, y)

#read in full set of data
data = pd.read_csv("data.csv")


#y_color is for colorcoding the individual points based on genus/phylum
colors = data.HEXcolor

#filter out metaData
x_data = data.filter(regex= 'abundanc')
x_data = np.asarray(x_data).astype('float64')
x_data = x_data.reshape((x_data.shape[0], -1))

#run tsne on data
vis_data = bh_sne(x_data, perplexity = 30)

#seperate into the x and y values to plot 2D
vis_x = vis_data[:, 0]
vis_y = vis_data[:, 1]

#compute distance matrix to use as "correct"
tsneDataXY = zip(vis_x, vis_y)      #redundant
tsneDistanceMatrix = distance.cdist(tsneDataXY, tsneDataXY, 'euclidean')

tsdm = pdist(tsneDataXY)
