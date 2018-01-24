# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import googlemaps
from progress.bar import IncrementalBar

class FancyBar(IncrementalBar):
    message = 'Loading'
    fill = '*'
    suffix = '%(percent).1f%% - %(elapsed_td)s / %(eta_td)s'

gmaps = googlemaps.Client(key=your_key)

origins = pd.read_csv("origins.csv")
destinations = pd.read_csv("destinations.csv")

outputtxt = open("output.txt", "w", encoding="utf-8")

# Matrix is divided into 10x10 subblocks such that there are 100 requests per second.
originBlocks = list()
i = 0
for i in range(0,len(origins),10):
    originBlocks.append(list(np.arange(i,min(len(origins),i+10))))

destinationsBlocks = list()
j = 0
for j in range(0,len(destinations),10):
    destinationsBlocks.append(list(np.arange(j,min(len(destinations),j+10))))

distances = np.zeros((len(origins.index),len(destinations.index)))
durations = np.zeros((len(origins.index),len(destinations.index)))
bar = FancyBar()

for oIndices in originBlocks:
    for dIndices in destinationsBlocks:
        oBlock = [",".join(elem) for elem in origins.iloc[oIndices].as_matrix()]
        dBlock = [",".join(elem) for elem in destinations.iloc[dIndices].as_matrix()]

        response = gmaps.distance_matrix(oBlock, dBlock)
        for o,row in zip(oIndices,response["rows"]):
            for d,element in zip(dIndices,row["elements"]):

                # Sometimes status is not OK, then enter NaN.
                if element["status"] == "OK":
                    distances[o][d] = element["distance"]["value"]
                    durations[o][d] = element["duration"]["value"]
                else:
                    distances[o][d] = float('nan')
                    durations[o][d] = float('nan')

                # Also create a csv file where distances and durations are given line by line.
                outputtxt.write('%dx%d: %s-%s-%s-%s\n' % (o,d,origins.iloc[o]["City"]+","+origins.iloc[o]["District"],destinations.iloc[d]["City"]+","+destinations.iloc[d]["District"],distances[o][d],durations[o][d]))
                bar.next()
bar.finish()
outputtxt.close()

# Save matrices as dataframes
distances = pd.DataFrame(distances, columns = np.arange(len(destinations.index)))
durations = pd.DataFrame(durations, columns = np.arange(len(destinations.index)))

distances.to_csv("distances.csv")
durations.to_csv("durations.csv")
