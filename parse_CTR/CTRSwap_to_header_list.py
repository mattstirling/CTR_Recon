'''
Created on Sep 15, 2016

@author: mstirling
'''

#import libraries
import os, time, re

#timing
t1 = time.time()

#in folder + out folder
#in folder
in_folder = 'C:/Users/mstirling/Desktop/Shared/RW/CTR Files/RW_ECR_Release_10/CTR_input_files_used/K2/'
#in_folder = 'C:/Users/mstirling/Desktop/CTR_out_RW_ECR9/in files/'
out_folder = in_folder + 'by_vector/'  
in_file = 'K2_CM_Swap_D_20170110_01.csv'
out_file = 'out_header_list.txt'

#make sure we have the folder
try:
    os.stat(out_folder[:-1])
except:
    os.mkdir(out_folder[:-1])

#output files
f_out = open(out_folder + out_file,'w')

#open input file
f_in = open(in_folder + in_file,'r')

#
header_set = set()

for line in f_in:
    this_match = re.search(r'^(.*?Swap.*?),',line)
    if this_match: header_set.add(this_match.group(1))

#write all of the headers to file
with open(out_folder + out_file,'w') as f_out:
    for header in sorted(header_set):
        f_out.write(header + '\n')

f_in.close()
f_out

#done message
print 'done files from ' + str(in_folder) 
print 'wrote to ' + str(out_folder) + str(out_file)

t2 = time.time()
print 'total run = ' + str(t2-t1) + ' sec'