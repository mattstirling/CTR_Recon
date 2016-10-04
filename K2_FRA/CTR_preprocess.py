'''
Created on Aug 23, 2016

@author: cnamgoong
'''
import pandas as pd, os, ConfigParser
from Map_Rules import apply_map_rule

#open config file
config = ConfigParser.ConfigParser()
config.read('config.ini')

#in CTR files
in_folder = config.get('filename','in_folder_CTR')
in_file_Fra = config.get('filename','in_file_CTR')

#in map files
map_folder = config.get('filename','in_folder_map')
map_file = config.get('filename','in_file_map')

#out files
out_folder = config.get('filename','out_folder')
out_file = config.get('filename','out_file_CTR')

#open in_files
df_K2 = pd.read_csv(in_folder+in_file_Fra)

#Merge 2 CTR files/dataframes into 1 file/dataframe
df_merge = pd.concat([df_K2],axis=0)
df_merge.reset_index(inplace=True,drop=True)

#drop the deals with Issue Date = File Creation Date
df_merge = df_merge[(~df_merge['Issue Date'].str.contains("2016/09/27"))]

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