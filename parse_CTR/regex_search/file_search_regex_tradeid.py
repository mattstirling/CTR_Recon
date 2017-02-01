'''
Created on Dec 7, 2016

@author: mstirling
'''

import re, mmap, os

this_trade_id_list = (['SO5601','I00010'])

#in folder
in_folder = 'C:/Users/mstirling/Desktop/Shared/RW/CTR Files/RW_ECR_Release_11/CTR_input_file/'
#in_folder = 'C:/Users/mstirling/Desktop/Shared/RW/K2 Files/Jan 27 Release - 20161230 Data/'
in_file = 'K2_CM_Swap_D_20170120_01.csv'

#out_folder = 'C:/Temp/python/out/K2_deals_with_dupe_vectors/'
out_folder = in_folder + 'trades/'
try: os.stat(out_folder[:-1])
except: os.mkdir(out_folder[:-1])

with open(in_folder + in_file,'r+') as f:
    data = mmap.mmap(f.fileno(), 0)
    for this_trade_id in this_trade_id_list:
        out_file = 'out_trade_ ' + this_trade_id + '.txt'
        f_out = open(out_folder + out_file,'w')
        for i in re.findall(r'[PC],.*' + this_trade_id + '.*\n', data):
            print i.strip()
            f_out.write(i)
        f_out.close()