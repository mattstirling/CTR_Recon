'''
Created on Oct 6, 2016
@author: ywang8
'''

import pandas as pd, os, re

import os

date = '2016-12-22'

#in_folder = 'C:/Users/ywang8/Documents/Side Project/For Matt/' + date + '/' + 'outfiles/riskwatch/'
in_folder = 'C:/Users/mstirling/Desktop/CTR_output_files/'
out_folder = 'C:/Users/mstirling/Desktop/err_out/'

out_file = 'Investigation_Result' + '_' + date + '.csv'


#filter out the files with bug
file_to_skip = []
for (dirpath, dirnames, filenames) in os.walk(in_folder):
    for filename in filenames:
        match = re.search(r'.*_Position_SBLOTC_D_.*',filename)
        if match:
            file_to_skip.append(filename)
            print(file_to_skip)

try:
    os.stat(out_folder[:-1])
except:
    os.mkdir(out_folder[:-1])

f_out = open(out_folder + out_file,'w')

f_out.write(','.join(['filename','col','row','error' + '\n']))

for (dirpath, dirnames, filenames) in os.walk(in_folder):
    row_input = []
    
    for filename in [f for f in filenames if f[-4:] =='.csv' and f not in file_to_skip]:
        
        file_path = in_folder + filename
        print(filename)
        df_in_file = pd.read_csv(file_path)   
        for col in df_in_file.columns:
            for row in df_in_file.index:
                if str(df_in_file.at[row,col])[:4] == 'Err_':
                    row_input = ','.join([filename, str(col), str(row), str(df_in_file.at[row,col]) + '\n'])
                    f_out.write(row_input)
           
f_out.close()
