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
    n=parameters[13]

    fast_standard = open(path_fast+turbinefast).read().splitlines()
    turbinefast = turbinefast[0:len(turbinefast)-4]

    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 Outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/Collective pitch controller')==False:
        print('Run your turbine with '+str(v)+'m/s wind speed '+str(h)+'hub heigh '+str(t)+'% turbulence intensity with '+str(s)+' seconds of duration first')
    else:
        new_path = path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 Outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/Collective pitch controller/'
        out = turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'.sfunc.out'
        
    standard_out = open(new_path+out).read().splitlines()
    output_string = out[0:len(out)-4]

    if os.path.exists(new_path+'Output data') == False:
        os.mkdir(new_path+'Output data')

    sim_path = new_path+'Output data/'
    out_noHeader = open(sim_path+output_string+'noHeader.out','w')
                            
    i = 0
    for linha in standard_out:
        if i>5:
            out_noHeader.write(linha+'\n')
        else:
            i=i+1                    
    out_noHeader = sim_path+output_string+'noHeader.out'

    f = open(out_noHeader, 'r+')                  
    row_list = []
    
    for row in f:
        row_list.append(row.split())
    column_list = zip(*row_list)
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Sheet1')
    i = 0
    out_noHeader=out_noHeader[0:len(out_noHeader)-4]
    
    for column in column_list:
        for item in range(len(column)):
            worksheet.write(item, i, column[item])
        workbook.save(out_noHeader+'.xls')
        i+=1
    
    data = pd.read_excel(out_noHeader+'.xls',header=None)
    dataIndex = pd.read_excel(out_noHeader+'.xls')
    
    TimeIndex = dataIndex.columns.get_loc('Time')
    Time = data.iloc[2:,TimeIndex]
    Time = [float(x) for x in Time]

#%%%%%%%%%%%%#
    
    BladeRootFlapWiseM1Index = dataIndex.columns.get_loc("RootMxb1")
    BladeRootFlapWiseM1 = data.iloc[2:,BladeRootFlapWiseM1Index]
    BladeRootFlapWiseM1 = [float(x) for x in BladeRootFlapWiseM1]

    BladeRootFlapWiseM2Index = dataIndex.columns.get_loc("RootMxb2")
    BladeRootFlapWiseM2 = data.iloc[2:,BladeRootFlapWiseM2Index]
    BladeRootFlapWiseM2 = [float(x) for x in BladeRootFlapWiseM2]

    BladeRootFlapWiseM3Index = dataIndex.columns.get_loc("RootMxb3")
    BladeRootFlapWiseM3 = data.iloc[2:,BladeRootFlapWiseM3Index]
    BladeRootFlapWiseM3 = [float(x) for x in BladeRootFlapWiseM3]

    
    plt.figure()
    plt.subplot(3,1,1)
    plt.plot(Time,BladeRootFlapWiseM1)
    plt.title('Blade Root Flapwise Moments\nBlade 1')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,2)
    plt.plot(Time,BladeRootFlapWiseM2)
    plt.title('Blade 2')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,3)
    plt.plot(Time,BladeRootFlapWiseM3)
    plt.title('Blade 3')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()
    
    plt.savefig(sim_path+'/BladeRootFlapMoments.png',bbox_inches='tight')
    plt.close('all')
    
#%%%%%%%%%%%%#

    BladeRootEdgeWiseM1Index = dataIndex.columns.get_loc("RootMyb1")
    BladeRootEdgeWiseM1 = data.iloc[2:,BladeRootEdgeWiseM1Index]
    BladeRootEdgeWiseM1 = [float(x) for x in BladeRootEdgeWiseM1]

    BladeRootEdgeWiseM2Index = dataIndex.columns.get_loc("RootMyb2")
    BladeRootEdgeWiseM2 = data.iloc[2:,BladeRootEdgeWiseM2Index]
    BladeRootEdgeWiseM2 = [float(x) for x in BladeRootEdgeWiseM2]

    BladeRootEdgeWiseM3Index = dataIndex.columns.get_loc("RootMyb3")
    BladeRootEdgeWiseM3 = data.iloc[2:,BladeRootEdgeWiseM3Index]
    BladeRootEdgeWiseM3 = [float(x) for x in BladeRootEdgeWiseM3]

    
    plt.figure()
    plt.subplot(3,1,1)
    plt.plot(Time,BladeRootEdgeWiseM1)
    plt.title('Blades Root Edgewise Moments\nBlade 1')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,2)
    plt.plot(Time,BladeRootEdgeWiseM2)
    plt.title('Blade 2')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,3)
    plt.plot(Time,BladeRootEdgeWiseM3)
    plt.title('Blade 3')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()
    
    plt.savefig(sim_path+'/BladeRootEdgeMoments.png',bbox_inches='tight')
    plt.close('all')

#%%%%%%%%%%%%#

    RotorTiltMomentIndex = dataIndex.columns.get_loc("YawBrMxn")
    RotorTiltMoment = data.iloc[2:,RotorTiltMomentIndex]
    RotorTiltMoment = [float(x) for x in RotorTiltMoment]

    RotorYawMomentIndex = dataIndex.columns.get_loc("YawBrMzn")
    RotorYawMoment = data.iloc[2:,RotorYawMomentIndex]
    RotorYawMoment = [float(x) for x in RotorYawMoment]

    RotorTorqueIndex = dataIndex.columns.get_loc("LSShftMxa")
    RotorTorque = data.iloc[2:,RotorTorqueIndex]
    RotorTorque = [float(x) for x in RotorTorque]

    plt.figure()
    plt.subplot(3,1,1)
    plt.plot(Time,RotorTiltMoment)
    plt.title('Rotor Quantities\nTilt Moment')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,2)
    plt.plot(Time,RotorYawMoment)
    plt.title('Yaw Moment')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,3)
    plt.plot(Time,RotorTorque)
    plt.title('Rotor Torque')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()
    
    plt.savefig(sim_path+'/RotorQuantities.png',bbox_inches='tight')
    plt.close('all')

#%%%%%%%%%%%%#

    TowerBaseNormalIndex = dataIndex.columns.get_loc("TwrBsMyt")
    TowerBaseNormal = data.iloc[2:,TowerBaseNormalIndex]
    TowerBaseNormal = [float(x) for x in TowerBaseNormal]

    TowerBaseLateralIndex = dataIndex.columns.get_loc("TwrBsMxt")
    TowerBaseLateral = data.iloc[2:,TowerBaseLateralIndex]
    TowerBaseLateral = [float(x) for x in TowerBaseLateral]

    TowerTorqueIndex = dataIndex.columns.get_loc("TwrBsMzt")
    TowerTorque = data.iloc[2:,TowerTorqueIndex]
    TowerTorque = [float(x) for x in TowerTorque]

    plt.figure()
    plt.subplot(3,1,1)
    plt.plot(Time,TowerBaseNormal)
    plt.title('Tower Base Moments\nNormal')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,2)
    plt.plot(Time,TowerBaseLateral)
    plt.title('Lateral')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,3)
    plt.plot(Time,TowerTorque)
    plt.title('Tower Torque')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.savefig(sim_path+'/TowerMoments.png',bbox_inches='tight')
    plt.close('all')

#%%%%%%%%%%%%#

    PitchActuationoLoad1Index = dataIndex.columns.get_loc("RootMzc1")
    PitchActuationoLoad1 = data.iloc[2:,PitchActuationoLoad1Index]
    PitchActuationoLoad1 = [float(x) for x in PitchActuationoLoad1]

    PitchActuationoLoad2Index = dataIndex.columns.get_loc("RootMzc2")
    PitchActuationoLoad2 = data.iloc[2:,PitchActuationoLoad2Index]
    PitchActuationoLoad2 = [float(x) for x in PitchActuationoLoad2]

    PitchActuationoLoad3Index = dataIndex.columns.get_loc("RootMzc3")
    PitchActuationoLoad3 = data.iloc[2:,PitchActuationoLoad3Index]
    PitchActuationoLoad3 = [float(x) for x in PitchActuationoLoad3]

    plt.figure()
    plt.subplot(3,1,1)
    plt.plot(Time,PitchActuationoLoad1)
    plt.title('Pitch actuation loads\nBlade 1')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,2)
    plt.plot(Time,PitchActuationoLoad2)
    plt.title('Blade 2')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,3)
    plt.plot(Time,PitchActuationoLoad3)
    plt.title('Blade 3')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.savefig(sim_path+'/PitchActuationLoads.png',bbox_inches='tight')
    plt.close('all')   

#%%%%%%%%%%%%#

    TowerTopAccelerationNormalIndex = dataIndex.columns.get_loc("YawBrTAxp")
    TowerTopAccelerationNormal = data.iloc[2:,TowerTopAccelerationNormalIndex]
    TowerTopAccelerationNormal = [float(x) for x in TowerTopAccelerationNormal]

    TowerTopAccelerationLaterallIndex = dataIndex.columns.get_loc("YawBrTAyp")
    TowerTopAccelerationLateral = data.iloc[2:,TowerTopAccelerationLaterallIndex]
    TowerTopAccelerationLateral = [float(x) for x in TowerTopAccelerationLateral]

    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(Time,TowerTopAccelerationNormal)
    plt.title('Tower Top Accelerations\nNormal direction')
    plt.ylabel('m/s^2')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(2,1,2)
    plt.plot(Time,TowerTopAccelerationLateral)
    plt.title('Lateral Direction')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.savefig(sim_path+'/TowerTopAccelerations.png',bbox_inches='tight')
    plt.close('all')

 #%%%%%%%%%%%%#

    TowerMidNormalIndex = dataIndex.columns.get_loc("TwHt1MLyt")
    TowerMidNormal = data.iloc[2:,TowerMidNormalIndex]
    TowerMidNormal = [float(x) for x in TowerMidNormal]

    TowerMidLateralIndex = dataIndex.columns.get_loc("TwHt1MLxt")
    TowerMidLateral = data.iloc[2:,TowerMidLateralIndex]
    TowerMidLateral = [float(x) for x in TowerMidLateral]

    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(Time,TowerMidNormal)
    plt.title('Tower mid Moments\nNormal')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(2,1,2)
    plt.plot(Time,TowerMidLateral)
    plt.title('Lateral')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.savefig(sim_path+'/TowerMidMoments.png',bbox_inches='tight')
    plt.close('all')

 #%%%%%%%%%%%%#

    TowerTopNormalIndex = dataIndex.columns.get_loc("YawBrMyp")
    TowerTopNormal = data.iloc[2:,TowerTopNormalIndex]
    TowerTopNormal = [float(x) for x in TowerTopNormal]

    TowerTopLateralIndex = dataIndex.columns.get_loc("YawBrMxp")
    TowerTopLateral = data.iloc[2:,TowerTopLateralIndex]
    TowerTopLateral = [float(x) for x in TowerTopLateral]

    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(Time,TowerTopNormal)
    plt.title('Tower top Moments\nNormal')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(2,1,2)
    plt.plot(Time,TowerTopLateral)
    plt.title('Lateral')
    plt.ylabel('kN.m')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.savefig(sim_path+'/TowerTopMoments.png',bbox_inches='tight')
    plt.close('all')

#%%%%%%%%%%%%#

    RotorPowerIndex = dataIndex.columns.get_loc("RotPwr")
    RotorPower = data.iloc[2:,RotorPowerIndex]
    RotorPower = [float(x) for x in RotorPower]

    GeneratorSpeedIndex = dataIndex.columns.get_loc("GenSpeed")
    GeneratorSpeed = data.iloc[2:,GeneratorSpeedIndex]
    GeneratorSpeed = [float(x) for x in GeneratorSpeed]

    RotorSpeedIndex = dataIndex.columns.get_loc("RotSpeed")
    RotorSpeed = data.iloc[2:,RotorSpeedIndex]
    RotorSpeed = [float(x) for x in RotorSpeed]

    AzimuthAngleIndex = dataIndex.columns.get_loc("Azimuth")
    AzimuthAngle = data.iloc[2:,AzimuthAngleIndex]
    AzimuthAngle = [float(x) for x in AzimuthAngle]

    plt.figure()
    plt.subplot(4,1,1)
    plt.plot(Time,RotorPower)
    plt.title('General quantities\n Power')
    plt.ylabel('MW')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(4,1,2)
    plt.plot(Time,GeneratorSpeed)
    plt.title('Generator Speed')
    plt.ylabel('RPM')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(4,1,3)
    plt.plot(Time,RotorSpeed)
    plt.title('Rotor Speed')
    plt.ylabel('RPM')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(4,1,4)
    plt.plot(Time,AzimuthAngle)
    plt.title('Rotor Azimuth Angle')
    plt.ylabel('Degrees')
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    plt.tight_layout()

    plt.savefig(sim_path+'/Quantities.png',bbox_inches='tight')
    plt.close('all')

    print('Check at "'+new_path+'Output data" folder')

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
    n=parameters[10]

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
    n=parameters[13]

    fast_standard = open(path_fast+turbinefast).read().splitlines()
    turbinefast = turbinefast[0:len(turbinefast)-4]

    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User Outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/Collective pitch controller')==False:
        print('Run your turbine with '+str(v)+'m/s wind speed '+str(h)+'hub heigh '+str(t)+'% turbulence intensity with '+str(s)+' seconds of duration first')
    else:
        new_path = path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User Outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/Collective pitch controller/'
        out = turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'.sfunc.out'
        
    standard_out = open(new_path+out).read().splitlines()
    output_string = out[0:len(out)-4]

    if os.path.exists(new_path+'Output data') == False:
        os.mkdir(new_path+'Output data')

    sim_path = new_path+'Output data/'
    out_noHeader = open(sim_path+output_string+'noHeader.out','w')
                            
    i = 0
    for linha in standard_out:
        if i>5:
            out_noHeader.write(linha+'\n')
        else:
            i=i+1                    
    out_noHeader = sim_path+output_string+'noHeader.out'

    f = open(out_noHeader, 'r+')                  
    row_list = []
    
    for row in f:
        row_list.append(row.split())
    column_list = zip(*row_list)
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Sheet1')
    i = 0
    out_noHeader=out_noHeader[0:len(out_noHeader)-4]
    
    for column in column_list:
        for item in range(len(column)):
            worksheet.write(item, i, column[item])
        workbook.save(new_path+output_string+'.xls')
        i+=1
    
    data = pd.read_excel(new_path+output_string+'.xls',header=None)
    output = data.iloc[0,0:]
    output = [str(x) for x in output]
    legend = data.iloc[1,0:]
    legend = [str(x) for x in legend]
       
    Time = data.iloc[2:,0]
    Time = [float(x) for x in Time]
    fig=[]
    
    for i in range(1,len(data.columns)):
        series =data.iloc[2:,i]
        fig.append(series)
    for i in range(len(fig)):
        fig[i]=[float(x) for x in fig[i]]
    
    for i in range(len(legend)):
        legend[i] = legend[i][1:len(legend[i])-1]
            
    for i in range(len(fig)):
        plt.close('all')
        plt.figure()
        plt.plot(Time,fig[i])
        plt.title(output[i+1])
        plt.ylabel(legend[i+1])
        plt.box(on=None)
        plt.savefig(sim_path+output[i+1]+'.png',bbox_inches='tight')
        plt.close('all')