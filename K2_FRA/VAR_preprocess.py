'''
Created on Aug 10, 2016

@author: cnamgoong
'''
import pandas as pd, ConfigParser
from Map_Rules import apply_map_rule

#control variables
bWriteReport = 1

#open config file
config = ConfigParser.ConfigParser()
config.read('config.ini')

#in VAR files
in_folder = config.get('filename','in_folder_VAR')
in_file_Fra = config.get('filename','in_file_VAR')

#in mapping rule files
map_folder = config.get('filename','in_folder_map')
map_file = config.get('filename','in_file_map')

#out folder
out_folder = config.get('filename','out_folder')
out_file = config.get('filename','out_file_VAR')

#open in_files
df_Fra = pd.read_csv(in_folder+in_file_Fra)
#print len(df_TRS.index)

#filter 
file_list_in_scope = ['/__bns__derivProdData__riskWatch__EQUITYFIO__ALL__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__EQUITYFSO__ALL__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__EQUITYILN__ALL__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__EQUITYSPI__ALL__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__EQUITYSPS__ALL__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__EQUITYSP__ALL__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__EQUITYSSO__ALL__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__LDNCCS__EUR__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__LDNCCS__GBP__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__LDNCCS__USD__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__LDNEURSWAP__EUR__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__LDNGBPSWAP__GBP__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__LDNINFLATION__GBP__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__NYDERIV__USD__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__NYIRSWAP__USD__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__NYOISHEDGE__USD__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__RETAIL__ALL__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__SWAPS_BOOK__USD__Sybase_K2.csv']
df_merge = df_Fra[(df_Fra.Filename.isin(file_list_in_scope))]
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
df_merge.to_csv(out_folder + out_file,index=False)

print 'done.'
print 'from ' + in_folder
print 'to ' + out_folder