'''
Created on Nov 28, 2016

@author: mstirling
'''

in_folder = '//scglobal.ad.scotiacapital.com/sc5/FILES/TAG_Common/Application Development/Non Retail Credit Process/Prod files/K2/Vector Testing/'
in_file = 'JIRA 6424/Principal Cashflow/ctrfeed_CCSwap_PayPrincipalCashflow.csv'

f_in = open(in_folder + in_file,'r')

for i in range(10):
    print f_in.readline().strip()


