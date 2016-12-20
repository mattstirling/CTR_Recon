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
        elif rulename == 'asset_reset_freq_remap':return asset_reset_freq_remap(value)
        elif rulename == 'comma_list_of_num_add_10decimals':return comma_list_of_num_add_10decimals(value)
        elif rulename == 'add_colon':return add_colon(value)
        elif rulename == 'right7':return right7(value)
        elif rulename == 'remove_systemprefix':return remove_systemprefix(value)
        else: return 'rule not in if-else tree'
    except:
        return value

def remove_systemprefix(value):
    return str(value).strip().split('.')[1]

def right7(value):
    return str(value)[-7:]

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

def replace_bar_with_comma(value):
    #actually replacing with ', ', not ','
    return str(value).replace('|',', ')

def asset_reset_freq_remap(value):
    if str(value) in ('nan','NaT'):
        return value
        
    dict_case = {
                  'Mon': 'Month'
                }
    return dict_case.get(value,value)

def add_10decimals(value):
    return str('{0:.10f}'.format(float(value)))

def comma_list_of_num_add_10decimals(value):
    #
    #hmmm.... this function doesn't work correct right now.
    #
    if str(value) in ('nan','NaT'):
        return value
    
    if isinstance(value, np.ndarray):
        preprocess_str =  ', '.join([str(i) for i in value.tolist()])
    
    elif isinstance(value, basestring):
        preprocess_str =  str(value)
    
    else:
        print type(value)
        return 'missing case in mapping process'
    
    comma_list_val = preprocess_str.split(', ')
    #print comma_list_val
    return ', '.join([add_10decimals(i) for i in comma_list_val])
    
def add_colon(value):
    return ':' + str(value)

