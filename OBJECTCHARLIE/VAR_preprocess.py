'''
Created on July 27, 2016

@author: cnamgoong
'''
import pandas as pd, ConfigParser
from Map_Rules import apply_map_rule  # @UnresolvedImport

#open config file
config = ConfigParser.ConfigParser()
config.read('config.ini')

#in VAR files
in_folder = config.get('filename','in_folder_VAR')
in_file_FOREX = config.get('filename','in_file_VAR')

#in CTR files
map_folder = config.get('filename','in_folder_map')
map_file = config.get('filename','in_file_map')

#out folder
out_folder = config.get('filename','out_folder')
out_file = config.get('filename','out_file_VAR')

#open in_files
df_FOREX = pd.read_csv(in_folder+in_file_FOREX)
#print len(df_TRS.index)

#filter 
df_merge = df_FOREX
#df_merge = df_FOREX[(df_FOREX.Filename.str.contains("/__bns__var_rw__data__riskwatch__charlie__"))&(df_FOREX.Name.str.contains("CHARLIE"))&(~df_FOREX.Name.str.contains("FX"))]
#print len(df_TRS.index)

print 'VAR num records: ' + str(len(df_merge.index))
print 'VAR num columns: ' + str(len(df_merge.columns))

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
df_merge.to_csv(out_folder + out_file,index=False)

print 'done.'
print 'from ' + in_folder
print 'to ' + out_folder