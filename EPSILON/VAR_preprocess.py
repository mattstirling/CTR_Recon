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
in_file_TRS = 'all/ByProduct/out_20160722_deals_BNS_Total_Return_Equity_Swap.csv' 

#in CTR files
map_folder = ''
map_file = 'map_EPSILON.csv'

#out folder
out_folder = 'C:/Users/mstirling/Desktop/Shared/RW/CTR Files/21-JUL-16/' + 'out_EPSILON/'
out_file_FX_Deals = 'out_EPSILON_VAR_preprocessed_file.csv'

#open in_files
df_TRS = pd.read_csv(in_folder+in_file_TRS)

#filter 
df_merge = df_TRS[(df_TRS.Filename == '/Sybase_Epsilon_processed.csv')&(df_TRS.Name.str.contains("EpsilonTRS"))]

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
        pd.options.mode.chained_assignment = None  # default='warn'
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
            pd.options.mode.chained_assignment = None  # default='warn'
            df_merge.at[j, this_col] = apply_map_rule(df_merge.at[j, this_col], this_map_rule) 

#sort by Name
df_merge.sort('Name', inplace = True)

#write out_files
df_merge.to_csv(out_folder + out_file_FX_Deals,index=False)

print 'done.'
print 'from ' + in_folder
print 'to ' + out_folder