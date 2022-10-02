# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 17:31:04 2018

@author: Leonardo
"""

import pandas as pd
import matplotlib.pyplot as plt
import xlwt
import os

def IEC_outputs(parameters):
    
    path_modules = parameters[0]
    path_fast = parameters[1]
    turbinefast=parameters[2]
    path_turbsim = parameters[3]
    turbsim = parameters[4]
    v = parameters[5]
    h = parameters[6]
    t = parameters[7]
    s = parameters[8]
    frequency = parameters[9]
    e=parameters[10]

    fast_standard = open(path_fast+turbinefast).read().splitlines()
    turbinefast = turbinefast[0:len(turbinefast)-4]
    out = turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s'+str(e)+'massfault.sfunc.out'
    
    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'massfault'+'/Collective pitch controller')==False:
        print('Run your turbine with '+str(v)+'m/s wind speed '+str(h)+'hub heigh '+str(t)+'% turbulence intensity with '+str(s)+' seconds of duration first')
    else:
        new_path_col= path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'massfault'+'/Collective pitch controller/'

    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'massfault'+'/Individual pitch controller')==False:
        print('Run your turbine with '+str(v)+'m/s wind speed '+str(h)+'hub heigh '+str(t)+'% turbulence intensity with '+str(s)+' seconds of duration first')
    else:
        new_path_IPC = path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'massfault'+'/Individual pitch controller/'   

    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'massfault'+'/Comparison')==False:
        os.mkdir(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'massfault'+'/Comparison')

    path_comparison = path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'massfault'+'/Comparison/'
    standard_out_col= open(new_path_col+out).read().splitlines()
    standard_out_IPC = open(new_path_IPC+out).read().splitlines()
    out = out[0:len(out)-4]


    ## CREATE NEW OUT IPC
    
    out_noHeader_IPC = open(path_comparison+output+'IPCnoHeader.out','w')
                            
    i = 0
    for linha in standard_out_IPC:
        if i >6:
            out_noHeader_IPC.write(linha+'\n')
        else:
            i=i+1
            
    out_noHeader_IPC = path_comparison+output+'IPCnoHeader.out'

    f = open(out_noHeader_IPC, 'r+')                  
    row_list = []
    
    for row in f:
        row_list.append(row.split())
    column_list = zip(*row_list)
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Sheet1')
    i = 0
    for column in column_list:
        for item in range(len(column)):
            worksheet.write(item, i, column[item])
        workbook.save(out_noHeader_IPC+'.xls')
        i+=1

    ## CREATE NEW OUT COLLECTIVE
        
    out_noHeader_col = open(path_comparison+output+'CollectivenoHeader.out','w')
                            
    i = 0
    for linha in standard_out_col:
        if i >6:
            out_noHeader_col.write(linha+'\n')
        else:
            i=i+1
            
    out_noHeader_col = path_comparison+output+'CollectivenoHeader.out'

    f = open(out_noHeader_col, 'r+')                  
    row_list = []
    
    for row in f:
        row_list.append(row.split())
    column_list = zip(*row_list)
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Sheet1')
    i = 0
    for column in column_list:
        for item in range(len(column)):
            worksheet.write(item, i, column[item])
        workbook.save(out_noHeader_col+'.xls')
        i+=1

    ## Get data
        
    data_IPC = pd.read_excel(out_noHeader_IPC+'.xls')
    data_col = pd.read_excel(out_noHeader_col+'.xls')

    ## DATA IPC
    FlapwiseBlade1RootMIPC = data_IPC.iloc[2:,4]
    FlapwiseBlade2RootMIPC = data_IPC.iloc[2:,6]
    FlapwiseBlade3RootMIPC = data_IPC.iloc[2:,8]
    
    EdgewiseBlade1RootMIPC = data_IPC.iloc[2:,5]
    EdgewiseBlade2RootMIPC = data_IPC.iloc[2:,7]
    EdgewiseBlade3RootMIPC = data_IPC.iloc[2:,9]
    
    RotorTiltIPC = data_IPC.iloc[2:,10]
    RotorYawIPC = data_IPC.iloc[2:,11]
    RotorTorqueIPC = data_IPC.iloc[2:,12]
    
    PitchLoadR1IPC = data_IPC.iloc[2:,13]
    PitchLoadR2IPC = data_IPC.iloc[2:,14]
    PitchLoadR3IPC = data_IPC.iloc[2:,15]
    
    PitchLoadM1IPC = data_IPC.iloc[2:,16]
    PitchLoadM2IPC = data_IPC.iloc[2:,17]
    PitchLoadM3IPC = data_IPC.iloc[2:,18]
    
    TowerTopAccNormalIPC = data_IPC.iloc[2:,19]
    TowerTopAccLatIPC = data_IPC.iloc[2:,20]
    
    TowerMidMoNormalIPC = data_IPC.iloc[2:,21]
    TowerMidMoLatIPC = data_IPC.iloc[2:,22]
    
    TowerTopMoNormalIPC = data_IPC.iloc[2:,23]
    TowerTopMoLatIPC = data_IPC.iloc[2:,24]
    
    PowerIPC = data_IPC.iloc[2:,25]
    RotorSpeedIPC = data_IPC.iloc[2:,26]
    GeneratorSpeedIPC = data_IPC.iloc[2:,27]
    AzimuthIPC = data_IPC.iloc[2:,28]
    
    Pitch1IPC = data_IPC.iloc[2:,29]
    Pitch2IPC = data_IPC.iloc[2:,30]
    Pitch3IPC = data_IPC.iloc[2:,31]

    ## DATA COLLECTIVE
    
    FlapwiseBlade1RootMCOL = data_col.iloc[2:,4]
    FlapwiseBlade2RootMCOL = data_col.iloc[2:,6]
    FlapwiseBlade3RootMCOL = data_col.iloc[2:,8]
    
    EdgewiseBlade1RootMCOL = data_col.iloc[2:,5]
    EdgewiseBlade2RootMCOL = data_col.iloc[2:,7]
    EdgewiseBlade3RootMCOL = data_col.iloc[2:,9]
    
    RotorTiltCOL = data_col.iloc[2:,10]
    RotorYawCOL = data_col.iloc[2:,11]
    RotorTorqueCOL = data_col.iloc[2:,12]
    
    PitchLoadR1COL = data_col.iloc[2:,13]
    PitchLoadR2COL = data_col.iloc[2:,14]
    PitchLoadR3COL = data_col.iloc[2:,15]
    
    PitchLoadM1COL = data_col.iloc[2:,16]
    PitchLoadM2COL = data_col.iloc[2:,17]
    PitchLoadM3COL = data_col.iloc[2:,18]
    
    TowerTopAccNormalCOL = data_col.iloc[2:,19]
    TowerTopAccLatCOL = data_col.iloc[2:,20]
    
    TowerMidMoNormalCOL = data_col.iloc[2:,21]
    TowerMidMoLatCOL = data_col.iloc[2:,22]
    
    TowerTopMoNormalCOL = data_col.iloc[2:,23]
    TowerTopMoLatCOL = data_col.iloc[2:,24]
    
    PowerCOL = data_col.iloc[2:,25]
    RotorSpeedCOL = data_col.iloc[2:,26]
    GeneratorSpeedCOL = data_col.iloc[2:,27]
    AzimuthCOL = data_col.iloc[2:,28]
    
    Pitch1COL = data_col.iloc[2:,29]
    Pitch2COL = data_col.iloc[2:,30]
    Pitch3COL= data_col.iloc[2:,31]
             
############################################################################################################################################################################################
############################################################################################################################################################################################
    
def User_outputs(parameters):
    
    path_modules = parameters[0]
    path_fast = parameters[1]
    turbinefast=parameters[2]
    path_turbsim = parameters[3]
    turbsim = parameters[4]
    v = parameters[5]
    h = parameters[6]
    t = parameters[7]
    s = parameters[8]
    frequency = parameters[9]
    e=parameters[10]

    fast_standard = open(path_fast+turbinefast).read().splitlines()
    turbinefast = turbinefast[0:len(turbinefast)-4]
    out = turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s'+str(e)+'massfault.sfunc.out'
    
    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'massfault'+'/Collective pitch controller')==False:
        print('Run your turbine with '+str(v)+'m/s wind speed '+str(h)+'hub heigh '+str(t)+'% turbulence intensity with '+str(s)+' seconds of duration first')
    else:
        new_path_col= path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'massfault'+'/Collective pitch controller/'

    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'massfault'+'/Individual pitch controller')==False:
        print('Run your turbine with '+str(v)+'m/s wind speed '+str(h)+'hub heigh '+str(t)+'% turbulence intensity with '+str(s)+' seconds of duration first')
    else:
        new_path_IPC = path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'massfault'+'/Individual pitch controller/'   

    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'massfault'+'/Comparison')==False:
        os.mkdir(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'massfault'+'/Comparison')

    path_comparison = path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'massfault'+'/Comparison/'
    standard_out_col= open(new_path_col+out).read().splitlines()
    standard_out_IPC = open(new_path_IPC+out).read().splitlines()
    out = out[0:len(out)-4]


    ## CREATE NEW OUT IPC
    
    out_noHeader_IPC = open(path_comparison+out+'IPCnoHeader.out','w')
                            
    i = 0
    for linha in standard_out_IPC:
        if i >5:
            out_noHeader_IPC.write(linha+'\n')
        else:
            i=i+1
            
    out_noHeader_IPC = path_comparison+out+'IPCnoHeader.out'

    f = open(out_noHeader_IPC, 'r+')                  
    row_list = []
    
    for row in f:
        row_list.append(row.split())
    column_list = zip(*row_list)
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Sheet1')
    i = 0
    for column in column_list:
        for item in range(len(column)):
            worksheet.write(item, i, column[item])
        workbook.save(out_noHeader_IPC+'.xls')
        i+=1

    ## CREATE NEW OUT COLLECTIVE
        
    out_noHeader_col = open(path_comparison+out+'CollectivenoHeader.out','w')
                            
    i = 0
    for linha in standard_out_col:
        if i >5:
            out_noHeader_col.write(linha+'\n')
        else:
            i=i+1
            
    out_noHeader_col = path_comparison+out+'CollectivenoHeader.out'

    f = open(out_noHeader_col, 'r+')                  
    row_list = []
    
    for row in f:
        row_list.append(row.split())
    column_list = zip(*row_list)
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Sheet1')
    i = 0
    for column in column_list:
        for item in range(len(column)):
            worksheet.write(item, i, column[item])
        workbook.save(out_noHeader_col+'.xls')
        i+=1

    ## Get data
        
    data_IPC = pd.read_excel(out_noHeader_IPC+'.xls',header=None)
    data_col = pd.read_excel(out_noHeader_col+'.xls',header=None)

    output = data_IPC.iloc[0,0:]
    output = [str(x) for x in output]
    legend = data_IPC.iloc[1,0:]
    legend = [str(x) for x in legend]
       
    Time = data_IPC.iloc[2:,0]
    Time = [float(x) for x in Time]

#### Get outlist IPC
    
    fig_IPC=[]
    
    for i in range(1,len(data_IPC.columns)):
        series =data_IPC.iloc[2:,i]
        fig_IPC.append(series)
    for i in range(len(fig_IPC)):
        fig_IPC[i]=[float(x) for x in fig_IPC[i]]
    
    for i in range(len(legend)):
        legend[i] = legend[i][1:len(legend[i])-1]

#### Get outlist collective
        
    fig_col=[]
    
    for i in range(1,len(data_col.columns)):
        series =data_col.iloc[2:,i]
        fig_col.append(series)
    for i in range(len(fig_col)):
        fig_col[i]=[float(x) for x in fig_col[i]]
            
    for i in range(len(fig_IPC)):
        plt.close('all')
        plt.figure()
        plt.plot(Time,fig_IPC[i],label = 'IPC')
        plt.plot(Time,fig_col[i],label='Collective')
        plt.title(output[i+1])
        plt.ylabel(legend[i+1])
        plt.xlabel('Time')
        plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
        plt.box(on=None)
        plt.savefig(path_comparison+output[i+1]+'.png',bbox_inches='tight')
        plt.close('all')

