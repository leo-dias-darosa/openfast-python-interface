# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 17:31:04 2018

@author: Leonardo
"""

import pandas as pd
import matplotlib.pyplot as plt
import xlwt
import os

def plot(parameters):
    
    path_turbsim = parameters[0]
    turbsim = parameters[1]
    path_fast = parameters[2]
    path_modules = parameters[3]
    turbinefast=parameters[4]
    v = parameters[5]
    h = parameters[6]
    t = parameters[7]
    s = parameters[8]
    e=parameters[9]
    n=parameters[10]
    frequency = parameters[11]
    simulink = parameters[12]

    fast_standard = open(path_fast+turbinefast).read().splitlines()
    turbinefast = turbinefast[0:len(turbinefast)-4]
    out =turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'.sfunc.out'

    fault_col=  path_fast+turbinefast+' - Customized Simulation - Simulink/'+turbinefast+'-'+str(v)+'ms - Failure/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/'

    normal_col=  path_fast+turbinefast+' - Customized Simulation - Simulink/'+turbinefast+'-'+str(v)+'ms - Normal/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/'
        
    path_comparison = path_fast+turbinefast+' - Customized Simulation - Simulink/'

    out = out[0:len(out)-4]
    
    out_header = open(normal_col+out+'.out').read().splitlines()
    out_noHeader = open(normal_col+out+'noHeader.out','w')

    i = 0
    for linha in out_header:
            if i >5:
                    out_noHeader.write(linha+'\n')
            else:
                    i=i+1
    out_noHeader.close()

    df = pd.read_fwf(normal_col+out+'noHeader.out')
    df.to_csv(normal_col+out+'noHeader.csv')


    out_header = open(fault_col+out+'.out').read().splitlines()
    out_noHeader = open(fault_col+out+'noHeader.out','w')

    i = 0
    for linha in out_header:
            if i >5:
                    out_noHeader.write(linha+'\n')
            else:
                    i=i+1
    out_noHeader.close()

    df = pd.read_fwf(fault_col+out+'noHeader.out')
    df.to_csv(fault_col+out+'noHeader.csv')


    ## Get data
        
    data_normal_col = pd.read_csv(normal_col+out+'noHeader.csv',header=None)
    data_fault_col= pd.read_csv(fault_col+out+'noHeader.csv',header=None)

    output = data_normal_col.iloc[0,0:]
    output = [str(x) for x in output]
    legend = data_normal_col.iloc[1,0:]
    legend = [str(x) for x in legend]
       
    Time = data_normal_col.iloc[2:,0]
    Time = [float(x) for x in Time]


#### Get outlist normal collective
        
    fig_normal_col=[]
    
    for i in range(1,len(data_normal_col.columns)):
        series =data_normal_col.iloc[2:,i]
        fig_normal_col.append(series)
    for i in range(len(fig_normal_col)):
        fig_normal_col[i]=[float(x) for x in fig_normal_col[i]]

#### Get outlist fault collective
        
    fig_fault_col=[]
    
    for i in range(1,len(data_fault_col.columns)):
        series =data_fault_col.iloc[2:,i]
        fig_fault_col.append(series)
    for i in range(len(fig_normal_col)):
        fig_fault_col[i]=[float(x) for x in fig_fault_col[i]]


#### Plots ####

    for i in range(len(legend)):
        legend[i] = legend[i][1:len(legend[i])-1]

    for i in range(len(data_normal_col)):

        plt.close('all')
        plt.figure()

        plt.subplot(3,1,1)
        plt.plot(Time,fig_normal_col[i],label='Normal Collective')
        plt.plot(Time,fig_fault_col[i],label='Fault Collective')
        plt.title(output[i+1])
        plt.ylabel(legend[i+1])
        plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
        plt.tick_params(axis='x',labelbottom=False)
        plt.box(on=None)

        plt.tight_layout()
        plt.savefig(path_comparison+output[i+1]+'.png',bbox_inches='tight')
        plt.close('all')

