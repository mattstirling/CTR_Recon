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
folder_A = 'C:/Temp/python/out/CTR Files/GSBL/'
file_A_list = ['trade_id_list_' + 'GSBL_SBL_Exposure_D_20160224_25_Stress_Testing.csv',
                     'trade_id_list_' + 'GSBL_Repo_Reverse_Repo_D_20160224_25_Stress_Testing.csv',
                     'trade_id_list_' + 'GSBL_SBL_Collateral_D_20160224_25_Stress_Testing.csv']

#RW file list
#folder_B = 'C:/Temp/python/out/RW Files/GSBL/'
#file_B_list = ['trade_id_list_'+'GSBL_OpenFwdContracts_ALL_TFRM_20160224.csv']
folder_B = 'C:/Temp/python/out/CTR Files/GSBL/'
file_B_list = ['trade_id_list_' + 'GSBL_SBL_Collateral_D_20160224_25_Stress_Testing.csv']

for file_A in file_A_list:
    #open df
    df_A = pd.read_csv(folder_A+file_A)
    size_A = df_A.size
    
    for file_B in file_B_list:  
        #open df
        df_B = pd.read_csv(folder_B+file_B)
        size_B = df_B.size
        
        df_overlap = pd.merge(df_A, df_B, how='inner', on=['Ticket'])
        size_overlap = df_overlap.size
        
        print(file_A + ', ' +str(size_A))  
        print(file_B + ', ' +str(size_B))
        print('overlap' + ', ' +str(size_overlap))
        print('')

print 'done.'
print 'between ' + folder_A
print 'and ' + folder_B
