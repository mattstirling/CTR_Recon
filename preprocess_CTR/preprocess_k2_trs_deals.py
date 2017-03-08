'''
Created on Feb 7, 2017

@author: mstirling
'''

import shutil
import os

in_folder = 'C:\Users\mstirling\Desktop\Shared\RW\CTR Files\RW_ECR_Release_13/ctr_ouput/out_K2_TRS/mtm_compare_w_ctr_underlying/'.replace('\\', '/')
in_file_list = ['K2_Bond_Total_Return_Swap_D_20170131_16_RiskWatch_v10.csv'
                ,'K2_Credit_Total_Return_Swap_D_20170131_16_RiskWatch_v10.csv']

out_folder = in_folder
out_file = 'k2_trs_deals.csv'

try: os.stat(out_folder[:-1])
except: os.mkdir(out_folder[:-1])

#concatenate
with open(out_folder + out_file,'wb') as wfd:
    for f in in_file_list:
        print in_folder + f
        with open(in_folder + f,'rb') as fd:
            shutil.copyfileobj(fd, wfd, 1024*1024*10)

print 'done.'
print 'to ' + out_folder + out_file




