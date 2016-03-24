'''
Created on Mar 8, 2016

@author: mstirling

Outcome #1:
based on this comparison, both the TFRM file and the CTR file has the valuation date in their filename
match like-for-like when comparing the files

'''
import pandas as pd
#s1 = pd.merge(df1, df2, how='inner', on=['user_id'])

#CTR file list
out_folder_CTR = 'C:/Temp/python/out/CTR Files/GSBL/'
out_file_CTR_list = ['trade_id_list_' + 'GSBL_SBL_Exposure_D_20160224_25_Stress_Testing.csv',
                     'trade_id_list_' + 'GSBL_Repo_Reverse_Repo_D_20160224_25_Stress_Testing.csv',
                     'trade_id_list_' + 'GSBL_SBL_Collateral_D_20160224_25_Stress_Testing.csv',
                     'trade_id_list_' + 'ANVILLON_Repo_Reverse_Repo_D_20160224_10_Stress_Testing.csv',
                     'trade_id_list_' + 'ANVILNY_Repo_Reverse_Repo_D_20160224_16_Stress_Testing.csv',
                     'trade_id_list_' + 'ANVILTOR_Repo_Reverse_Repo_D_20160224_15_Stress_Testing.csv']

#RW file list
out_folder_RW = 'C:/Temp/python/out/RW Files/GSBL/'
in_file_SBL_list = ['trade_id_list_'+'GSBL_OpenFwdContracts_ALL_TFRM_20160224.csv']

for file_CTR in out_file_CTR_list:
    #open df
    df_CTR = pd.read_csv(out_folder_CTR+file_CTR)
    size_CTR = df_CTR.size
    
    for file_RW in in_file_SBL_list:  
        #open df
        df_RW = pd.read_csv(out_folder_RW+file_RW)
        size_RW = df_RW.size
        
        df_overlap = pd.merge(df_CTR, df_RW, how='inner', on=['Ticket'])
        size_overlap = df_overlap.size
        
        print(file_CTR + ', ' +str(size_CTR))  
        print(file_RW + ', ' +str(size_RW))
        print('overlap' + ', ' +str(size_overlap))
        print('')

print 'done.'
print 'between ' + out_folder_CTR
print 'and ' + out_folder_RW
