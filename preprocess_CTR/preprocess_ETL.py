'''
Created on Aug 10, 2016

@author: cnamgoong
'''
import numpy as np
import re

def rec_rate_funding_ticket_correction(rec_rate,fixed_flag,fixed_rate,spread_rate):
    out_rec_rate = []
    for i in range(len(rec_rate)):
        split_this_vect = rec_rate[i].split('%')
        if float(str(split_this_vect[0]).strip()) > 0 : 
            #case 1.0 % MON ACT/360, return 0 % MON ACT/360
            out_rec_rate.append('0 %' + split_this_vect[1])
        else:
            #case 0 % MON ACT/360, return 1.0 % MON ACT/360
            if str(fixed_flag[i]) == 'True':
                #get the fixed rate
                out_rec_rate.append(str(fixed_rate[i]) + ' %' + split_this_vect[1])
            
            else:
                split_spread = str(spread_rate[i]).split(',')
                if len(split_spread) == 1:
                    if str(spread_rate[i]) == 'nan':
                        out_rec_rate.append('0 %' + split_this_vect[1])
                    else:
                        out_rec_rate.append(str(spread_rate[i]) + ' %' + split_this_vect[1])
                else:
                    out_rec_rate.append(float(split_spread.strip()) + ' %' + split_this_vect[1])
    
    return out_rec_rate
    

def number_list_divide_by_100(value):
    str_num_list = str(value)
    if str_num_list == 'nan': return ''
    str_num_list = str_num_list.split(', ')
    str_num_list = [str(float(i)/100) for i in str_num_list]
    return ', '.join(str_num_list)

def list_bar_to_comma_space(value):
    str_date_list = str(value)
    if str_date_list == 'nan': return ''
    str_date_list = str_date_list.replace('|',', ')
    if ',' not in str_date_list: str_date_list = str_date_list.rstrip(')').lstrip('(') 
    return str_date_list

def list_bar_to_comma_space_with_brackets_always(value):
    str_date_list = str(value)
    if str_date_list == 'nan': return ''
    str_date_list = str_date_list.replace('|',', ').replace(')','').replace('(','')
    return '(' + str_date_list + ')'

def date_list_bar_to_comma_space(value):
    str_date_list = str(value)
    if str_date_list == 'nan': return ''
    return str_date_list.replace('|',', ')

def rec_rate_x100(value):
    str_rec_rate = str(value)
    if str_rec_rate == 'nan' : return ''
    #print str_rec_rate
    str_rec_rate_list = str_rec_rate.split('%')
    #print str(100*float(str_rec_rate_list[0])) + ' %' + str_rec_rate_list[1]
    return str(100*float(str_rec_rate_list[0])) + ' %' + str_rec_rate_list[1]  

def number_list_reverse(value):
    str_num_list = str(value)
    print str_num_list
    if str_num_list in ['nan']: return ''
    num_list = str_num_list.split(',')
    if len(num_list)>1:
        return ', '.join(reversed(num_list))
    else:
        #list of 1 number
        return str_num_list

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
