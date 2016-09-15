'''
Created on Sep 15, 2016

@author: mstirling
'''
'''
Created on Sep 15, 2016

@author: mstirling
'''

#import libraries
import os, time, re

#timing
t1 = time.time()

#in folder + out folder
main_folder = 'C:/Users/mstirling/Desktop/Shared/RW/CTR Files/20160912_Inbound/'
in_folder = main_folder + 'K2/'
out_folder = main_folder + 'K2_out/'  
in_file = 'K2_CM_Swap_D_20160912_02' + '.csv'
in_file_header_list = 'out_' 'K2_CM_Swap_D_20160912_02' + '_HeaderList' + '.txt'

#make sure we have the output folder
try:
    os.stat(out_folder[:-1])
except:
    os.mkdir(out_folder[:-1])

#get the header list from file
header_list = []
f_in_header_list = open(out_folder + in_file_header_list,'r')
for line in f_in_header_list:
    header_list.append(line.strip())

for header in header_list:
    
    #output the header because the process takes so long
    print header
    
    #get header length, header filename, and open the file for output
    header_len = len(header)
    header_for_filename = re.sub(r'[, .:]',r'_',header)    
    out_file = 'out_' 'K2_CM_Swap_D_20160912_02' + '_' + header_for_filename + '.csv'
    f_out = open(out_folder + out_file,'w')     
    
    for line in open(in_folder + in_file,'r'):
        if line[:header_len]==header:
            f_out.write(line)
    
    f_out.close()

#done message
print 'done files from ' + str(in_folder) 
print 'wrote to ' + str(out_folder) 

t2 = time.time()
print 'total run = ' + str(t2-t1) + ' sec'