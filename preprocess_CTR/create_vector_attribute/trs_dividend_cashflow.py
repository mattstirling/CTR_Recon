'''
Created on Jan 17, 2017

@author: mstirling
'''
import pandas as pd, os, time
import re

#timing
t1 = time.time()

#control variables
create_file_vector = 0
create_file_vector_attribute = 1

#in folder
in_folder = 'C:\Users\mstirling\Desktop\Shared\RW\CTR Files/2017-01-31-PRD\in_K2/'.replace('\\','/')
in_file = 'K2_CM_TRS_D_20170131_01_PRD.csv'
in_vector_name = 'C,TRS v1.87:Dividend Cashflow'

#out folder and files
out_folder = in_folder + 'vectors/'
out_file_vector =  in_file.replace('.csv','') + '_' + re.sub(r'[, .:]',r'_',in_vector_name) + '.csv' 
out_file_vector_attribute = in_file.replace('.csv','') + '_' + re.sub(r'[, .:]',r'_',in_vector_name) + '_attribute.csv'

#make sure we have the output folder
try: os.stat(out_folder[:-1])
except: os.mkdir(out_folder[:-1])

#create a file with only the header records in scope
if create_file_vector:
    #get header length, header filename, and open the file for output
    #C,TRS v1.87:Dividend Cashflow
    in_vector_name_len = len(in_vector_name)
    f_out = open(out_folder + out_file_vector,'w')     
    for line in open(in_folder + in_file,'r'):
        if line[:in_vector_name_len]==in_vector_name:
            f_out.write(line)
    f_out.close()

if create_file_vector_attribute:
    
    f_out = open(out_folder + out_file_vector_attribute,'w')
    f_out.write('Name,Dividend Cashflow' + '\n')
    
    #open vector file
    df = pd.read_csv(out_folder+out_file_vector, header = None, usecols = [3,4,5,6,7], dtype={6: str})
    df.columns = ['id','vector_name','date','amt','currency']
    
    #get all ids in this file
    id_list = df.id.unique()
    
    #for each id, order records by date desc and then merge into 1 str
    for this_id in id_list:
        this_id_df = df.loc[df.id.isin([this_id])]
        this_id_df.sort(['date'],ascending = True, inplace=True)
        this_id_df['out_str'] = this_id_df['date'].str.replace('-','/') + ' ' + this_id_df['amt'].str.replace('-','') + ' ' + this_id_df['currency']  
        rw_val = ', '.join(this_id_df.out_str.tolist())
        if ',' in rw_val: rw_val = '"(' + rw_val + ')"'
        f_out.write(this_id + ',' + rw_val + '\n')
        df = df[-df.id.isin([this_id])]
    f_out.close()

print 'done'

t2 = time.time()
print 'total run = ' + str(t2-t1) + ' sec'
