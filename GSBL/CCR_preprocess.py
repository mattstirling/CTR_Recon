'''
Created on Feb 23, 2016

@author: mstirling
'''
import pandas as pd
from Map_Rules import apply_map_rule

#control variables
bWriteReport = 1

#in VAR files
in_folder = 'C:/Users/mstirling/Desktop/Shared/RW/CCR Session/2016/07/'
in_file_gpf_col = 'gpf_collateral.csv.20160721'
in_file_gpf_e = 'gpf_exposure.csv.20160721'
in_file_gsf_col = 'gsf_collateral.csv.20160721'
in_file_gsf_e = 'gsf_exposure.csv.20160721' 

#in mapping rule files
map_folder = ''
map_file = 'map_GSBL.csv'

#out folder
out_folder = 'C:/Users/mstirling/Desktop/Shared/RW/CTR Files/21-JUL-16/' + 'out_GSBL/'
out_file = 'out_GSBL_exp_preprocessed_file.csv'

#open in_files
df_gpf_e = pd.read_csv(in_folder+in_file_gpf_e)
df_gpf_col = pd.read_csv(in_folder+in_file_gpf_e)
df_gsf_e = pd.read_csv(in_folder+in_file_gpf_e)
df_gsf_col = pd.read_csv(in_folder+in_file_gpf_e)

#print len(df_TRS.index)

df_merge = df_gpf_e
print len(df_merge.index)

#reorder columns
df_merge.sort_index(axis=1,inplace=True)

print 'CTR num records: ' + str(len(df_merge.index))
print 'CTR num columns: ' + str(len(df_merge.columns))

#open mapping rules
df_map = pd.read_csv(map_folder+map_file)

#apply transformation for alias
#copy alias values to real column and drop alias column
for i in df_map[~df_map['RW Alias'].isnull()].index:
    #assume only 1 alias per column for now
    this_col = str(df_map.at[i,'Column Name'])
    this_alias = str(df_map.at[i,'RW Alias'])
    
    #copy alias values to 'this_col'
    for j in df_merge[~df_merge[this_alias].isnull()].index:
        df_merge.at[j,this_col] = df_merge.at[j,this_alias] 
    
    #drop alias column
    df_merge.drop([this_alias],axis=1,inplace=True)

#now apply 'within-cell' mapping rules
for i in df_map['Column Name'].index:
    this_col = str(df_map.at[i,'Column Name'])
    this_map_rule = str(df_map.at[i,'RW Map Rule'])
    
    #apply the mapping rule if rule 'not nan/blank'
    if not this_map_rule == 'nan':
        for j in df_merge.index:
            df_merge.at[j, this_col] = apply_map_rule(df_merge.at[j, this_col], this_map_rule) 

#sort by Name
#df_merge.sort('Name', inplace = True)

#write out_files
df_merge.to_csv(out_folder + out_file,index=False)

print 'done.'
print 'from ' + in_folder
print 'to ' + out_folder