'''
Created on Aug 10, 2016

@author: cnamgoong
'''
import numpy as np
import re

def apply_map_rule(value,rulename):
    
    try:
        if rulename == 'change_flag': return change_flag(value)
        elif rulename == 'boolean_maker': return boolean_maker(value)
        elif rulename == 'pay_holiday' : return pay_holiday(value)
        elif rulename == 'not_in_scope': return not_in_scope(value)        
        elif rulename == 'average_frequency' : return average_frequency(value)
        elif rulename == 'ctr_to_var_name' : return ctr_to_var_name(value)
        elif rulename == 'special_frequency' : return special_frequency(value)
        elif rulename == 'cap_frequency' : return cap_frequency(value)
        elif rulename == 'ctr_id_changer' : return ctr_id_changer(value)
        elif rulename == 'ctr_daycount_changer' : return ctr_daycount_changer(value)
        elif rulename == 'remove_K2prefix_pluspostfix_R': return remove_K2prefix_pluspostfix_R(value)
        elif rulename == 'remove_K2prefix': return remove_K2prefix(value)
        elif rulename == 'remove_systemprefix': return remove_systemprefix(value)
        else: return 'rule not in if-else tree'
    except:
        return value

def remove_systemprefix(value):
    return str(value).strip().split('.')[1]

def remove_K2prefix (value):
    return str(value)[3:]

def remove_K2prefix_pluspostfix_R(value):
    return str(value)[3:] + 'R'
    
def ctr_id_changer(value):
    val = str(value).strip()
    id = val.split(".")[1]
    return ":" + id

def ctr_daycount_changer(value):
    flag = str(value).strip()
    dict_case = {
                'ACT/360' : 'actual/360'
                , 'ACT/365' : 'actual/365'
                , 'ACT360' : '30/360'
                }
    new_flag = dict_case.get(flag,flag)
    return new_flag

def cap_frequency(value):
    flag = str(value).strip()
    dict_case = {
                '28-Day' : '28DAY'
                , 'Month' : 'MON'
                , 'Quarter' : 'QURT'
                , 'semi-annual' : 'SEMI'
                }
    new_flag = dict_case.get(flag,flag)
    return new_flag

def ctr_to_var_name(value):
    value = str(value).strip()
    value = str(value)[3:]
    return value

def not_in_scope(value):
    value = value.strip()
    return None

def change_flag(value):
    value = str(value.strip())
    dict_case = {
                'Sell' : '-1'
                ,'Buy' : '1'
                }
    return dict_case.get(value,value)

def boolean_maker(value):
    flag = str(value).strip()
    dict_case = {
                 'N' : 'False'
                 ,'Y' : 'True'
                 }
    new_flag = dict_case.get(flag,flag)
    return new_flag

def average_frequency(value):
    flag = str(value).strip()
    dict_case = {
                'Month' : 'MON'
                }
    new_flag = dict_case.get(flag,flag)
    return new_flag

def special_frequency(value):
    flag = str(value).strip()
    dict_case = {
                'Month' : 'MONTH'
                }
    new_flag = dict_case.get(flag,flag)
    return new_flag

def pay_holiday(value):
    flag = str(value).strip()
    dict_case = {
                'Err_03' : 'LON;NYC'
                }
    new_flag = dict_case.get(flag,flag)
    return new_flag
