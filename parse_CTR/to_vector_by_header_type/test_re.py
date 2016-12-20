'''
Created on Dec 2, 2016

@author: mstirling
'''
import re

#in folder
in_folder = 'C:/Users/mstirling/Desktop/'
in_file = 'K2_CM_Swap_D_20161201_01.csv'

#in_folder = 'C:/Users/mstirling/Desktop/Shared/RW/CTR Files/2016-10-24-PRD/'
#in_file = 'K2_CM_Swap_D_20161024_01.csv'


#pull data from file
for line in open(in_folder + in_file,'r'):
    match = re.search(r'.*SR3979.*',line)
    if match: print line.rstrip()