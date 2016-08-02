'''
Created on July 27, 2016

@author: cnamgoong
'''
import numpy as np
import re

def apply_map_rule(value,rulename):
    
    try:
        if rulename == 'remove_objcharlie': return remove_objcharlie(value)
        elif rulename == 'remove_xcharlie': return remove_xcharlie(value)
        elif rulename == 'remove_idxcharlie': return remove_idxcharlie(value)
        elif rulename == 'remove_idobjcharlie': return remove_idobjcharlie(value)
        elif rulename == 'not_in_scope': return not_in_scope(value)
        elif rulename == 'already_known': return already_known(value)
        else: return 'rule not in if-else tree'
    except:
        return value
    
def already_known(value):
    value = None
    return

def remove_objcharlie(value):
    return str(value)[10:]

def remove_idobjcharlie(value):
    return str(value)[11:]

def remove_xcharlie(value):
    code = str(value)[9:12].strip()
    str_num = str(value)[-6:].strip()
    dict_case = {
                'MAL':'KL'
                ,'SEL':'SE'
                , 'HKG' : 'HK'
                , 'IND' : 'IN'
                , 'SH' : 'CN'
                , 'SIN' : 'SP'
                }
    new_code = dict_case.get(code,code)
    return new_code + '.' + str_num

def remove_idxcharlie(value):
    code = str(value)[10:13].strip()
    str_num = str(value)[-6:].strip()
    dict_case = {
                'MAL':'KL'
                ,'SEL':'SE'
                , 'HKG' : 'HK'
                , 'IND' : 'IN'
                , 'SH' : 'CN'
                , 'SIN' : 'SP'
                }
    new_code = dict_case.get(code,code)
    return new_code + '.' + str_num
 
def not_in_scope(value):
    return None