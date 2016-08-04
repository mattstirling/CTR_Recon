'''
Created on Feb 23, 2016

@author: mstirling
'''
import pandas as pd
from GSBL_Map_Rules import GSBL_apply_map_rule

#control variables
b_merge_data = 0

#in files
in_folder = 'C:/Temp/python/in/CTR files/GSBL/20160330/'
in_file_SBL = 'GSBL_SBL_Exposure_D_20160330_25_Stress_Testing.csv'
in_file_Repo = 'GSBL_Repo_Reverse_Repo_D_20160330_25_Stress_Testing.csv'
in_file_Collateral = 'GSBL_SBL_Collateral_D_20160330_25_Stress_Testing.csv'

#in map files
in_map_folder = 'C:/Temp/python/in/CTR_RW_Map/GSBL/'
in_map_file_SBL = 'CTR_RW_Map_SBL_trade_list.csv'
in_map_file_Repo = in_map_file_SBL
in_map_file_Collateral = in_map_file_SBL

#out files
out_folder = 'C:/Temp/python/out/CTR Files/GSBL/'
out_file_SBL = 'trade_id_list_' + in_file_SBL
out_file_Repo = 'trade_id_list_' + in_file_Repo
out_file_Collateral = 'trade_id_list_' + in_file_Collateral

#open in_files
df_SBL = pd.read_csv(in_folder+in_file_SBL)
df_Repo = pd.read_csv(in_folder+in_file_Repo)
df_Collateral = pd.read_csv(in_folder+in_file_Collateral)

#open mapping files
df_map_SBL = pd.read_csv(in_map_folder+in_map_file_SBL)
df_map_Repo = pd.read_csv(in_map_folder+in_map_file_Repo)
df_map_Collateral = pd.read_csv(in_map_folder+in_map_file_Collateral)

#get columns to write from mapping files
#out columns are the same for all
out_cols_SBL = [col for col in df_map_SBL['RW Column Name']]

#apply mapping rules
# 1 - SBL
for i in df_map_SBL['CTR Column Name'].index:
    this_RW_col = str(df_map_SBL.at[i,'RW Column Name'])
    this_CTR_col = str(df_map_SBL.at[i,'CTR Column Name'])
    this_CTR_map_rule = str(df_map_SBL.at[i,'CTR Map Rule'])
    
    #apply the mapping rule if rule 'not nan/blank'
    if not this_CTR_map_rule == 'nan':
        for j in df_SBL.index:
            df_SBL.at[j, this_CTR_col] = GSBL_apply_map_rule(df_SBL.at[j, this_CTR_col], this_CTR_map_rule)
            
    #map the CTR column name to the RW column name
    if not this_RW_col == this_CTR_col:
        df_SBL.rename(columns = {this_CTR_col:this_RW_col}, inplace = True)
    
# 2 - Repo
for i in df_map_Repo['CTR Column Name'].index:
    this_RW_col = str(df_map_Repo.at[i,'RW Column Name'])
    this_CTR_col = str(df_map_Repo.at[i,'CTR Column Name'])
    this_CTR_map_rule = str(df_map_Repo.at[i,'CTR Map Rule'])
    
    #apply the mapping rule if rule 'not nan/blank'
    if not this_CTR_map_rule == 'nan':
        for j in df_Repo.index:
            df_Repo.at[j, this_CTR_col] = GSBL_apply_map_rule(df_Repo.at[j, this_CTR_col], this_CTR_map_rule)
            
    #map the CTR column name to the RW column name
    if not this_RW_col == this_CTR_col:
        df_Repo.rename(columns = {this_CTR_col:this_RW_col}, inplace = True)
    
# 3 - Collateral
for i in df_map_Collateral['CTR Column Name'].index:
    this_RW_col = str(df_map_Collateral.at[i,'RW Column Name'])
    this_CTR_col = str(df_map_Collateral.at[i,'CTR Column Name'])
    this_CTR_map_rule = str(df_map_Collateral.at[i,'CTR Map Rule'])
    
    #apply the mapping rule if rule 'not nan/blank'
    if not this_CTR_map_rule == 'nan':
        for j in df_Collateral.index:
            df_Collateral.at[j, this_CTR_col] = GSBL_apply_map_rule(df_Collateral.at[j, this_CTR_col], this_CTR_map_rule)
            
    #map the CTR column name to the RW column name
    if not this_RW_col == this_CTR_col:
        df_Collateral.rename(columns = {this_CTR_col:this_RW_col}, inplace = True)

#sort the CTR dataframe by Ticket
sort_col = 'Ticket'
if b_merge_data:
    #Merge 2 CTR files/dataframes into 1 file/dataframe
    df_CTR_Merged = pd.concat([df_SBL,df_Repo,df_Collateral],keys=['SBL','Repo','Collateral'])
    #df4 = df3.drop_duplicates(subset='rownum', take_last=True)
    
    #sort
    df_CTR_Merged.sort(sort_col, inplace = True)

    #write out_files
    df_CTR_Merged.to_csv(out_folder + out_file_SBL,index=False,columns=out_cols_SBL)

else:
    #sort
    df_SBL.sort(sort_col, inplace = True)
    df_Repo.sort(sort_col, inplace = True)
    df_Collateral.sort(sort_col, inplace = True)
    
    #write out_files
    df_SBL.to_csv(out_folder + out_file_SBL,index=False,columns=out_cols_SBL)
    df_Repo.to_csv(out_folder + out_file_Repo,index=False,columns=out_cols_SBL)
    df_Collateral.to_csv(out_folder + out_file_Collateral,index=False,columns=out_cols_SBL)

print 'done.'
print 'from ' + in_folder
print 'to ' + out_folder
