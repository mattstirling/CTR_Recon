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
        elif rulename == 'disc_curve_changer' : return disc_curve_changer(value)
        elif rulename == 'forw_curve_changer' : return forw_curve_changer(value)
        elif rulename == 'pay_lag_convention' : return pay_lag_convention(value)
        elif rulename == 'pay_holiday' : return pay_holiday(value)
        elif rulename == 'not_in_scope': return not_in_scope(value)        
        elif rulename == 'varstr_rate' : return varstr_rate(value)
        elif rulename == 'round_notional' : return round_notional(value)
        elif rulename == 'prod_type' : return prod_type(value)
        elif rulename == 'ctrstr_rate' : return ctrstr_rate(value)
        elif rulename == 'placeholder' : return 'FRA' #placeholder(value)
        else: return 'rule not in if-else tree'
    except:
        return value

def round_notional(value):
    amount = str(value)[:-3]
    amount = amount.split(".")[0]
    return amount.strip()

def not_in_scope(value):
    value = value.strip()
    return None

def ctrstr_rate(value):
    val = str(value).strip()
    perc = val.split(" %")[0]
    new_perc = round(perc, 6)
    return new_perc + " % ANNU"

def prod_type(value):
    val = float('FALSE')
    return val

def placeholder(value):
    val = value + 'FRA'
    return val

def varstr_rate(value):
    val = str(value).strip()
    perc = val.split(" %")[0]
    perc = perc.rstrip("0") #remove trailing zeros from numbers
    if str(perc)[0] == '-' :
        if str(perc)[1] == '0' :
            perc = '-' + str(perc)[2:]
        else : 
            perc = str(perc)[1:]
    elif str(perc)[0] == '0':
        perc = str(perc)[1:]
    return perc + " % ANNU"
    
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

def disc_curve_changer(value):
    flag = str(value).strip()
    dict_case = {
                ':sUSDMid' : ':USDsUSD1dMid'
                ,':sGBPMid' : ':GBPsGBP1dMid'
                ,':sEURMid' : ':EURsEUR1dMid'
                ,':sCADMid' : ':CADsCAD1dMid'
                }
    new_flag = dict_case.get(flag,flag)
    return new_flag

def forw_curve_changer(value):
    flag = str(value).strip()
    dict_case = {
                ':sEURMid' : ':EURsEUR6mMid'
                ,':sGBPMid' : ':GBPsGBP6mMid'

                }
    new_flag = dict_case.get(flag,flag)
    return new_flag

def pay_lag_convention(value):
    flag = str(value).strip()
    dict_case = {
                'Err_03' : 'Business'
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
