import pandas as pd
import numpy as np
import random
from random import randint
from matplotlib import colors
import time

start_time = time.time()
otuTable = pd.read_csv("otuTable.csv")
data = pd.read_csv("data.csv")

#hard code colors for each phylum
phylums =   ['Actinobacteria',
            'Bacteroidetes',
            'Firmicutes',
            'Other',
            'Proteobacteria',
            'Verrucomicrobia']

genusExceptions =   ['Enterococcus',
                    'Blautia',
                    'Lactobacillus',
                    'Staphylococcus']

rgb = pd.Series([(.886, .259, .957),
                (.176, .749, .761),
                (.965, .62, .627),
                (.071, .573, .275),
                (.561, .459, .212),
                (.231, .318, .639),
                (1.0, 1.0, .816),
                (.957, .259, .259),
                (.945, .922, .145),
                (1.0, .8, .8)],
                index =
                ['Actinobacteria',
                'Bacteroidetes',
                'Blautia',
                'Enterococcus',
                'Firmicutes',
                'Lactobacillus',
                'Other',
                'Proteobacteria',
                'Staphylococcus',
                'Verrucomicrobia'])

rgbDF = pd.DataFrame(rgb)
#find most diminant in each row
dataAbundances = data.filter(regex = 'abundance')
dominantAbundance = dataAbundances.idxmax(axis=1)

#Create match color to easily find correct type
otuTable['abundanceMatch'] = np.nan
for i in range(0, otuTable.shape[0]):
    #run through every rows
    otuTable.loc[i,'abundanceMatch'] = i + 1

otuTable['abundanceMatch'] = 'abundances' + otuTable['abundanceMatch'].astype(str)
otuTable['abundanceMatch'] = otuTable['abundanceMatch'].map(lambda x: x.rstrip('0').rstrip('.'))


#match correct colors
data['HEXcolor'] = np.nan
data['graphingLabel'] = np.nan
for i in range(0, data.shape[0]):
    #find abundance to search for
    targetAbundance = dominantAbundance[i:i+1].item()
    if i % 100 == 0:
        print "Assigned colors for %d samples:" % i
    #match abundance to phylum and genus
    basePhylum = otuTable[otuTable.abundanceMatch == targetAbundance].Phylum.item()
    baseGenus = otuTable[otuTable.abundanceMatch == targetAbundance].Genus.item()

    if (not basePhylum in phylums) and (not baseGenus in phylums):
        #handle exceptions
        #print "Type represented as 'other'"
        basePhylum = 'Other'
        baseGenus = 'Other'
    if basePhylum in phylums:
        #color by phylum
        randomNum = (randint(500,1000)/1000.0)
        tempColor = rgb[basePhylum]
        tempColor = [j * randomNum for j in tempColor]
        hexColor = colors.to_hex(tempColor)
        data.loc[i,'HEXcolor']= hexColor
        data.loc[i,'graphingLabel']= basePhylum
        #print "Color assigned by Phylum:    %d" % i

    if baseGenus in genusExceptions:
        #color by genus
        randomNum = (randint(500,1000)/1000.0)
        tempColor = rgb[baseGenus]
        tempColor = [j * randomNum for j in tempColor]
        hexColor = colors.to_hex(tempColor)
        data.loc[i,'HEXcolor']= hexColor
        data.loc[i,'graphingLabel']= baseGenus
        #print "Color assigned by Genus:     %d" % i


#move column to front of table
cols = data.columns.tolist()
cols.insert(5,cols.pop(cols.index('HEXcolor')))
data = data.reindex(columns = cols)

cols = data.columns.tolist()
cols.insert(5,cols.pop(cols.index('graphingLabel')))
data = data.reindex(columns = cols)

print("All colors assigned in %.2f seconds." % (time.time() - start_time))
print("Saving updated.csv file...")
data.to_csv("dataUpdated.csv", index = False)

#
