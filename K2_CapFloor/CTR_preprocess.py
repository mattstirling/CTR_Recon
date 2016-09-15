'''
Created on Aug 30, 2016

@author: cnamgoong
'''
import pandas as pd, os
from Map_Rules import apply_map_rule

#in CTR files
in_folder = 'C:/Users/mstirling/Desktop/Shared/RW/CTR Files/20160812_DEV/'
in_file_Cap = 'K2/K2_Cap_D_20160812_1_RiskWatch.csv'
in_file_Floor = 'K2/K2_Floor_D_20160812_1_RiskWatch.csv'

#in map files
map_folder = ''
map_file = 'map_K2_CapFloor.csv'

#out files
out_folder = in_folder + 'out_K2/'
out_file = 'out_K2_CapFloor_CTR_preprocessed_file.csv'

#open in_files
df_Cap = pd.read_csv(in_folder+in_file_Cap)
df_Floor = pd.read_csv(in_folder+in_file_Floor)

#Merge 2 CTR files/dataframes into 1 file/dataframe
df_merge = pd.concat([df_Cap, df_Floor],axis=0)
df_merge.reset_index(inplace=True,drop=True)

#drop the deals with Issue Date = File Creation Date
#df_merge = df_merge[(~df_merge['Issue Date'].str.contains("2016/08/15"))]

#reorder columns
df_merge.sort_index(axis=1,inplace=True)

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

#write out_files
try: os.stat(out_folder[:-1])
except: os.mkdir(out_folder[:-1])

#df_merge.to_csv(out_folder + out_file_merged,index=False,columns=out_cols_FX_Deals)
df_merge.to_csv(out_folder + out_file,index=False)

print 'done.'
print 'from ' + in_folder
print 'to ' + out_folder