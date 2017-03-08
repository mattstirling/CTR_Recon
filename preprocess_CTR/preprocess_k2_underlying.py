'''
Created on Feb 7, 2017

@author: mstirling
'''

import preprocess_ETL #@UnresolvedImport
import pandas as pd, numpy as np
import glob2
import shutil
import os

in_folder = 'C:\Users\mstirling\Desktop\Shared\RW\CTR Files\RW_ECR_Release_13/ctr_ouput/'.replace('\\', '/')
out_folder = in_folder + 'mtm_compare_k2_underlying/'
out_file = 'k2_underlying.csv'

try: os.stat(out_folder[:-1])
except: os.mkdir(out_folder[:-1])

#concatenate
with open(out_folder + out_file,'wb') as wfd:
    for f in glob2.glob(in_folder + 'K2_CSM_*.csv'):
        print f
        with open(f,'rb') as fd:
            shutil.copyfileobj(fd, wfd, 1024*1024*10)

print 'done.'
print 'to ' + out_folder + out_file




