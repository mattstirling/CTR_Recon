'''
Created on July 27, 2016

@author: cnamgoong
'''
import pandas as pd, os, ConfigParser,re
from Map_Rules import apply_map_rule  # @UnresolvedImport

def get_first_OBJCHARLIEIN_filename(filelist):
    #want the lower version number of the OBJCHARLIEIN_ file
    match_version_list = []
    match_file_list = []
    
    for f in filelist:
        match = re.search(r'OBJCHARLIEIN_FX_Forward_D_[0-9]{8}_([0-9]+)_RiskWatch.csv', f)
        if match:
            match_version_list.append(int(match.group(1)))
            match_file_list.append(f)
    
    if len(match_version_list) > 0:
        return match_file_list[match_version_list.index(min(match_version_list))]

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

#get list of in_files for OBJCHARLIE
#want only OBJCHARLIE files
#want only _FX_Forward_D_ and _NDF_D_
#want the lower version number of the OBJCHARLIEIN_ file
all_filenames = [f for f in os.listdir(in_folder) if os.path.isfile(os.path.join(in_folder, f))]
in_filenames = ([f for f in all_filenames 
                  if f[-4:] == '.csv'
                  and f[:10] == 'OBJCHARLIE' 
                  and ('_FX_Forward_D_' in f or '_NDF_D_' in f)
                  and 'OBJCHARLIEIN' not in f])
#want the lower version number of the OBJCHARLIEIN_ file
in_filenames.append(get_first_OBJCHARLIEIN_filename(all_filenames))

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

#apply mapping rules
df_map = pd.read_csv(map_folder+map_file)
for i in df_map['Column Name'].index:
    this_col = str(df_map.at[i,'Column Name'])
    this_map_rule = str(df_map.at[i,'CTR Map Rule'])
    
    #apply the mapping rule if rule 'not nan/blank'
    if not this_map_rule == 'nan':
        for j in df_merge.index:
            df_merge.at[j, this_col] = apply_map_rule(df_merge.at[j, this_col], this_map_rule)
            if(this_col == 'Include Notional'):
                print "VALUE ::  >>>> ", df_merge.at[j, this_col]
            
            #print j 

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
