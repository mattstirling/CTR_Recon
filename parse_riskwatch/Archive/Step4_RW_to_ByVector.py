'''
Created on Jan 13, 2016

@author: mstirling

'''
import time, os, ConfigParser

#open config file
config = ConfigParser.ConfigParser()
config.read('config.ini')

#in folder
in_folder = config.get('filename','parent_folder')

in_folder_byproduct = 'all/ByProduct/'
out_folder_byvector = 'all/ByVector/'

#files in scope
files_in_scope = (['out_deals_BNS_Currency_Swap.csv'])

#fields in scope
columns_in_scope = (['Pay Principal Payment','Rec Principal Payment'])

#out header cols
out_header_cols = 'id,rw_column,date,amt,curr'

for this_file in files_in_scope:
    
    f_in = open(in_folder + in_folder_byproduct + this_file,'r')
    f_header = f_in.readline().strip().split(',')
    this_index_id = f_header.index('ID')
    
    #get a list of fields in the header that are vectors
    vector_cols = []
    for i in range(len(f_header)):
        if f_header[i] in columns_in_scope:
            vector_cols.append([f_header[i],i])
    
    #open the file to write out to
    out_file = this_file.replace('out_deals_','out_vectors_')
    f_out = open(in_folder + out_folder_byvector + out_file,'w')
    f_out.write(out_header_cols)
    
    for line in f_in:
        this_line = line.strip().split(',')
        
        
        for [v_name, v_index] in vector_cols:
            
            this_id = this_line[this_index_id]
            this_vector_value = this_line[v_index]
        
            if len(this_vector_value)>0:
                this_vector_value_list = this_vector_value.strip('(').strip(')').split('|')    
                
                for j in this_vector_value_list:
                    [this_date, this_amt, this_curr] = j.split(' ')                
                    record_to_insert = ([str(this_id)
                                        ,str(v_name)
                                        ,str(this_date)
                                        ,str(this_amt)
                                        ,str(this_curr)])
                    f_out.write('\n' + ','.join(record_to_insert))
        
    #close the file    
    f_out.close()
   
        
    
print 'done'
    

