'''
Created on Feb 23, 2016

@author: mstirling
'''
import pandas as pd

#control variables
sort_col = 'Ticket'

#file variables
in_folder = 'C:/Temp/python/in/RW files/GSBL/'
in_file_SBL_list = ['GSBL_OpenFwdContracts_ALL_TFRM_20160222.csv',
                    'GSBL_OpenFwdContracts_ALL_TFRM_20160223.csv',
                    'GSBL_OpenFwdContracts_ALL_TFRM_20160224.csv']

#in map files
in_map_folder = 'C:/Temp/python/in/CTR_RW_Map/GSBL/'
in_map_file_SBL = 'CTR_RW_Map_SBL_trade_list.csv'

#out folder
out_folder = 'C:/Temp/python/out/RW Files/GSBL/'

#open mapping files
df_map_SBL = pd.read_csv(in_map_folder+in_map_file_SBL)

#get columns to write from mapping files
out_cols_SBL = [col for col in df_map_SBL['RW Column Name']]

for in_file_SBL in in_file_SBL_list:
    #out file name
    out_file_SBL = 'trade_id_list_' + in_file_SBL
    
    #open in_files
    df_SBL = pd.read_csv(in_folder+in_file_SBL)
    
    #apply a filter based on Tran Type
    df_SBL = df_SBL[df_SBL['Tran Type'].isin(['RR','R','BL','BD'])] 
    
    #sort
    df_SBL.sort(sort_col, inplace = True)
    
    #write out_files
    df_SBL.to_csv(out_folder + out_file_SBL,columns=out_cols_SBL,index=False)
    
print 'done.'
print 'from ' + in_folder
print 'to ' + out_folder
