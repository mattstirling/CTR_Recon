'''
Created on Jan 13, 2016

@author: mstirling

'''
import time, os, ConfigParser, glob, re

#open config file
config = ConfigParser.ConfigParser()
config.read('config.ini')

#in folder
parent_folder = config.get('filename','parent_folder')

in_folder = 'riskwatch_ctrfile_by_vector/'
out_folder = 'riskwatch_by_header_by_vector/'

#make sure we have the folder
try:
    os.stat(parent_folder + out_folder[:-1])
except:
    os.mkdir(parent_folder + out_folder[:-1])

#get files to process
in_path_list = glob.glob(parent_folder + in_folder + '*.csv')
in_file_list = [i[len(parent_folder + in_folder):] for i in in_path_list]

#initialize empty lists
out_file_list = []
out_filename_list = []

for this_file in in_file_list:
    
    #open file
    f_in = open(parent_folder + in_folder + this_file,'r')
    
    #read the header
    this_header = f_in.readline().split(',')
    try:
        this_line = f_in.readline()
    except:
        continue
    
    if not this_line == '': 
    
        #get the filename
        split_line = this_line.strip().split(',')
        this_header_type =  split_line[this_header.index('rw_header_type')]
        this_vector =  split_line[this_header.index('rw_column')]
        out_filename = 'out_vectors_' + this_header_type.replace(' ', '_') + this_vector.replace(' ', '_') + '.csv'
        
        #look for the filename in the index
        if out_filename in out_filename_list:
            out_file_index =  out_filename_list.index(out_filename)
            out_file = out_file_list[out_file_index]
        
        else:
            #otherwise open a new file
            out_file = open(parent_folder + out_folder + out_filename,'w')
            out_file.write(','.join(this_header))
            
            #add to list
            out_filename_list.append(out_filename)
            out_file_list.append(out_file)
            
        #write this line to our file
        out_file.write(this_line)
        
        #read the rest of the file
        try:
            out_file.write(f_in.read())
        except:
            continue

print 'done'
    

