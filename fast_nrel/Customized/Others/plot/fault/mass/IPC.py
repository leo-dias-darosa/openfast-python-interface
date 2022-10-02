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
    n=parameters[13]

    fast_standard = open(path_fast+turbinefast).read().splitlines()
    turbinefast = turbinefast[0:len(turbinefast)-4]
    out_fault = turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(e)+'massfault-'+str(n)+'.sfunc.out'
    out =turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'.sfunc.out'

    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(e)+'massfault-'+str(n)+'/Individual pitch controller')==False:
        print('Run your turbine with '+str(v)+'m/s wind speed '+str(h)+'hub heigh '+str(t)+'% turbulence intensity with '+str(s)+' seconds of duration first')
    else:
        fault_IPC= path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(e)+'massfault-'+str(n)+'/Individual pitch controller/'
   
    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 Outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/Collective pitch controller')==False:
        print('Run your turbine with '+str(v)+'m/s wind speed '+str(h)+'hub heigh '+str(t)+'% turbulence intensity with '+str(s)+' seconds of duration first')
    else:
        normal_IPC= path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 Outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/Collective pitch controller/'
        
    if os.path.exists(fault_IPC+'Output Data')==False:
        os.mkdir(fault_IPC+'Output Data')

    output_data = fault_IPC+'Output Data/'

    standard_normal_IPC=open(normal_IPC+out).read().splitlines()
    standard_fault_IPC= open(fault_IPC+out_fault).read().splitlines()

    out = out[0:len(out)-4]
    out_fault = out_fault[0:len(out)-4]


    ## NEW OUT IPC NORMAL

    normal_noHeader_IPC = open(output_data+str(v)+'ms-'+str(t)+'ti-'+'NormalnoHeader.out','w')
                            
    i = 0
    for linha in standard_normal_IPC:
        if i >5:
            normal_noHeader_IPC.write(linha+'\n')
        else:
            i=i+1
    normal_noHeader_IPC.close()
    
    normal_noHeader_IPC = output_data+str(v)+'ms-'+str(t)+'ti-'+'NormalnoHeader.out'
    f = open(normal_noHeader_IPC, 'r+')                  
    row_list = []
    normal_noHeader_IPC = normal_noHeader_IPC[0:len(normal_noHeader_IPC)-4]
    for row in f:
        row_list.append(row.split())
    column_list = zip(*row_list)
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Sheet1')
    i = 0
    for column in column_list:
        for item in range(len(column)):
            worksheet.write(item, i, column[item])
        workbook.save(normal_noHeader_IPC+'.xls')
        i+=1

    ## NEW OUT IPC FAULT

    fault_noHeader_IPC = open(output_data+str(v)+'ms-'+str(t)+'ti-'+str(e)+'MassFaultnoHeader.out','w')
                            
    i = 0
    for linha in standard_fault_IPC:
        if i >5:
            fault_noHeader_IPC.write(linha+'\n')
        else:
            i=i+1
    fault_noHeader_IPC.close()
    
    fault_noHeader_IPC = output_data+str(v)+'ms-'+str(t)+'ti-'+str(e)+'MassFaultnoHeader.out'
    
    f = open(fault_noHeader_IPC, 'r+')                  
    row_list = []
    fault_noHeader_IPC = fault_noHeader_IPC[0:len(fault_noHeader_IPC)-4]
    for row in f:
        row_list.append(row.split())
    column_list = zip(*row_list)
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Sheet1')
    i = 0
    for column in column_list:
        for item in range(len(column)):
            worksheet.write(item, i, column[item])
        workbook.save(fault_noHeader_IPC+'.xls')
        i+=1

    ## Get data

    dataIndex = pd.read_excel(normal_noHeader_IPC+'.xls')
    data_normal_IPC = pd.read_excel(normal_noHeader_IPC+'.xls',header=None)
    data_fault_IPC= pd.read_excel(fault_noHeader_IPC+'.xls',header=None)
    
    TimeIndex = dataIndex.columns.get_loc('Time')
    Time = data_normal_IPC.iloc[2:,TimeIndex]
    Time = [float(x) for x in Time]

    legend_positionX=0.85
    legend_positionY=1

#%%%%%%%%%%%%#
    
    BladeRootFlapWiseM1Index = dataIndex.columns.get_loc("RootMxb1")
    BladeRootFlapWiseM1Normal = data_normal_IPC.iloc[2:,BladeRootFlapWiseM1Index]
    BladeRootFlapWiseM1Normal = [float(x) for x in BladeRootFlapWiseM1Normal]
    BladeRootFlapWiseM1Fault = data_fault_IPC.iloc[2:,BladeRootFlapWiseM1Index]
    BladeRootFlapWiseM1Fault = [float(x) for x in BladeRootFlapWiseM1Fault]

    BladeRootFlapWiseM2Index = dataIndex.columns.get_loc("RootMxb2")
    BladeRootFlapWiseM2Normal = data_normal_IPC.iloc[2:,BladeRootFlapWiseM2Index]
    BladeRootFlapWiseM2Normal = [float(x) for x in BladeRootFlapWiseM2Normal]
    BladeRootFlapWiseM2Fault = data_fault_IPC.iloc[2:,BladeRootFlapWiseM2Index]
    BladeRootFlapWiseM2Fault = [float(x) for x in BladeRootFlapWiseM2Fault]

    BladeRootFlapWiseM3Index = dataIndex.columns.get_loc("RootMxb3")
    BladeRootFlapWiseM3Normal = data_normal_IPC.iloc[2:,BladeRootFlapWiseM3Index]
    BladeRootFlapWiseM3Normal = [float(x) for x in BladeRootFlapWiseM3Normal]
    BladeRootFlapWiseM3Fault = data_fault_IPC.iloc[2:,BladeRootFlapWiseM3Index]
    BladeRootFlapWiseM3Fault = [float(x) for x in BladeRootFlapWiseM3Fault]
   
    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(16,8)
    plt.subplot(3,1,1)
    plt.plot(Time,BladeRootFlapWiseM1Normal,label = 'Normal operation')
    plt.plot(Time,BladeRootFlapWiseM1Fault,label='Blade mass fault operation')
    plt.title('Blade Root Flapwise Moments \n Blade 1')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,2)
    plt.plot(Time,BladeRootFlapWiseM2Normal,label = 'Normal operation')
    plt.plot(Time,BladeRootFlapWiseM2Fault,label='Blade mass fault operation')
    plt.title('Blade 2')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()
    
    plt.subplot(3,1,3)
    plt.plot(Time,BladeRootFlapWiseM3Normal,label = 'Normal operation')
    plt.plot(Time,BladeRootFlapWiseM3Fault,label='Blade mass fault operation')
    plt.title('Blade 3')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.box(on=None)
    plt.tight_layout()
    
    plt.savefig(output_data+'/BladeRootFlapMoments.png',dpi = 200)
    plt.close('all')
    
#%%%%%%%%%%%%#

    BladeRootEdgeWiseM1Index = dataIndex.columns.get_loc("RootMyb1")
    BladeRootEdgeWiseM1Normal = data_normal_IPC.iloc[2:,BladeRootEdgeWiseM1Index]
    BladeRootEdgeWiseM1Normal = [float(x) for x in BladeRootEdgeWiseM1Normal]
    BladeRootEdgeWiseM1Fault = data_fault_IPC.iloc[2:,BladeRootEdgeWiseM1Index]
    BladeRootEdgeWiseM1Fault = [float(x) for x in BladeRootEdgeWiseM1Fault]

    BladeRootEdgeWiseM2Index = dataIndex.columns.get_loc("RootMyb2")
    BladeRootEdgeWiseM2Normal = data_normal_IPC.iloc[2:,BladeRootEdgeWiseM2Index]
    BladeRootEdgeWiseM2Normal = [float(x) for x in BladeRootEdgeWiseM2Normal]
    BladeRootEdgeWiseM2Fault = data_fault_IPC.iloc[2:,BladeRootEdgeWiseM2Index]
    BladeRootEdgeWiseM2Fault = [float(x) for x in BladeRootEdgeWiseM2Fault]

    BladeRootEdgeWiseM3Index = dataIndex.columns.get_loc("RootMyb3")
    BladeRootEdgeWiseM3Normal = data_normal_IPC.iloc[2:,BladeRootEdgeWiseM3Index]
    BladeRootEdgeWiseM3Normal = [float(x) for x in BladeRootEdgeWiseM3Normal]
    BladeRootEdgeWiseM3Fault = data_fault_IPC.iloc[2:,BladeRootEdgeWiseM3Index]
    BladeRootEdgeWiseM3Fault = [float(x) for x in BladeRootEdgeWiseM3Fault]

    
    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(16,8)
    plt.subplot(3,1,1)
    plt.plot(Time,BladeRootEdgeWiseM1Normal,label = 'Normal operation')
    plt.plot(Time,BladeRootEdgeWiseM1Fault,label='Blade mass fault operation')
    plt.title('Blade Root Edgewise Moments \n Blade 1')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,2)
    plt.plot(Time,BladeRootEdgeWiseM2Normal,label = 'Normal operation')
    plt.plot(Time,BladeRootEdgeWiseM2Fault,label='Blade mass fault operation')
    plt.title('Blade 2')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,3)
    plt.plot(Time,BladeRootEdgeWiseM3Normal,label = 'Normal operation')
    plt.plot(Time,BladeRootEdgeWiseM3Fault,label='Blade mass fault operation')
    plt.title('Blade 3')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.box(on=None)
    plt.tight_layout()
    
    plt.savefig(output_data+'/BladeRootEdgeMoments.png',dpi = 200)
    plt.close('all')
    
#%%%%%%%%%%%%#

    RotorTiltMomentIndex = dataIndex.columns.get_loc("YawBrMxn")
    RotorTiltMomentNormal = data_normal_IPC.iloc[2:,RotorTiltMomentIndex]
    RotorTiltMomentNormal = [float(x) for x in RotorTiltMomentNormal]
    RotorTiltMomentFault = data_fault_IPC.iloc[2:,RotorTiltMomentIndex]
    RotorTiltMomentFault = [float(x) for x in RotorTiltMomentFault]

    RotorYawMomentIndex = dataIndex.columns.get_loc("YawBrMzn")
    RotorYawMomentNormal = data_normal_IPC.iloc[2:,RotorYawMomentIndex]
    RotorYawMomentNormal = [float(x) for x in RotorYawMomentNormal]
    RotorYawMomentFault = data_fault_IPC.iloc[2:,RotorYawMomentIndex]
    RotorYawMomentFault = [float(x) for x in RotorYawMomentFault]

    RotorTorqueIndex = dataIndex.columns.get_loc("LSShftMxa")
    RotorTorqueNormal = data_normal_IPC.iloc[2:,RotorTorqueIndex]
    RotorTorqueNormal = [float(x) for x in RotorTorqueNormal]
    RotorTorqueFault = data_fault_IPC.iloc[2:,RotorTorqueIndex]
    RotorTorqueFault = [float(x) for x in RotorTorqueFault]

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(16,8)
    plt.subplot(3,1,1)
    plt.plot(Time,RotorTiltMomentNormal,label = 'Normal operation')
    plt.plot(Time,RotorTiltMomentFault,label='Blade mass fault operation')
    plt.title('Rotor Quantities \n Tilt Moment')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,2)
    plt.plot(Time,RotorYawMomentNormal,label = 'Normal operation')
    plt.plot(Time,RotorYawMomentFault,label='Blade mass fault operation')
    plt.title('Yaw Moment')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,3)
    plt.plot(Time,RotorTorqueNormal,label = 'Normal operation')
    plt.plot(Time,RotorTorqueFault,label='Blade mass fault operation')
    plt.title('Rotor Torque')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.box(on=None)
    plt.tight_layout()
    
    plt.savefig(output_data+'/RotorQuantities.png',dpi = 200)
    plt.close('all')

#%%%%%%%%%%%%#

    TowerBaseNormalIndex = dataIndex.columns.get_loc("TwrBsMyt")
    TowerBaseNormalNormal = data_normal_IPC.iloc[2:,TowerBaseNormalIndex]
    TowerBaseNormalNormal = [float(x) for x in TowerBaseNormalNormal]
    TowerBaseNormalFault = data_fault_IPC.iloc[2:,TowerBaseNormalIndex]
    TowerBaseNormalFault = [float(x) for x in TowerBaseNormalFault]

    TowerBaseLateralIndex = dataIndex.columns.get_loc("TwrBsMxt")
    TowerBaseLateralNormal = data_normal_IPC.iloc[2:,TowerBaseLateralIndex]
    TowerBaseLateralNormal = [float(x) for x in TowerBaseLateralNormal]
    TowerBaseLateralFault = data_fault_IPC.iloc[2:,TowerBaseLateralIndex]
    TowerBaseLateralFault = [float(x) for x in TowerBaseLateralFault]

    TowerTorqueIndex = dataIndex.columns.get_loc("TwrBsMxt")
    TowerTorqueNormal = data_normal_IPC.iloc[2:,TowerTorqueIndex]
    TowerTorqueNormal = [float(x) for x in TowerTorqueNormal]
    TowerTorqueFault = data_fault_IPC.iloc[2:,TowerTorqueIndex]
    TowerTorqueFault = [float(x) for x in TowerTorqueFault]

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(16,8)
    plt.subplot(3,1,1)
    plt.plot(Time,TowerBaseNormalNormal,label='Normal operation')
    plt.plot(Time,TowerBaseNormalFault,label='Blade mass fault operation')
    plt.title('Tower Moments \n Base Normal')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,2)
    plt.plot(Time,TowerBaseLateralNormal,label='Normal operation')
    plt.plot(Time,TowerBaseLateralFault,label='Blade mass fault operation')
    plt.title('Base Lateral')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,3)
    plt.plot(Time,TowerTorqueNormal,label = 'Normal operation')
    plt.plot(Time,TowerTorqueFault,label='Blade mass fault operation')
    plt.title('Torque')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.box(on=None)
    plt.tight_layout()

    plt.savefig(output_data+'/TowerMoments.png',dpi = 200)
    plt.close('all')

#%%%%%%%%%%%%#

    PitchActuationoLoad1Index = dataIndex.columns.get_loc("RootMzc1")
    PitchActuationoLoad1Normal = data_normal_IPC.iloc[2:,PitchActuationoLoad1Index]
    PitchActuationoLoad1Normal = [float(x) for x in PitchActuationoLoad1Normal]
    PitchActuationoLoad1Fault = data_fault_IPC.iloc[2:,PitchActuationoLoad1Index]
    PitchActuationoLoad1Fault = [float(x) for x in PitchActuationoLoad1Fault]

    PitchActuationoLoad2Index = dataIndex.columns.get_loc("RootMzc2")
    PitchActuationoLoad2Normal = data_normal_IPC.iloc[2:,PitchActuationoLoad2Index]
    PitchActuationoLoad2Normal = [float(x) for x in PitchActuationoLoad2Normal]
    PitchActuationoLoad2Fault = data_fault_IPC.iloc[2:,PitchActuationoLoad2Index]
    PitchActuationoLoad2Fault = [float(x) for x in PitchActuationoLoad2Fault]

    PitchActuationoLoad3Index = dataIndex.columns.get_loc("RootMzc3")
    PitchActuationoLoad3Normal = data_normal_IPC.iloc[2:,PitchActuationoLoad3Index]
    PitchActuationoLoad3Normal = [float(x) for x in PitchActuationoLoad3Normal]
    PitchActuationoLoad3Fault = data_fault_IPC.iloc[2:,PitchActuationoLoad3Index]
    PitchActuationoLoad3Fault = [float(x) for x in PitchActuationoLoad3Fault]

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(16,8)
    plt.subplot(3,1,1)
    plt.plot(Time,PitchActuationoLoad1Normal,label='Normal operation')
    plt.plot(Time,PitchActuationoLoad1Fault,label='Blade mass fault operation')
    plt.title('Pitch actuation loads \n Blade 1')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,2)
    plt.plot(Time,PitchActuationoLoad2Normal,label='Normal operation')
    plt.plot(Time,PitchActuationoLoad2Fault,label='Blade mass fault operation')
    plt.title('Blade 2')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,3)
    plt.plot(Time,PitchActuationoLoad3Normal,label='Normal operation')
    plt.plot(Time,PitchActuationoLoad3Fault,label='Blade mass fault operation')
    plt.title(' Blade 3')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.box(on=None)
    plt.tight_layout()

    plt.savefig(output_data+'/PitchActuationLoads.png',dpi = 200)
    plt.close('all')   

#%%%%%%%%%%%%#

    TowerTopAccelerationNormalIndex = dataIndex.columns.get_loc("YawBrTAxp")
    TowerTopAccelerationNormalNormal = data_normal_IPC.iloc[2:,TowerTopAccelerationNormalIndex]
    TowerTopAccelerationNormalNormal = [float(x) for x in TowerTopAccelerationNormalNormal]
    TowerTopAccelerationNormalFault = data_fault_IPC.iloc[2:,TowerTopAccelerationNormalIndex]
    TowerTopAccelerationNormalFault = [float(x) for x in TowerTopAccelerationNormalFault]

    TowerTopAccelerationLaterallIndex = dataIndex.columns.get_loc("YawBrTAyp")
    TowerTopAccelerationLateralNormal = data_normal_IPC.iloc[2:,TowerTopAccelerationLaterallIndex]
    TowerTopAccelerationLateralNormal = [float(x) for x in TowerTopAccelerationLateralNormal]
    TowerTopAccelerationLateralFault = data_fault_IPC.iloc[2:,TowerTopAccelerationLaterallIndex]
    TowerTopAccelerationLateralFault = [float(x) for x in TowerTopAccelerationLateralFault]

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(16,8)
    plt.subplot(2,1,1)
    plt.plot(Time,TowerTopAccelerationNormalNormal,label='Normal operation')
    plt.plot(Time,TowerTopAccelerationNormalFault,label='Blade mass fault operation')
    plt.title('Tower Top Accelerations \n Normal direction')
    plt.ylabel('m/s²')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(2,1,2)
    plt.plot(Time,TowerTopAccelerationLateralNormal,label='Normal operation')
    plt.plot(Time,TowerTopAccelerationLateralFault,label='Blade mass fault operation')
    plt.title('Lateral direction')
    plt.ylabel('m/s²')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.box(on=None)
    plt.tight_layout()

    plt.savefig(output_data+'/TowerTopAccelerations.png',dpi = 200)
    plt.close('all')

 #%%%%%%%%%%%%#

    TowerMidNormalIndex = dataIndex.columns.get_loc("TwHt1MLyt")
    TowerMidNormalNormal = data_normal_IPC.iloc[2:,TowerMidNormalIndex]
    TowerMidNormalNormal = [float(x) for x in TowerMidNormalNormal]
    TowerMidNormalFault = data_fault_IPC.iloc[2:,TowerMidNormalIndex]
    TowerMidNormalFault = [float(x) for x in TowerMidNormalFault]

    TowerMidLateralIndex = dataIndex.columns.get_loc("TwHt1MLxt")
    TowerMidLateralNormal = data_normal_IPC.iloc[2:,TowerMidLateralIndex]
    TowerMidLateralNormal = [float(x) for x in TowerMidLateralNormal]
    TowerMidLateralFault = data_fault_IPC.iloc[2:,TowerMidLateralIndex]
    TowerMidLateralFault = [float(x) for x in TowerMidLateralFault]

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(16,8)
    plt.subplot(2,1,1)
    plt.plot(Time,TowerMidNormalNormal,label='Normal operation')
    plt.plot(Time,TowerMidNormalFault,label='Blade mass fault operation')
    plt.title('Tower mid Moments \n Normal')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(2,1,2)
    plt.plot(Time,TowerMidLateralNormal,label='Normal operation')
    plt.plot(Time,TowerMidLateralFault,label='Blade mass fault operation')
    plt.title('Lateral')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.box(on=None)
    plt.tight_layout()

    plt.savefig(output_data+'/TowerMidMoments.png',dpi = 200)
    plt.close('all')

#%%%%%%%%%%%%#

    TowerTopNormalIndex = dataIndex.columns.get_loc("YawBrMyp")
    TowerTopNormalNormal = data_normal_IPC.iloc[2:,TowerTopNormalIndex]
    TowerTopNormalNormal = [float(x) for x in TowerTopNormalNormal]
    TowerTopNormalFault = data_fault_IPC.iloc[2:,TowerTopNormalIndex]
    TowerTopNormalFault = [float(x) for x in TowerTopNormalFault]

    TowerTopLateralIndex = dataIndex.columns.get_loc("YawBrMxp")
    TowerTopLateralNormal = data_normal_IPC.iloc[2:,TowerTopLateralIndex]
    TowerTopLateralNormal = [float(x) for x in TowerTopLateralNormal]
    TowerTopLateralFault = data_fault_IPC.iloc[2:,TowerTopLateralIndex]
    TowerTopLateralFault = [float(x) for x in TowerTopLateralFault]

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(16,8)
    plt.subplot(2,1,1)
    plt.plot(Time,TowerTopNormalNormal,label='Normal operation')
    plt.plot(Time,TowerTopNormalFault,label='Blade mass fault operation')
    plt.title('Tower top Moments \n Normal')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(2,1,2)
    plt.plot(Time,TowerTopLateralNormal,label='Normal operation')
    plt.plot(Time,TowerTopLateralFault,label='Blade mass fault operation')
    plt.title('Lateral')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.box(on=None)
    plt.tight_layout()

    plt.savefig(output_data+'/TowerTopMoments.png',dpi = 200)
    plt.close('all')

#%%%%%%%%%%%%#

    RotorPowerIndex = dataIndex.columns.get_loc("RotPwr")
    RotorPowerNormal = data_normal_IPC.iloc[2:,RotorPowerIndex]
    RotorPowerNormal = [float(x) for x in RotorPowerNormal]
    RotorPowerFault = data_fault_IPC.iloc[2:,RotorPowerIndex]
    RotorPowerFault = [float(x) for x in RotorPowerFault]

    GeneratorSpeedIndex = dataIndex.columns.get_loc("GenSpeed")
    GeneratorSpeedNormal = data_normal_IPC.iloc[2:,GeneratorSpeedIndex]
    GeneratorSpeedNormal = [float(x) for x in GeneratorSpeedNormal]
    GeneratorSpeedFault = data_fault_IPC.iloc[2:,GeneratorSpeedIndex]
    GeneratorSpeedFault = [float(x) for x in GeneratorSpeedFault]

    RotorSpeedIndex = dataIndex.columns.get_loc("RotSpeed")
    RotorSpeedNormal = data_normal_IPC.iloc[2:,RotorSpeedIndex]
    RotorSpeedNormal = [float(x) for x in RotorSpeedNormal]
    RotorSpeedFault = data_fault_IPC.iloc[2:,RotorSpeedIndex]
    RotorSpeedFault = [float(x) for x in RotorSpeedFault]

    AzimuthAngleIndex = dataIndex.columns.get_loc("Azimuth")
    AzimuthAngleNormal = data_normal_IPC.iloc[2:,AzimuthAngleIndex]
    AzimuthAngleNormal = [float(x) for x in AzimuthAngleNormal]
    AzimuthAngleFault = data_fault_IPC.iloc[2:,AzimuthAngleIndex]
    AzimuthAngleFault = [float(x) for x in AzimuthAngleFault]

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(16,8)   
    plt.subplot(4,1,1)
    plt.plot(Time,RotorPowerNormal,label='Normal operation')
    plt.plot(Time,RotorPowerFault,label='Blade mass fault operation')
    plt.title('General quantities \n Power')
    plt.ylabel('MW')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(4,1,2)
    plt.plot(Time,GeneratorSpeedNormal,label='Normal operation')
    plt.plot(Time,GeneratorSpeedFault,label='Blade mass fault operation')
    plt.title('Generator Speed')
    plt.ylabel('RPM')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(4,1,3)
    plt.plot(Time,RotorSpeedNormal,label='Normal operation')
    plt.plot(Time,RotorSpeedFault,label='Blade mass fault operation')
    plt.title('Rotor Speed')
    plt.ylabel('RPM')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(4,1,4)
    plt.plot(Time,AzimuthAngleNormal,label='Normal operation')
    plt.plot(Time,AzimuthAngleFault,label='Blade mass fault operation')
    plt.title('Rotor Azimuth Angle')
    plt.ylabel('Degrees')
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.box(on=None)
    plt.tight_layout()

    plt.savefig(output_data+'/Quantities.png',dpi = 200)
    plt.close('all')

    print('Check at "'+output_data+'" folder')
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
    n=parameters[13]
    
    fast_standard = open(path_fast+turbinefast).read().splitlines()
    turbinefast = turbinefast[0:len(turbinefast)-4]
    out_fault = turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(e)+'massfault-'+str(n)+'.sfunc.out'
    out =turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'.sfunc.out'

    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(e)+'massfault-'+str(n)+'/Individual pitch controller')==False:
        print('Run your turbine with '+str(v)+'m/s wind speed '+str(h)+'hub heigh '+str(t)+'% turbulence intensity with '+str(s)+' seconds of duration first')
    else:
        fault_col= path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(e)+'massfault-'+str(n)+'/Individual pitch controller/'
   
    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User Outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/Individual pitch controller')==False:
        print('Run your turbine with '+str(v)+'m/s wind speed '+str(h)+'hub heigh '+str(t)+'% turbulence intensity with '+str(s)+' seconds of duration first')
    else:
        normal_col= path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User Outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/Individual pitch controller/'        

    if os.path.exists(fault_col+'Output Data')==False:
        os.mkdir(fault_col+'Output Data')

    output_data = fault_col+'Output Data/'

    standard_normal_col=open(normal_col+out).read().splitlines()
    standard_fault_col= open(fault_col+out_fault).read().splitlines()

    out = out[0:len(out)-4]
    out_fault = out_fault[0:len(out)-4]


    ## NEW OUT COLLECTIVE NORMAL

    normal_noHeader_col = open(output_data+out+'normalcolnoHeader.out','w')
                            
    i = 0
    for linha in standard_normal_col:
        if i >5:
            normal_noHeader_col.write(linha+'\n')
        else:
            i=i+1
    normal_noHeader_col.close()
    
    normal_noHeader_col = output_data+out+'normalcolnoHeader.out'
    f = open(normal_noHeader_col, 'r+')                  
    row_list = []
    normal_noHeader_col = normal_noHeader_col[0:len(normal_noHeader_col)-4]
    for row in f:
        row_list.append(row.split())
    column_list = zip(*row_list)
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Sheet1')
    i = 0
    for column in column_list:
        for item in range(len(column)):
            worksheet.write(item, i, column[item])
        workbook.save(normal_noHeader_col+'.xls')
        i+=1

    ## NEW OUT COLLECTIVE FAULT

    fault_noHeader_col = open(output_data+out+'faultcolnoHeader.out','w')
                            
    i = 0
    for linha in standard_fault_col:
        if i >5:
            fault_noHeader_col.write(linha+'\n')
        else:
            i=i+1
    fault_noHeader_col.close()
    
    fault_noHeader_col = output_data+out+'faultcolnoHeader.out'
    
    f = open(fault_noHeader_col, 'r+')                  
    row_list = []
    fault_noHeader_col = fault_noHeader_col[0:len(fault_noHeader_col)-4]
    for row in f:
        row_list.append(row.split())
    column_list = zip(*row_list)
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Sheet1')
    i = 0
    for column in column_list:
        for item in range(len(column)):
            worksheet.write(item, i, column[item])
        workbook.save(fault_noHeader_col+'.xls')
        i+=1

    ## Get data
        
    data_normal_col = pd.read_excel(normal_noHeader_col+'.xls',header=None)
    data_fault_col= pd.read_excel(fault_noHeader_col+'.xls',header=None)

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

    for i in range(len(fig_normal_col)):
        plt.close('all')
        plt.figure()
        plt.plot(Time,fig_normal_col[i],label='Normal Collective')
        plt.plot(Time,fig_fault_col[i],label='Fault Collective')
        plt.title(output[i+1])
        plt.ylabel(legend[i+1])
        plt.xlabel('Time \n Wind speed at '+str(v)+'m/s and '+str(t)+'% turbulence intensity')
        plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
        plt.box(on=None)
        plt.savefig(output_data+output[i+1]+'.png',bbox_inches='tight')
        plt.close('all')
