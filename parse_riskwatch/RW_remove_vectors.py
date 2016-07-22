'''
Created on Jan 13, 2016

@author: mstirling
'''
import time

#file variables
in_folder = 'C:/Temp/python/in/'
in_file = 'deals.csv'
out_folder = 'C:/Temp/python/out/'
out_file = 'out_' + time.strftime("%Y%m%d") + '_' + in_file 

f_out = open(out_folder + out_file,'w')
with open(in_folder + in_file, 'r') as f_in:
    line_count = 0
    for line in f_in:
        line_count+=1
        b_include_line = 1
        if line[:5] ==',,,,,': b_include_line = 0
        if line[:5] ==',:pos': b_include_line = 0
        if line[:8] ==',Default': b_include_line = 0
        if line[:1] =='#': b_include_line = 0
        if b_include_line: 
            f_out.write(line)
                
f_out.close()

print 'done.'  