'''
Created on July 28, 2016

@author: cnamgoong
'''
import pandas as pd, os, numpy as np

#in files
in_CTR_folder = 'C:/Users/mstirling/Desktop/Shared/RW/CTR Files/21-JUL-16/'
in_CTR_file = 'out_OBJECTCHARLIE/' + 'out_OBJCHARLIE_FXFORWARD_CTR_preprocessed_file.csv'
in_VAR_folder = in_CTR_folder
in_VAR_file = 'out_OBJECTCHARLIE/' + 'out_OBJCHARLIE_FXFORWARD_VAR_preprocessed_file.csv'
out_file = 'out_OBJECTCHARLIE/' + 'out_compare_diff_OBJECTCHARLIE_FXFORWARD.csv'

#load data
df_CTR = pd.read_csv(in_CTR_folder+in_CTR_file)
df_VAR = pd.read_csv(in_VAR_folder+in_VAR_file)
print len(df_CTR.columns)
print len(df_VAR.columns)

#set index to Name
df_CTR.set_index('Name',inplace=True)
df_VAR.set_index('Name',inplace=True)

#sort by index
df_CTR.sort_index(axis=0,inplace=True)
df_VAR.sort_index(axis=0,inplace=True)

#drop any columns that are not in common
common_cols = [col for col in df_CTR.columns if col in df_VAR.columns]
df_CTR.drop(labels=[col for col in df_CTR.columns if col not in common_cols],axis=1,inplace=True)
df_VAR.drop(labels=[col for col in df_VAR.columns if col not in common_cols],axis=1,inplace=True)
print len(df_CTR.columns)
print len(df_VAR.columns)

#reorder columns
df_CTR.sort_index(axis=1,inplace=True)
df_VAR.sort_index(axis=1,inplace=True)

#take difference
difference_locations = np.where((df_CTR != df_VAR) & ~(df_CTR.isnull() & df_VAR.isnull()))
changed_CTR = df_CTR.values[difference_locations]
changed_VAR = df_VAR.values[difference_locations]
changed_index = [df_CTR.index[i] for i in difference_locations[0]] 
changed_col = [df_CTR.columns[i] for i in difference_locations[1]]
df_diff = pd.DataFrame({'name':changed_index,'column':changed_col,'val_CTR': changed_CTR, 'val_VAR': changed_VAR})

print 'num records match: ' + str(len(df_CTR.index))
print 'num columns match: ' + str(len(df_CTR.columns))
print 'num non-null cells to compare: ' + str(len(np.where((df_CTR.isnull() & df_VAR.isnull()))[0])) 
print 'num cells diff: ' + str(len(df_diff.index)) 

df_diff.to_csv(in_CTR_folder + out_file)

print len(df_diff)

df_group = df_diff.groupby(['column']).size()

#print only a subset of the file
#df_diff[df_diff.column=='Asset Notional'].to_csv(in_VAR_folder + out_VAR_file)

print 'done.'
print 'done. write from ' + in_CTR_folder + in_CTR_file
print 'done. write from ' + in_VAR_folder + in_VAR_file
print 'done. write to ' + in_CTR_folder