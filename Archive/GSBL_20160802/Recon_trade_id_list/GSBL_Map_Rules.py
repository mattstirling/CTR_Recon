'''
Created on Feb 24, 2016

@author: mstirling
'''
def GSBL_apply_map_rule(value,rulename):
    if rulename == 'GSBL_right7': return GSBL_right7(value)
    
def GSBL_right7(value):
    #format of the ticket is ':GSBL.N_' + '0000000' 
    return str(value)[-7:]


