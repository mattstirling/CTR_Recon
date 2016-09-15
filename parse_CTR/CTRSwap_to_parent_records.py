'''
Created on Sep 15, 2016

@author: mstirling
'''

#import libraries
import os, time

#timing
t1 = time.time()

#in folder + out folder
main_folder = 'C:/Users/mstirling/Desktop/Shared/RW/CTR Files/20160912_Inbound/'
in_folder = main_folder + 'K2/'
out_folder = main_folder + 'K2_out/'  
in_file = 'K2_CM_Swap_D_20160912_02' + '.csv'
out_file = 'out_' 'K2_CM_Swap_D_20160912_02' + '_ParentRecordsOnly' + '.csv'

#make sure we have the folder
try:
    os.stat(out_folder[:-1])
except:
    os.mkdir(out_folder[:-1])

#output files
f_out = open(out_folder + out_file,'w')

#open input file
f_in = open(in_folder + in_file,'r')

for line in f_in:
    if line[:6]=='P,Swap':
        f_out.write(line.strip() + '\n')

f_in.close()
f_out

#done message
print 'done files from ' + str(in_folder) 
print 'wrote to ' + str(out_folder) + str(out_file)

t2 = time.time()
print 'total run = ' + str(t2-t1) + ' sec'