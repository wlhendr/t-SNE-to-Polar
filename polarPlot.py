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
