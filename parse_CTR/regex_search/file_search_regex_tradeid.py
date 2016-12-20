'''
Created on Dec 7, 2016

@author: mstirling
'''

import re, mmap,os

this_trade_id_list = (['TB1612'
                      ,'TB1628'])

#in folder
in_folder = 'C:/Users/mstirling/Desktop/'
in_file = 'K2_CM_TRS_D_20161215_02.csv'

out_folder = 'C:/Temp/python/out/K2_deals_with_dupe_vectors/'
try: os.stat(out_folder[:-1])
except: os.mkdir(out_folder[:-1])

with open(in_folder + in_file,'r+') as f:
    data = mmap.mmap(f.fileno(), 0)
    for this_trade_id in this_trade_id_list:
        out_file = 'out_trade_ ' + this_trade_id + '_K2_CM_Swap_D_20161215_02' +  '.txt'
        f_out = open(out_folder + out_file,'w')
        for i in re.findall(r'[PC],.*' + this_trade_id + '.*\n', data):
            print i.strip()
            f_out.write(i)
        f_out.close()