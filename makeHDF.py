#!/usr/bin/env python
# coding: utf-8


import h5py as h5
import glob,os,ast
import pandas as pd
from tqdm import tqdm
import numpy as np

dloc = 'census-atlas/data/lsoa'
files = glob.glob(dloc + '/*.csv')
files.sort()
df = pd.read_csv(files[0])
codes = df.GEOGRAPHY_CODE
shape = list(df.shape)
shape.append(len(files))
shape


f = h5.File('test.h5', 'a')


try:del f['indicators']
except:None
indicators = f.create_dataset("indicators", (shape[0],shape[2],shape[1]), dtype='i8')


j=0
dummy = np.empty(shape=(shape[0],shape[2],shape[1]))
for i in tqdm(files):
    df = pd.read_csv(i).set_index('GEOGRAPHY_CODE').loc[codes]
    df['perc'] = (df[df.columns[-1]]/df['0'])*10000 # 100% and 2dp so /100
    dummy[:,j,:] = df.values
    j += 1

indicators[:,:,:] = dummy.astype('i8')


GEOCD = dict( zip(codes,range(len(codes)) ))
f.attrs['GEOCD'] = str(GEOCD)
fname = dict( [[os.path.basename(i).split('.')[0],j] for j,i in enumerate(files) ])
f.attrs['INDICATORS'] = str(fname)
f.attrs['VALUE'] = str(dict(value=0,count=1,percent=2))
f.attrs['order'] = 'indicators,geocd,values'


# # turn back into a dict
# ast.literal_eval(f.attrs['VALUE'])


f.close()
