'''
Created on Aug 12, 2016

@author: cnamgoong
'''
import pandas as pd
from Map_Rules import apply_map_rule

#control variables
bWriteReport = 1

#in VAR files
in_folder = 'C:/Users/mstirling/Desktop/Shared/RW/VAR Session/market.16.08.12/'
in_file_CapFloor = 'all/ByProduct/out_20160912_deals_BNS_CapFloor.csv' 

#in mapping rule files
map_folder = ''
map_file = 'map_K2_CapFloor.csv'

#out folder
out_folder = 'C:/Users/mstirling/Desktop/Shared/RW/CTR Files/20160812_DEV/'
out_file_CapFloor_Deals =  'out_K2/' + 'out_K2_CapFloor_VAR_preprocessed_file.csv'

#open in_files
df_CapFloor = pd.read_csv(in_folder+in_file_CapFloor)
#print len(df_TRS.index)

#filter 
file_list_in_scope = ['/__bns__derivProdData__riskWatch__EMERGINGMEX__MXN__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__EMERGINGMKT__MXN__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__LDNINFLATION__EUR__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__LDNOPTIONS__EUR__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__LDNOPTIONS__GBP__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__LDNOPTIONS__USD__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__MEXJV__MXN__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__MEXJV__USD__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__MEXTREASURY__MXN__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__MEXTREASURY__USD__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__NYDERIV__USD__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__NYOPTIONS__USD__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__RETAIL__ALL__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__STRUCTURED__ALL__Sybase_K2.csv'
                      ,'/__bns__derivProdData__riskWatch__TORUSFI__USD__Sybase_K2.csv']
df_merge = df_CapFloor[(df_CapFloor.Filename.isin(file_list_in_scope))]

#df.sort('C').drop_duplicates(subset=['A', 'B'], take_last=True)

df_merge.reset_index(inplace=True,drop=True)
print len(df_merge.index)

#remove all placeholder deals
df_merge = df_merge[(~df_merge['Placeholder'] == True)]

#reorder columns
df_merge.sort_index(axis=1,inplace=True)

#open mapping rules
df_map = pd.read_csv(map_folder+map_file)

#apply transformation for alias
#copy alias values to real column and drop alias column
for i in df_map[~df_map['RW Alias'].isnull()].index:
    #assume only 1 alias per column for now
    this_col = str(df_map.at[i,'Column Name'])
    this_alias = str(df_map.at[i,'RW Alias'])
    
    #copy alias values to 'this_col'
    for j in df_merge[~df_merge[this_alias].isnull()].index:
        df_merge.at[j,this_col] = df_merge.at[j,this_alias] 
    
    #drop alias column
    df_merge.drop([this_alias],axis=1,inplace=True)

#now apply 'within-cell' mapping rules
for i in df_map['Column Name'].index:
    this_col = str(df_map.at[i,'Column Name'])
    this_map_rule = str(df_map.at[i,'RW Map Rule'])
    
    #apply the mapping rule if rule 'not nan/blank'
    if not this_map_rule == 'nan':
        for j in df_merge.index:
            df_merge.at[j, this_col] = apply_map_rule(df_merge.at[j, this_col], this_map_rule) 

#sort by Name
df_merge.sort('Name', inplace = True)

#write out_files
df_merge.to_csv(out_folder + out_file_CapFloor_Deals,index=False)

print 'done.'
print 'from ' + in_folder
print 'to ' + out_folder