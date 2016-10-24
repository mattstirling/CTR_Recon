'''
Created on Feb 23, 2016

@author: mstirling
'''
import pandas as pd, os, ConfigParser, re
from Map_Rules import apply_map_rule  # @UnresolvedImport

def filename_to_RWyyyymmdd(filename):
    match = re.search(r'.*_D_([0-9]{4})([0-9]{2})([0-9]{2})_.*',filename)
    if match: return match.group(1) + '/' + match.group(2) + '/' + match.group(3) 

#open config file
config = ConfigParser.ConfigParser()
config.read('config.ini')

#in folder
in_folder = config.get('filename','in_folder_CTR')

#in map files
map_folder = config.get('filename','in_folder_map')
map_file = config.get('filename','in_file_map')

#out files
out_folder = config.get('filename','out_folder')
out_file = config.get('filename','out_file_CTR')

#get list of in_files
#want only ANVIL repo files + Impact triparty files
#want only _Repo_Reverse_Repo_D_
all_filenames = [f for f in os.listdir(in_folder) if os.path.isfile(os.path.join(in_folder, f))]
in_filenames = ([f for f in all_filenames 
                  if f[-4:] == '.csv'
                  and (f[:2] == 'K2')  
                  and ('_Interest_Rate_Swap_D_' in f)])

#prefix the directory
in_filenames = [in_folder + f for f in in_filenames]

#open each file into a dataframe (all have same header)
df_list = []
for f in in_filenames:
    df_list.append(pd.read_csv(f))

#merge all dataframes into 1
df_merge = pd.concat(df_list,axis=0)     
df_merge.reset_index(inplace=True)

#filter on the maturity date
business_date = filename_to_RWyyyymmdd(in_filenames[0])
#df_merge = df_merge[(~df_merge['Maturity Date'].str.contains(business_date))]

print 'CTR num records: ' + str(len(df_merge.index))
print 'CTR num columns: ' + str(len(df_merge.columns))

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


