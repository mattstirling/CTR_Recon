'''
Created on Dec 7, 2016

@author: mstirling
'''

import re, mmap,os

#in folder
in_folder = 'C:/Users/mstirling/Desktop/'
in_file = 'K2_CM_Swap_D_20161216_01.csv'

out_folder = 'C:/Temp/python/out/'
out_file = 'out_trade_regex.txt'
f_out = open(out_folder + out_file,'w')
    
try: os.stat(out_folder[:-1])
except: os.mkdir(out_folder[:-1])

with open(in_folder + in_file,'r+') as f:
    data = mmap.mmap(f.fileno(), 0)
    for i in re.findall(r'^[PC].*Msg 208*\n', data):
        print i.strip()
        f_out.write(i)
    