'''
Created on Feb 23, 2016

@author: mstirling
'''
import pandas as pd
from GSBL.Recon_trade_id_list.GSBL_Map_Rules import GSBL_apply_map_rule

#in files
in_folder = 'C:/Temp/python/in/CTR files/GSBL/'
in_file_SBL = 'GSBL_SBL_Exposure_D_20160224_25_Stress_Testing.csv'

#in map files
in_map_folder = 'C:/Temp/python/in/CTR_RW_Map/GSBL/'
in_map_file_SBL = 'CTR_RW_Map_SBL.csv'

#out files
out_folder = 'C:/Temp/python/out/CTR Files/OC/'
out_file_SBL = 'CTR_denormalized_20160218.csv'

#open in_files
df_SBL = pd.read_csv(in_folder+in_file_SBL)

#open mapping files
df_map_SBL = pd.read_csv(in_map_folder+in_map_file_SBL)

#get columns to write from mapping files
#out_cols are the same per Riskwatch file
out_cols_FX_Deals = [col for col in df_map_SBL['RW Column Name']]

#apply mapping rules
# 1 - FX_Forward (apply mapping rules)
for i in df_map_FX_Forward['CTR Column Name'].index:
    this_CTR_col = str(df_map_FX_Forward.at[i,'CTR Column Name'])
    this_CTR_map_rule = str(df_map_FX_Forward.at[i,'CTR Map Rule'])
    
    #apply the mapping rule if rule 'not nan/blank'
    if not this_CTR_map_rule == 'nan':
        for j in df_FX_Forward.index:
            df_FX_Forward.at[j, this_CTR_col] = OC_apply_map_rule(df_FX_Forward.at[j, this_CTR_col], this_CTR_map_rule) 

# 2 - NDF (apply mapping rules)
for i in df_map_FX_NDF['CTR Column Name'].index:
    this_CTR_col = str(df_map_FX_NDF.at[i,'CTR Column Name'])
    this_CTR_map_rule = str(df_map_FX_NDF.at[i,'CTR Map Rule'])
    
    #apply the mapping rule if rule 'not nan/blank'
    if not this_CTR_map_rule == 'nan':
        for j in df_FX_NDF.index:
            df_FX_NDF.at[j, this_CTR_col] = OC_apply_map_rule(df_FX_NDF.at[j, this_CTR_col], this_CTR_map_rule) 

#Merge 2 CTR files/dataframes into 1 file/dataframe
df_CTR_Merged = pd.concat([df_FX_Forward,df_FX_NDF],keys=['FX_Forward','NDF'])

#sort the CTR dataframe by Name
sort_col = 'Name'
df_CTR_Merged.sort(sort_col, inplace = True)

#write out_files
df_CTR_Merged.to_csv(out_folder + out_file_merged,index=False,columns=out_cols_FX_Deals)
#df_FX_Forward.to_csv(out_folder + out_file_FX_Forward,index=False,columns=out_cols_FX_Deals)

print 'done.'
print 'from ' + in_folder
print 'to ' + out_folder


