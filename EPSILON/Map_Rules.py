'''
Created on Feb 24, 2016

@author: mstirling
'''
def apply_map_rule(value,rulename):
    
    if rulename == 'KO_dot_right6': return KO_dot_right6(value)
    elif rulename == 'colon_KO_dot_right6': return colon_KO_dot_right6(value)
    elif rulename == 'add_bracket_add_2decimals': return add_bracket_add_2decimals(value)
    elif rulename == 'add_2decimals': return add_2decimals(value)
    elif rulename == 'Y_to_true':return Y_to_true(value)

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