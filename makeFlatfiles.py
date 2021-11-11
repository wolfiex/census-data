#!/usr/bin/env python
# coding: utf-8


import h5py as h5
from p_tqdm import p_imap,p_map
import numpy as np
import pandas as pd

import os,re,glob
__LOC__ = './data/'

def mkdir(loc):
    try:os.mkdir(loc)
    except FileExistsError: None

mkdir(__LOC__)
f = h5.File('test.h5', 'r')
cols = f.attrs['order'].split(',')

indi = eval(f.attrs['INDICATORS'])
geocd = eval(f.attrs['GEOCD'])

f['indicators'].shape,max(geocd.values()),max(indi.values())


## CSV and JSON

def gen_buff_itext(k):
    j,i=k
    warn = False

    newpath_c = f'{__LOC__}indicator_csv/'
    newpath_j = f'{__LOC__}indicator_json/'

    data = f['indicators'][:,i,:]
    if np.any(data<0):
        warn = j
        data = np.where(data<-1, 0, data)

    data = pd.DataFrame(data)
    data.columns = cols
    data.to_csv(f'{newpath_c}{j}.csv')
    data.to_json(f'{newpath_j}{j}.json')


    return warn


def gen_buff_ltext(k):
    j,i=k
    warn = False

    newpath_c = f'{__LOC__}location_csv/'
    newpath_j = f'{__LOC__}location_json/'

    data = f['indicators'][i,:,:]
    if np.any(data<0):
        warn = j
        data = np.where(data<-1, 0, data)

    data = pd.DataFrame(data)
    data.columns = cols
    data.to_csv(f'{newpath_c}{j}.csv')
    data.to_json(f'{newpath_j}{j}.json')


    return warn

# new indicator area
# for i,j in enumerate(indi):

def gen_buff_ifirst(k):
    j,i=k
    warn = False

    newpath = f'{__LOC__}indicator_first/'
    data = f['indicators'][:,i,:]
    if np.any(data<0):
        warn = j
        data = np.where(data<-1, 0, data)

    data = list(data.flatten()).__str__()

    #     print(f'node ./to_buffer {data} {newpath}{j}.buff ')
    os.system(f'node ./to_buffer "{data}" {newpath}{j}.buff')

    return warn


# Location first structure
def gen_buff_lfirst(k):
    j,i=k
    warn = False

    newpath = f'{__LOC__}location_first/'
    data = f['indicators'][i,:,:]
    if np.any(data<0):
        warn = j
        data = np.where(data<-1, 0, data)

    data = list(data.flatten()).__str__()

    os.system(f'node ./to_buffer "{data}" {newpath}{j}.buff')

    return warn


if __name__ == '__main__':
    mkdir(f'{__LOC__}/indicator_first/')
    mkdir(f'{__LOC__}/location_first/')
    mkdir(f'{__LOC__}/indicator_csv/')
    mkdir(f'{__LOC__}/indicator_json/')
    mkdir(f'{__LOC__}/location_csv/')
    mkdir(f'{__LOC__}/location_json/')

   ## intentionally not combigned functions as we will only use one

    # warnings = p_map(gen_buff_ifirst, list(indi.items()))

#    warnings2 = p_map(gen_buff_lfirst, list(geocd.items())) # very slow!

#    warnings3 = p_map(gen_buff_itext, list(indi.items()))

    warnings4 = p_map(gen_buff_ltext, list(geocd.items())) # very slow!


    with open('data/geocodes.txt','w') as cd: cd.write([x for _,x in sorted(zip(geocd.values(),geocd.keys()))].__str__())

    with open('data/indicatorcodes.txt','w') as cd: cd.write([x for _,x in sorted(zip(indi.values(),indi.keys()))].__str__())
