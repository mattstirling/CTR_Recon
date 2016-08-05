'''
Created on Feb 23, 2016

@author: mstirling
'''
import pandas as pd
from Map_Rules import apply_map_rule  # @UnresolvedImport

#control variables
bWriteReport = 1

#in VAR files
in_folder = 'C:/Users/mstirling/Desktop/Shared/RW/VAR Session/market.16.07.21/'
in_file_Repo = 'all/ByProduct/out_20160722_deals_BNS_Repo.csv' 

#in mapping rule files
map_folder = 'C:/Users/mstirling/Desktop/Shared/RW/CTR Files/21-JUL-16/'
map_file = 'map/map_ANVIL_Repo.csv'

#out folder
out_folder = map_folder
out_file_FX_Deals =  'out_ANVIL/' + 'out_ANVIL_Repo_VAR_preprocessed_file.csv'

#open in_files
df_Repo = pd.read_csv(in_folder+in_file_Repo)
#print len(df_TRS.index)

#filter 
file_list_in_scope = ['/sybase_anvil_london_20160721.csv'
                      ,'/sybase_anvil_ny_20160721.csv'
                      ,'/sybase_anvil_toronto_20160721.csv']
df_merge = df_Repo[(df_Repo.Filename.isin(file_list_in_scope))]
df_merge.reset_index(inplace=True,drop=True)
print len(df_merge.index)

#reorder columns
df_merge.sort_index(axis=1,inplace=True)

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
df_merge.sort('Name', inplace = True)

#write out_files
df_merge.to_csv(out_folder + out_file_FX_Deals,index=False)

print 'done.'
print 'from ' + in_folder
print 'to ' + out_folder