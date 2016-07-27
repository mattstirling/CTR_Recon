'''
Created on Jul 27, 2016

@author: mstirling
'''
import pandas as pd

#in files
in_CTR_folder = 'C:/Users/mstirling/Desktop/Shared/RW/CTR Files/21-JUL-16/'
in_CTR_file = 'out_EPSILON/' + 'out_TRS.csv'
in_VAR_folder = 'C:/Users/mstirling/Desktop/Shared/RW/VAR Session/market.16.07.21/'
in_VAR_file = 'recon/' + 'EPSILON_TRS.csv'
out_file = 'out_EPSILON/' + 'out_diff_by_column_EPSILON_TRS.csv'

#load data
df_CTR = pd.read_csv(in_CTR_folder+in_CTR_file, nrows = 10)
df_VAR = pd.read_csv(in_VAR_folder+in_VAR_file, nrows = 10)
print len(df_CTR.columns)
print len(df_VAR.columns)

df_CTR_col = pd.DataFrame({'in_CTR':['Y' for col in df_CTR.columns]},index=df_CTR.columns) 
df_VAR_col = pd.DataFrame({'in_VAR':['Y' for col in df_VAR.columns]},index=df_VAR.columns)
df_merge_col = pd.concat([df_CTR_col,df_VAR_col],axis=1)

df_merge_col.sort_index(axis=1,inplace=True)

df_merge_col.to_csv(in_CTR_folder + out_file)

print 'done.'
print 'done. write from ' + in_CTR_folder + in_CTR_file
print 'done. write from ' + in_VAR_folder + in_VAR_file
print 'done. write to ' + in_CTR_folder