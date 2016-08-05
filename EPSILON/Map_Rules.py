'''
Created on Feb 24, 2016

@author: mstirling
'''
import numpy as np
import re

def apply_map_rule(value,rulename):
    
    try:
        if rulename == 'KO_dot_right6': return KO_dot_right6(value)
        elif rulename == 'colon_KO_dot_right6': return colon_KO_dot_right6(value)
        elif rulename == 'add_bracket_add_2decimals': return add_bracket_add_2decimals(value)
        elif rulename == 'add_2decimals': return add_2decimals(value)
        elif rulename == 'Y_to_true':return Y_to_true(value)
        elif rulename == 'round_to_2decimal':return round_to_2decimal(value)
        elif rulename == 'replace_bar_with_comma':return replace_bar_with_comma(value) 
        elif rulename == 'add_colon':return add_colon(value)
        elif rulename == 'replace_bar_and_remove_trailing_zeros': return replace_bar_and_remove_trailing_zeros(value)
        elif rulename == 'map_freq':return map_freq(value)
        elif rulename == 'remove_zerovalue_resets':return remove_zerovalue_resets(value)
        elif rulename == 'remove_trailing_zero_from_gl_notional':return remove_trailing_zero_from_gl_notional(value)
        else: return 'rule not in if-else tree'
    except:
        return value

def remove_trailing_zero_from_gl_notional(value):
    temp_str = re.sub(r'([0-9])[.]00\s([a-zA-Z])',r'\1 \2',value)
    temp_str = re.sub(r'([0-9][.][1-9])0\s([a-zA-Z])',r'\1 \2',temp_str)
    return temp_str

def map_freq(value):
    dict_case = {
            'Mon': 'Month'
            ,'Quarter':'QURT'
            }
    return dict_case.get(value,value)

def remove_zerovalue_resets(value):
    #return str(type(value))
    return re.sub(r'(,\s0)+',r'',value)                 #5.6, 0, 0, 0 -> 5.6  
 
def replace_bar_and_remove_trailing_zeros(value):
    temp_str = re.sub(r'([^0])(0*)([|])',r'\1, ',value) #remove trailing zeros from numbers
    temp_str = re.sub(r'([^0])(0*)$',r'\1',temp_str)    #remove trailing zero from the final number
    temp_str = re.sub(r'[.],',',',temp_str)             #89. -> 89
    temp_str = re.sub(r'[.]$','',temp_str)              #89. -> 89
    temp_str = re.sub(r'^0[.]','.',temp_str)            #remove leading zero
    temp_str = re.sub(r'\s0[.]',' .',temp_str)          #remove leading zero
    temp_str = re.sub(r'-0[.]','-.',temp_str)           #remove leading zero
    temp_str = re.sub(r'(,\s0)+',r'',temp_str)          #5.6, 0, 0, 0 -> 5.6
    return temp_str
    
def replace_bar_with_comma(value):
    #actually replacing with "comma + space"
    return str(value).replace('|',', ')
    

def round_to_2decimal(value):
    return np.round(value,0)

def KO_dot_right6(value):
    return 'KO' + value[-6:]

def colon_KO_dot_right6(value):
    return ':KO' + value[-6:]

def add_bracket_add_2decimals(value):
    date_num_USD = value.split(' ')
    return '(' + date_num_USD[0] + ' ' '{0:.2f}'.format(float(date_num_USD[1])) + ' ' +date_num_USD[2] + ')' 

def add_2decimals(value):
    num_USD = value.split(' ')
    return '{0:.2f}'.format(float(num_USD[0])) + ' ' +num_USD[1]

def Y_to_true(value):
    if value=='Y': return 'True'
    else: return value

def add_colon(value):
    return ':' + str(value)
    
       