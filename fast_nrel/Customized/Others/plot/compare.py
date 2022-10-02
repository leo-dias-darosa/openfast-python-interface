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

    fast_standard = open(path_fast+turbinefast).read().splitlines()
    turbinefast = turbinefast[0:len(turbinefast)-4]
    out = turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s.sfunc.out'
    
    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s'+'/Individual pitch controller')==False:
        print('Run your turbine with '+str(v)+'m/s wind speed '+str(h)+'hub heigh '+str(t)+'% turbulence intensity with '+str(s)+' seconds of duration first')
    else:
        new_path_IPC = path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s'+'/Individual pitch controller/'

    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s'+'/Collective pitch controller')==False:
        print('Run your turbine with '+str(v)+'m/s wind speed '+str(h)+'hub heigh '+str(t)+'% turbulence intensity with '+str(s)+' seconds of duration first')
    else:
        new_path_col = path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s'+'/Collective pitch controller/'    

    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s'+'/Comparison')==False:
        os.mkdir(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s'+'/Comparison')

    path_comparison = path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s'+'/Comparison/'

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

    dataIndex = pd.read_excel(out_noHeader_IPC+'.xls')
    data_IPC = pd.read_excel(out_noHeader_IPC+'.xls',header=None)
    data_col = pd.read_excel(out_noHeader_col+'.xls',header=None)

    TimeIndex = dataIndex.columns.get_loc('Time')
    Time = data_IPC.iloc[2:,TimeIndex]
    Time = [float(x) for x in Time]
    
#%%%%%%%%%%%%#
    
    BladeRootFlapWiseM1Index = dataIndex.columns.get_loc("RootMxb1")
    BladeRootFlapWiseM1IPC = data_IPC.iloc[2:,BladeRootFlapWiseM1Index]
    BladeRootFlapWiseM1IPC = [float(x) for x in BladeRootFlapWiseM1IPC]

    BladeRootFlapWiseM2Index = dataIndex.columns.get_loc("RootMxb2")
    BladeRootFlapWiseM2IPC = data_IPC.iloc[2:,BladeRootFlapWiseM2Index]
    BladeRootFlapWiseM2IPC = [float(x) for x in BladeRootFlapWiseM2IPC]

    BladeRootFlapWiseM3Index = dataIndex.columns.get_loc("RootMxb3")
    BladeRootFlapWiseM3IPC = data_IPC.iloc[2:,BladeRootFlapWiseM3Index]
    BladeRootFlapWiseM3IPC = [float(x) for x in BladeRootFlapWiseM3IPC]

    BladeRootFlapWiseM1COL = data_col.iloc[2:,BladeRootFlapWiseM1Index]
    BladeRootFlapWiseM1COL = [float(x) for x in BladeRootFlapWiseM1IPC]
    
    BladeRootFlapWiseM2COL = data_col.iloc[2:,BladeRootFlapWiseM2Index]
    BladeRootFlapWiseM2COL = [float(x) for x in BladeRootFlapWiseM2COL]

    BladeRootFlapWiseM3COL = data_col.iloc[2:,BladeRootFlapWiseM3Index]
    BladeRootFlapWiseM3COL = [float(x) for x in BladeRootFlapWiseM3COL]
    
    plt.figure()
    plt.subplot(3,1,1)
    plt.plot(Time,BladeRootFlapWiseM1COL,label = 'Collective Pitch Controller')
    plt.plot(Time,BladeRootFlapWiseM1IPC,label = 'Individual Pitch Controller')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.title('Blade Root Flapwise Moments\nBlade 1')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,2)
    plt.plot(Time,BladeRootFlapWiseM2COL,label = 'Collective Pitch Controller')
    plt.plot(Time,BladeRootFlapWiseM2IPC,label = 'Individual Pitch Controller')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.title('Blade 2')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,3)
    plt.plot(Time,BladeRootFlapWiseM3COL,label = 'Collective Pitch Controller')
    plt.plot(Time,BladeRootFlapWiseM3IPC,label = 'Individual Pitch Controller')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.title('Blade 3')
    plt.ylabel('kN.m')
    plt.box(on=None)
    plt.tight_layout()
    
    plt.savefig(path_comparison+'/BladeRootFlapMoments.png',bbox_inches='tight')
    plt.close('all')
    
#%%%%%%%%%%%%#
    
    BladeRootEdgeWiseM1Index = dataIndex.columns.get_loc("RootMyb1")
    BladeRootEdgeWiseM1IPC = data_IPC.iloc[2:,BladeRootEdgeWiseM1Index]
    BladeRootEdgeWiseM1IPC = [float(x) for x in BladeRootEdgeWiseM1IPC]

    BladeRootEdgeWiseM2Index = dataIndex.columns.get_loc("RootMyb2")
    BladeRootEdgeWiseM2IPC = data_IPC.iloc[2:,BladeRootEdgeWiseM2Index]
    BladeRootEdgeWiseM2IPC = [float(x) for x in BladeRootEdgeWiseM2IPC]

    BladeRootEdgeWiseM3Index = dataIndex.columns.get_loc("RootMyb3")
    BladeRootEdgeWiseM3IPC = data_IPC.iloc[2:,BladeRootEdgeWiseM3Index]
    BladeRootEdgeWiseM3IPC = [float(x) for x in BladeRootEdgeWiseM3IPC]

    BladeRootEdgeWiseM1COL = data_col.iloc[2:,BladeRootEdgeWiseM1Index]
    BladeRootEdgeWiseM1COL = [float(x) for x in BladeRootEdgeWiseM1COL]

    BladeRootEdgeWiseM2COL = data_col.iloc[2:,BladeRootEdgeWiseM2Index]
    BladeRootEdgeWiseM2COL = [float(x) for x in BladeRootEdgeWiseM2COL]

    BladeRootEdgeWiseM3COL = data_col.iloc[2:,BladeRootEdgeWiseM3Index]
    BladeRootEdgeWiseM3COL = [float(x) for x in BladeRootEdgeWiseM3COL]
    
    plt.figure()
    plt.subplot(3,1,1)
    plt.plot(Time,BladeRootEdgeWiseM1COL,label = 'Collective Pitch Controller')
    plt.plot(Time,BladeRootEdgeWiseM1IPC,label = 'Individual Pitch Controller')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.title('Blade Root Edgwise Moments\nBlade 1')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,2)
    plt.plot(Time,BladeRootEdgeWiseM2COL,label = 'Collective Pitch Controller')
    plt.plot(Time,BladeRootEdgeWiseM2IPC,label = 'Individual Pitch Controller')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.title('Blade 2')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,3)
    plt.plot(Time,BladeRootEdgeWiseM3COL,label = 'Collective Pitch Controller')
    plt.plot(Time,BladeRootEdgeWiseM3IPC,label = 'Individual Pitch Controller')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.title('Blade 3')
    plt.ylabel('kN.m')
    plt.box(on=None)
    plt.tight_layout()
    
    plt.savefig(path_comparison+'/BladeRootEdgeMoments.png',bbox_inches='tight')
    plt.close('all')

#%%%%%%%%%%%%#

    RotorTiltMomentIndex = dataIndex.columns.get_loc("YawBrMxn")
    RotorTiltMomentIPC = data_IPC.iloc[2:,RotorTiltMomentIndex]
    RotorTiltMomentIPC = [float(x) for x in RotorTiltMomentIPC]
    RotorTiltMomentCOL = data_col.iloc[2:,RotorTiltMomentIndex]
    RotorTiltMomentCOL = [float(x) for x in RotorTiltMomentCOL]

    RotorYawMomentIndex = dataIndex.columns.get_loc("YawBrMzn")
    RotorYawMomentIPC = data_IPC.iloc[2:,RotorYawMomentIndex]
    RotorYawMomentIPC = [float(x) for x in RotorYawMomentIPC]
    RotorYawMomentCOL = data_col.iloc[2:,RotorYawMomentIndex]
    RotorYawMomentCOL = [float(x) for x in RotorYawMomentCOL]

    RotorTorqueIndex = dataIndex.columns.get_loc("LSShftMxa")
    RotorTorqueIPC = data_IPC.iloc[2:,RotorTorqueIndex]
    RotorTorqueIPC = [float(x) for x in RotorTorqueIPC]
    RotorTorqueCOL = data_col.iloc[2:,RotorTorqueIndex]
    RotorTorqueCOL = [float(x) for x in RotorTorqueCOL]

    plt.figure()
    plt.subplot(3,1,1)
    plt.plot(Time,RotorTiltMomentCOL,label = 'Collective Pitch Controller')
    plt.plot(Time,RotorTiltMomentIPC,label = 'Individual Pitch Controller')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.title('Rotor Quantities\nTilt Moment')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,2)
    plt.plot(Time,RotorYawMomentCOL,label = 'Collective Pitch Controller')
    plt.plot(Time,RotorYawMomentIPC,label = 'Individual Pitch Controller')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.title('Yaw Moment')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,3)
    plt.plot(Time,RotorTorqueCOL,label = 'Collective Pitch Controller')
    plt.plot(Time,RotorTorqueIPC,label = 'Individual Pitch Controller')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.title('Rotor Torque')
    plt.ylabel('kN.m')
    plt.box(on=None)
    plt.tight_layout()
    
    plt.savefig(path_comparison+'/RotorQuantities.png',bbox_inches='tight')
    plt.close('all')

#%%%%%%%%%%%%#

    TowerBaseNormalIndex = dataIndex.columns.get_loc("YawBrMxn")
    TowerBaseNormalIPC = data_IPC.iloc[2:,TowerBaseNormalIndex]
    TowerBaseNormalIPC = [float(x) for x in TowerBaseNormalIPC]
    TowerBaseNormalCOL = data_col.iloc[2:,TowerBaseNormalIndex]
    TowerBaseNormalCOL = [float(x) for x in TowerBaseNormalCOL]

    TowerBaseLateralIndex = dataIndex.columns.get_loc("YawBrMzn")
    TowerBaseLateralIPC = data_IPC.iloc[2:,TowerBaseLateralIndex]
    TowerBaseLateralIPC = [float(x) for x in TowerBaseLateralIPC]
    TowerBaseLateralCOL = data_col.iloc[2:,TowerBaseLateralIndex]
    TowerBaseLateralCOL = [float(x) for x in TowerBaseLateralCOL]

    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(Time,TowerBaseNormalCOL,label = 'Collective Pitch Controller')
    plt.plot(Time,TowerBaseNormalIPC,label = 'Individual Pitch Controller')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.title('Tower Base Moments\nNormal')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(2,1,2)
    plt.plot(Time,TowerBaseLateralCOL,label = 'Collective Pitch Controller')
    plt.plot(Time,TowerBaseLateralIPC,label = 'Individual Pitch Controller')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.title('Lateral')
    plt.ylabel('kN.m')
    plt.box(on=None)
    plt.tight_layout()

    plt.savefig(path_comparison+'/TowerBaseMoments.png',bbox_inches='tight')
    plt.close('all')
    print('Check at "'+path_comparison+'" folder')

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

    fast_standard = open(path_fast+turbinefast).read().splitlines()
    turbinefast = turbinefast[0:len(turbinefast)-4]
    out = turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s.sfunc.out'
    
    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s'+'/Individual pitch controller')==False:
        print('Run your turbine with '+str(v)+'m/s wind speed '+str(h)+'hub heigh '+str(t)+'% turbulence intensity with '+str(s)+' seconds of duration first')
    else:
        new_path_IPC = path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s'+'/Individual pitch controller/'

    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s'+'/Collective pitch controller')==False:
        print('Run your turbine with '+str(v)+'m/s wind speed '+str(h)+'hub heigh '+str(t)+'% turbulence intensity with '+str(s)+' seconds of duration first')
    else:
        new_path_col = path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s'+'/Collective pitch controller/'    

    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s'+'/Comparison')==False:
        os.mkdir(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s'+'/Comparison')

    path_comparison = path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s'+'/Comparison/'
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

