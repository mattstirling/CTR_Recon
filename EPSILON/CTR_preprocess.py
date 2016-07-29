'''
Created on Feb 23, 2016

@author: mstirling
'''
import pandas as pd, os
from Map_Rules import apply_map_rule

#in CTR files
in_folder = 'C:/Users/mstirling/Desktop/Shared/RW/CTR Files/21-JUL-16/'
in_file_CTRS = 'EPSILON/EPSILON_Credit_Total_Return_Swap_D_20160721_27_RiskWatch.csv'
in_file_TRS = 'EPSILON/EPSILON_Equity_Swap_D_20160721_27_RiskWatch.csv'

#in map files
map_folder = in_folder
map_file = 'map/map_EPSILON.csv'

#out files
out_folder = in_folder + 'out_EPSILON/'
out_file = 'out_TRS.csv'

#open in_files
df_CTRS = pd.read_csv(in_folder+in_file_CTRS)
df_TRS = pd.read_csv(in_folder+in_file_TRS)

#Merge 2 CTR files/dataframes into 1 file/dataframe
df_merge = pd.concat([df_CTRS,df_TRS],axis=0)
df_merge.reset_index(inplace=True)

#apply mapping rules
df_map = pd.read_csv(map_folder+map_file)
for i in df_map['Column Name'].index:
    this_col = str(df_map.at[i,'Column Name'])
    this_map_rule = str(df_map.at[i,'CTR Map Rule'])
    
    #apply the mapping rule if rule 'not nan/blank'
    if not this_map_rule == 'nan':
        for j in df_merge.index:
            df_merge.at[j, this_col] = apply_map_rule(df_merge.at[j, this_col], this_map_rule) 

#sort the CTR dataframe by Name
sort_col = 'Name'
df_merge.sort(sort_col, inplace = True)

#write out_files
try: os.stat(out_folder[:-1])
except: os.mkdir(out_folder[:-1])

#df_merge.to_csv(out_folder + out_file_merged,index=False,columns=out_cols_FX_Deals)
df_merge.to_csv(out_folder + out_file,index=False)

print 'done.'
print 'from ' + in_folder
print 'to ' + out_folder


