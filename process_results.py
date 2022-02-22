#!/usr/bin/env python3

import os
from glob import glob
import pandas as pd

def digitSplit(string):
    # iterate until encounter a digit
    for idx,character in enumerate(string):
        if character.isdigit():
            return (string[:idx],string[idx:])

def processFilename(filename):
    attribs = dict(
        digitSplit(chunk) for
        chunk in filename.split('_')[1:]
    )
    # compute the mean and stddev of 
    data = pd.read_csv(filename,sep = '\s+',header = None)
    # discard the warm up and cool down periods equal to number of
    # vehicles times the number of seats
    offset = int(attribs['nv'])*int(attribs['cp'])
    data = data.iloc[offset:-offset]
    pickup = data[3] - data[2]
    travel = data[4] - data[3] - data[1]
    attribs['meanPickupDelay'] = pickup.mean()
    attribs['meanTravelDelay'] = travel.mean()
    attribs['stdPickupDelay'] = pickup.sem()
    attribs['stdTravelDelay'] = travel.sem()
    return attribs

pd.DataFrame(
    processFilename(filename)
    for filename in glob('rides_*')
).sort_values('rr').to_csv('results.csv',index = False)
