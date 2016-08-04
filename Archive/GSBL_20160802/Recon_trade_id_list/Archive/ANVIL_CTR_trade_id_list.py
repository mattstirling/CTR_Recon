'''
Created on Feb 23, 2016

@author: mstirling
'''
import pandas as pd
from GSBL_Map_Rules import GSBL_apply_map_rule

#control variables
b_merge_data = 0

#sort the CTR dataframe by Ticket
sort_col = 'Ticket'

#in files
in_folder = 'C:/Temp/python/in/CTR files/ANVIL/'
in_file_list = ['ANVILLON_Repo_Reverse_Repo_D_20160224_10_Stress_Testing.csv',
                'ANVILNY_Repo_Reverse_Repo_D_20160224_16_Stress_Testing.csv',
                'ANVILTOR_Repo_Reverse_Repo_D_20160224_15_Stress_Testing.csv']

#in map files
in_map_folder = 'C:/Temp/python/in/CTR_RW_Map/ANVIL/'
in_map_file = 'CTR_RW_Map_Repo_trade_list.csv'

#out files
out_folder = 'C:/Temp/python/out/CTR Files/GSBL/'

for in_file in in_file_list:
    
    #out files
    out_file = 'trade_id_list_' + in_file
    
    #open in_files
    df_data = pd.read_csv(in_folder+in_file)

    #open mapping files
    df_map = pd.read_csv(in_map_folder+in_map_file)

    #get columns to write from mapping files
    #out columns are the same for all
    out_cols = [col for col in df_map['RW Column Name']]

    #apply mapping rules
    for i in df_map['CTR Column Name'].index:
        this_RW_col = str(df_map.at[i,'RW Column Name'])
        this_CTR_col = str(df_map.at[i,'CTR Column Name'])
        this_CTR_map_rule = str(df_map.at[i,'CTR Map Rule'])
    
        #apply the mapping rule if rule 'not nan/blank'
        if not this_CTR_map_rule == 'nan':
            for j in df_data.index:
                df_data.at[j, this_CTR_col] = GSBL_apply_map_rule(df_data.at[j, this_CTR_col], this_CTR_map_rule)
                
        #map the CTR column name to the RW column name
        if not this_RW_col == this_CTR_col:
            df_data.rename(columns = {this_CTR_col:this_RW_col}, inplace = True)
        

    #sort
    df_data.sort(sort_col, inplace = True)
    
    #write out_files
    df_data.to_csv(out_folder + out_file,index=False,columns=out_cols)
    
print 'done.'
print 'from ' + in_folder
print 'to ' + out_folder
