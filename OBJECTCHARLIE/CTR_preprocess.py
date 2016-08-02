'''
Created on July 27, 2016

@author: cnamgoong
'''
import pandas as pd, os
from Map_Rules import apply_map_rule

#in CTR files
in_folder = 'C:/Users/mstirling/Desktop/Shared/RW/CTR Files/21-JUL-16/'
in_file_CN = 'OBJECTCHARLIE/OBJCHARLIECN_FX_Forward_D_20160721_1_RiskWatch.csv'
in_file_GZ = 'OBJECTCHARLIE/OBJCHARLIEGZ_FX_Forward_D_20160721_1_RiskWatch.csv'
in_file_HK = 'OBJECTCHARLIE/OBJCHARLIEHK_FX_Forward_D_20160721_1_RiskWatch.csv'
in_file_IN = 'OBJECTCHARLIE/OBJCHARLIEIN_FX_Forward_D_20160721_1_RiskWatch.csv'
in_file_KL = 'OBJECTCHARLIE/OBJCHARLIEKL_FX_Forward_D_20160721_1_RiskWatch.csv'
in_file_SE = 'OBJECTCHARLIE/OBJCHARLIESE_FX_Forward_D_20160721_1_RiskWatch.csv'
in_file_SP = 'OBJECTCHARLIE/OBJCHARLIESP_FX_Forward_D_20160721_16_RiskWatch.csv'
in_file_TP = 'OBJECTCHARLIE/OBJCHARLIETP_FX_Forward_D_20160721_1_RiskWatch.csv'
in_file_HKNDF = 'OBJECTCHARLIE/OBJCHARLIEHK_NDF_D_20160721_1_RiskWatch.csv'
in_file_SENDF = 'OBJECTCHARLIE/OBJCHARLIESE_NDF_D_20160721_1_RiskWatch.csv'
in_file_SPNDF = 'OBJECTCHARLIE/OBJCHARLIESP_NDF_D_20160721_16_RiskWatch.csv'
in_file_TPNDF = 'OBJECTCHARLIE/OBJCHARLIETP_NDF_D_20160721_1_RiskWatch.csv'

#in map files
map_folder = ''
map_file = 'map_OBJECTCHARLIE.csv'

#out files
out_folder = in_folder + 'out_OBJECTCHARLIE/'
out_file = 'out_FXFORWARD.csv'

#open in_files
df_CN = pd.read_csv(in_folder+in_file_CN)
df_GZ = pd.read_csv(in_folder+in_file_GZ)
df_HK = pd.read_csv(in_folder+in_file_HK)
df_IN = pd.read_csv(in_folder+in_file_IN)
df_KL = pd.read_csv(in_folder+in_file_KL)
df_SE = pd.read_csv(in_folder+in_file_SE)
df_SP = pd.read_csv(in_folder+in_file_SP)
df_TP = pd.read_csv(in_folder+in_file_TP)
df_HKNDF = pd.read_csv(in_folder+in_file_HKNDF)
df_SENDF = pd.read_csv(in_folder+in_file_SENDF)
df_SPNDF = pd.read_csv(in_folder+in_file_SPNDF)
df_TPNDF = pd.read_csv(in_folder+in_file_TPNDF)

#Merge 8 CTR files/dataframes into 1 file/dataframe
df_merge = pd.concat([df_CN,df_GZ,df_HK,df_IN,df_KL,df_SE,df_SP,df_TP,df_HKNDF,df_SENDF,df_SPNDF,df_TPNDF],axis=0)
df_merge.reset_index(inplace=True)

df_merge = df_merge[(~df_merge['Maturity Date'].str.contains("2016/07/21"))]


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