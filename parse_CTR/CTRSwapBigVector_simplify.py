'''
Created on Sep 15, 2016

@author: mstirling
'''

#in folder + out folder
main_folder = 'C:/Users/mstirling/Desktop/Shared/RW/CTR Files/20160912_Inbound/'
folder = main_folder + 'K2_out/'  

case = 2
if case == 1:
    in_file = 'out_K2_CM_Swap_D_20160912_02_C_Swap_v1_80_Rec_Interest_Cashflow' + '.csv'
    out_file = 'out_K2_CM_Swap_D_20160912_02_C_Swap_v1_80_Rec_Interest_Cashflow' + '_simplify' + '.csv'
    list_of_strings_to_remove = ['C,Swap v1.80:Rec Interest Cashflow,Cross Currency Swap,'
                                 ,'Rec Interest Cashflow,']
elif case == 2:
    in_file = 'out_K2_CM_Swap_D_20160912_02_C_Swap_v1_80_Pay_Interest_Cashflow' + '.csv'
    out_file = 'out_K2_CM_Swap_D_20160912_02_C_Swap_v1_80_Pay_Interest_Cashflow' + '_simplify' + '.csv'
    list_of_strings_to_remove = ['C,Swap v1.80:Pay Interest Cashflow,Cross Currency Swap,'
                                 ,'Pay Interest Cashflow,']

f_out = open(folder + out_file,'w')

for line in open(folder + in_file,'r'):
    this_line = line
    for str in list_of_strings_to_remove:
        this_line = this_line.replace(str,'') 
    f_out.write(this_line)
    


    


