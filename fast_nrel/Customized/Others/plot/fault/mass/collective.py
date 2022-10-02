# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 17:31:04 2018

@author: Leonardo
"""

import pandas as pd
import matplotlib.pyplot as plt
import xlwt
import os
import numpy as np
from scipy.fftpack import fft, ifft

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

    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(e)+'massfault-'+str(n)+'/Collective pitch controller')==False:
         print('Run your turbine with '+str(v)+'m/s wind speed '+str(h)+'hub heigh '+str(t)+'% turbulence intensity with '+str(s)+' seconds of duration first')
    else:
        fault_col= path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(e)+'massfault-'+str(n)+'/Collective pitch controller/'
   
    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 Outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/Collective pitch controller')==False:
        print('Run your turbine with '+str(v)+'m/s wind speed '+str(h)+'hub heigh '+str(t)+'% turbulence intensity with '+str(s)+' seconds of duration first')
    else:
        normal_col= path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - IEC61400.13 Outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/Collective pitch controller/'
        
    if os.path.exists(fault_col+'Output Data')==False:
        os.mkdir(fault_col+'Output Data')

    output_data = fault_col+'Output Data/'
    standard_normal_col=open(normal_col+out).read().splitlines()
    standard_fault_col= open(fault_col+out_fault).read().splitlines()

    out = out[0:len(out)-4]
    out_fault = out_fault[0:len(out)-4]


    ## NEW OUT COLLECTIVE NORMAL

    normal_noHeader_col = open(output_data+str(v)+'ms-'+str(t)+'ti-'+'NormalnoHeader.out','w')
                           
    i = 0
    for linha in standard_normal_col:
        if i >5:
            normal_noHeader_col.write(linha+'\n')
        else:
            i=i+1
    normal_noHeader_col.close()
    normal_noHeader_col = output_data+str(v)+'ms-'+str(t)+'ti-'+'NormalnoHeader.out'
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

    fault_noHeader_col = open(output_data+str(v)+'ms-'+str(t)+'ti-'+str(e)+'MassFaultnoHeader.out','w')
                            
    i = 0
    for linha in standard_fault_col:
        if i >5:
            fault_noHeader_col.write(linha+'\n')
        else:
            i=i+1
    fault_noHeader_col.close()
    
    fault_noHeader_col = output_data+str(v)+'ms-'+str(t)+'ti-'+str(e)+'MassFaultnoHeader.out'
    
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

    dataIndex =  pd.read_excel(normal_noHeader_col+'.xls')
    data_normal_col = pd.read_excel(normal_noHeader_col+'.xls',header=None)
    data_fault_col= pd.read_excel(fault_noHeader_col+'.xls',header=None)
    
    TimeIndex = dataIndex.columns.get_loc('Time')
    Time = data_normal_col.iloc[2:,TimeIndex]
    Time = [float(x) for x in Time]

    legend_positionX=0.95
    legend_positionY=0.99
    inches_x_time_series=14
    inches_y_time_series=8
    inches_x_FFT=12
    inches_y_FFT=8

    N= len(Time)
    K=np.arange(0,N,1)
    T = N/frequency
    Freq_mirror = K/T
    cut=int(N)+1
    xmin =0.2
    xmax=frequency*0.5/3
    ymin=0
    
    ## Where to get y vectors    
    points = frequency/N
    y0=0.2/points
    yf=xmax/points
    y0=int(y0)
    yf=int(yf)
    font_size= 15
    legend_size = 13
    tick_size = 12
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
    
    BladeRootFlapWiseM1Index = dataIndex.columns.get_loc("RootMxb1")
    BladeRootFlapWiseM1Normal = data_normal_col.iloc[2:,BladeRootFlapWiseM1Index]
    BladeRootFlapWiseM1Normal = [float(x) for x in BladeRootFlapWiseM1Normal]

    BladeRootFlapWiseM1Fault = data_fault_col.iloc[2:,BladeRootFlapWiseM1Index]
    BladeRootFlapWiseM1Fault = [float(x) for x  in BladeRootFlapWiseM1Fault]

    BladeRootFlapWiseM2Index = dataIndex.columns.get_loc("RootMxb2")
    BladeRootFlapWiseM2Normal = data_normal_col.iloc[2:,BladeRootFlapWiseM2Index]
    BladeRootFlapWiseM2Normal = [float(x) for x in BladeRootFlapWiseM2Normal]

    BladeRootFlapWiseM2Fault = data_fault_col.iloc[2:,BladeRootFlapWiseM2Index]
    BladeRootFlapWiseM2Fault = [float(x) for x in BladeRootFlapWiseM2Fault]

    BladeRootFlapWiseM3Index = dataIndex.columns.get_loc("RootMxb3")
    BladeRootFlapWiseM3Normal = data_normal_col.iloc[2:,BladeRootFlapWiseM3Index]
    BladeRootFlapWiseM3Normal = [float(x) for x in BladeRootFlapWiseM3Normal]

    BladeRootFlapWiseM3Fault = data_fault_col.iloc[2:,BladeRootFlapWiseM3Index]
    BladeRootFlapWiseM3Fault = [float(x) for x in BladeRootFlapWiseM3Fault]
   
    ## Time Series

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(inches_x_time_series,inches_y_time_series)
    plt.subplot(3,1,1)
    plt.plot(Time,BladeRootFlapWiseM1Normal,label = 'Normal operation')
    plt.plot(Time,BladeRootFlapWiseM1Fault,label='Blade mass fault operation')
    plt.title('Blade Root Flapwise Moments\nBlade 1',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,2)
    plt.plot(Time,BladeRootFlapWiseM2Normal,label = 'Normal operation')
    plt.plot(Time,BladeRootFlapWiseM2Fault,label='Blade mass fault operation')
    plt.title('Blade 2',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()
 
    plt.subplot(3,1,3)
    plt.plot(Time,BladeRootFlapWiseM3Normal,label = 'Normal operation')
    plt.plot(Time,BladeRootFlapWiseM3Fault,label='Blade mass fault operation')
    plt.title('Blade 3',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.xlabel('Time(s)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity and '+str(e)+'% blade mass fault at blade 1',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.savefig(output_data+'/BladeRootFlapMoments.png',dpi = 200)
    plt.close('all')
    
    ## FFT 

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(inches_x_FFT,inches_y_FFT)
    plt.subplot(3,1,1)
    BladeRootFlapWiseM1NormalFFT = fft(BladeRootFlapWiseM1Normal,N)
    BladeRootFlapWiseM1NormalFFT=np.abs(BladeRootFlapWiseM1NormalFFT)
    BladeRootFlapWiseM1NormalFFT=BladeRootFlapWiseM1NormalFFT/(N/2)
    BladeRootFlapWiseM1FaultFFT = fft(BladeRootFlapWiseM1Fault)
    BladeRootFlapWiseM1FaultFFT=np.abs(BladeRootFlapWiseM1FaultFFT)
    BladeRootFlapWiseM1FaultFFT = BladeRootFlapWiseM1FaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],BladeRootFlapWiseM1NormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],BladeRootFlapWiseM1FaultFFT[0:cut],label='Blade mass fault operation FFT')
    plt.title('Blade Root Flapwise Moments FFT\nBlade 1',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    ymax= max(BladeRootFlapWiseM1FaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()

    plt.subplot(3,1,2)
    BladeRootFlapWiseM2NormalFFT = fft(BladeRootFlapWiseM2Normal,N)
    BladeRootFlapWiseM2NormalFFT=np.abs(BladeRootFlapWiseM2NormalFFT)
    BladeRootFlapWiseM2NormalFFT=BladeRootFlapWiseM2NormalFFT/(N/2)
    BladeRootFlapWiseM2FaultFFT = fft(BladeRootFlapWiseM2Fault,N)
    BladeRootFlapWiseM2FaultFFT=np.abs(BladeRootFlapWiseM2FaultFFT)
    BladeRootFlapWiseM2FaultFFT = BladeRootFlapWiseM2FaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],BladeRootFlapWiseM2NormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],BladeRootFlapWiseM2FaultFFT[0:cut],label='Blade mass fault operation FFT')
    plt.title('Blade 2',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    ymax = max(BladeRootFlapWiseM2FaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()

    plt.subplot(3,1,3)
    BladeRootFlapWiseM3NormalFFT = fft(BladeRootFlapWiseM3Normal,N)
    BladeRootFlapWiseM3NormalFFT=np.abs(BladeRootFlapWiseM3NormalFFT)
    BladeRootFlapWiseM3NormalFFT=BladeRootFlapWiseM3NormalFFT/(N/2)
    BladeRootFlapWiseM3FaultFFT = fft(BladeRootFlapWiseM3Fault,N)
    BladeRootFlapWiseM3FaultFFT=np.abs(BladeRootFlapWiseM3FaultFFT)
    BladeRootFlapWiseM3FaultFFT = BladeRootFlapWiseM3FaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],BladeRootFlapWiseM3NormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],BladeRootFlapWiseM3FaultFFT[0:cut],label='Blade mass fault operation FFT')
    plt.title('Blade 3',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.xlabel('Frequency(Hz)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity and '+str(e)+'% blade mass fault at blade 1',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))    
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    ymax = max(BladeRootFlapWiseM3FaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()

    plt.savefig(output_data+'/BladeRootFlapMomentsFFT.png',dpi = 200)
    plt.close('all')
    
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

    BladeRootEdgeWiseM1Index = dataIndex.columns.get_loc("RootMyb1")
    BladeRootEdgeWiseM1Normal = data_normal_col.iloc[2:,BladeRootEdgeWiseM1Index]
    BladeRootEdgeWiseM1Normal = [float(x) for x in BladeRootEdgeWiseM1Normal]

    BladeRootEdgeWiseM1Fault = data_fault_col.iloc[2:,BladeRootEdgeWiseM1Index]
    BladeRootEdgeWiseM1Fault = [float(x) for x in BladeRootEdgeWiseM1Fault]

    BladeRootEdgeWiseM2Index = dataIndex.columns.get_loc("RootMyb2")
    BladeRootEdgeWiseM2Normal = data_normal_col.iloc[2:,BladeRootEdgeWiseM2Index]
    BladeRootEdgeWiseM2Normal = [float(x) for x in BladeRootEdgeWiseM2Normal]

    BladeRootEdgeWiseM2Fault = data_fault_col.iloc[2:,BladeRootEdgeWiseM2Index]
    BladeRootEdgeWiseM2Fault = [float(x) for x in BladeRootEdgeWiseM2Fault]

    BladeRootEdgeWiseM3Index = dataIndex.columns.get_loc("RootMyb3")
    BladeRootEdgeWiseM3Normal = data_normal_col.iloc[2:,BladeRootEdgeWiseM3Index]
    BladeRootEdgeWiseM3Normal = [float(x) for x in BladeRootEdgeWiseM3Normal]

    BladeRootEdgeWiseM3Fault = data_fault_col.iloc[2:,BladeRootEdgeWiseM3Index]
    BladeRootEdgeWiseM3Fault = [float(x) for x in BladeRootEdgeWiseM3Fault]

    ## Time Series

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(inches_x_time_series,inches_y_time_series)
    plt.subplot(3,1,1)
    plt.plot(Time,BladeRootEdgeWiseM1Normal,label = 'Normal operation')
    plt.plot(Time,BladeRootEdgeWiseM1Fault,label='Blade mass fault operation')
    plt.title('Blade Root Edgewise Moments\nBlade 1',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,2)
    plt.plot(Time,BladeRootEdgeWiseM2Normal,label = 'Normal operation')
    plt.plot(Time,BladeRootEdgeWiseM2Fault,label='Blade mass fault operation')
    plt.title('Blade 2',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,3)
    plt.plot(Time,BladeRootEdgeWiseM3Normal,label = 'Normal operation')
    plt.plot(Time,BladeRootEdgeWiseM3Fault,label='Blade mass fault operation')
    plt.title('Blade 3',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.xlabel('Time(s)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity and '+str(e)+'% blade mass fault at blade 1',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.savefig(output_data+'/BladeRootEdgeMoments.png',dpi = 200)
    plt.close('all')

    ## FFT

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(inches_x_FFT,inches_y_FFT)
    plt.subplot(3,1,1)
    BladeRootEdgeWiseM1NormalFFT = fft(BladeRootEdgeWiseM1Normal,N)
    BladeRootEdgeWiseM1NormalFFT=np.abs(BladeRootEdgeWiseM1NormalFFT)
    BladeRootEdgeWiseM1NormalFFT=BladeRootEdgeWiseM1NormalFFT/(N/2)
    BladeRootEdgeWiseM1FaultFFT = fft(BladeRootEdgeWiseM1Fault)
    BladeRootEdgeWiseM1FaultFFT=np.abs(BladeRootEdgeWiseM1FaultFFT)
    BladeRootEdgeWiseM1FaultFFT = BladeRootEdgeWiseM1FaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],BladeRootEdgeWiseM1NormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],BladeRootEdgeWiseM1FaultFFT[0:cut],label='Blade mass fault operation FFT')
    plt.title('Blade Root Edgewise Moments FFT\nBlade 1',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    ymax= max(BladeRootEdgeWiseM1FaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()

    plt.subplot(3,1,2)
    BladeRootEdgeWiseM2NormalFFT = fft(BladeRootEdgeWiseM2Normal,N)
    BladeRootEdgeWiseM2NormalFFT=np.abs(BladeRootEdgeWiseM2NormalFFT)
    BladeRootEdgeWiseM2NormalFFT=BladeRootEdgeWiseM2NormalFFT/(N/2)
    BladeRootEdgeWiseM2FaultFFT = fft(BladeRootEdgeWiseM2Fault,N)
    BladeRootEdgeWiseM2FaultFFT=np.abs(BladeRootEdgeWiseM2FaultFFT)
    BladeRootEdgeWiseM2FaultFFT = BladeRootEdgeWiseM2FaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],BladeRootEdgeWiseM2NormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],BladeRootEdgeWiseM2FaultFFT[0:cut],label='Blade mass fault operation FFT')
    plt.title('Blade 2',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    ymax = max(BladeRootEdgeWiseM2FaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()

    plt.subplot(3,1,3)
    BladeRootEdgeWiseM3NormalFFT = fft(BladeRootEdgeWiseM3Normal,N)
    BladeRootEdgeWiseM3NormalFFT=np.abs(BladeRootEdgeWiseM3NormalFFT)
    BladeRootEdgeWiseM3NormalFFT=BladeRootEdgeWiseM3NormalFFT/(N/2)
    BladeRootEdgeWiseM3FaultFFT = fft(BladeRootEdgeWiseM3Fault,N)
    BladeRootEdgeWiseM3FaultFFT=np.abs(BladeRootEdgeWiseM3FaultFFT)
    BladeRootEdgeWiseM3FaultFFT = BladeRootEdgeWiseM3FaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],BladeRootEdgeWiseM3NormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],BladeRootEdgeWiseM3FaultFFT[0:cut],label='Blade mass fault operation FFT')
    plt.title('Blade 3',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.xlabel('Frequency (Hz)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity and '+str(e)+'% blade mass fault at blade 1',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    ymax = max(BladeRootEdgeWiseM3FaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()

    plt.savefig(output_data+'/BladeRootEdgeMomentsFFT.png',dpi = 200)
    plt.close('all')
    

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

    RotorTiltMomentIndex = dataIndex.columns.get_loc("YawBrMxn")
    RotorTiltMomentNormal = data_normal_col.iloc[2:,RotorTiltMomentIndex]
    RotorTiltMomentNormal = [float(x) for x in RotorTiltMomentNormal]
    RotorTiltMomentFault = data_fault_col.iloc[2:,RotorTiltMomentIndex]
    RotorTiltMomentFault = [float(x) for x in RotorTiltMomentFault]

    RotorYawMomentIndex = dataIndex.columns.get_loc("YawBrMzn")
    RotorYawMomentNormal = data_normal_col.iloc[2:,RotorYawMomentIndex]
    RotorYawMomentNormal = [float(x) for x in RotorYawMomentNormal]
    RotorYawMomentFault = data_fault_col.iloc[2:,RotorYawMomentIndex]
    RotorYawMomentFault = [float(x) for x in RotorYawMomentFault]

    RotorTorqueIndex = dataIndex.columns.get_loc("LSShftMxa")
    RotorTorqueNormal = data_normal_col.iloc[2:,RotorTorqueIndex]
    RotorTorqueNormal = [float(x) for x in RotorTorqueNormal]
    RotorTorqueFault = data_fault_col.iloc[2:,RotorTorqueIndex]
    RotorTorqueFault = [float(x) for x in RotorTorqueFault]

    ## Time Series

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(inches_x_time_series,inches_y_time_series)
    plt.subplot(3,1,1)
    plt.plot(Time,RotorTiltMomentNormal,label = 'Normal operation')
    plt.plot(Time,RotorTiltMomentFault,'r--',label='Blade mass fault operation')
    plt.title('Rotor Quantities\nTilt Moment',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,2)
    plt.plot(Time,RotorYawMomentNormal,label = 'Normal operation')
    plt.plot(Time,RotorYawMomentFault,'r--',label='Blade mass fault operation')
    plt.title('Yaw Moment',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,3)
    plt.plot(Time,RotorTorqueNormal,label = 'Normal operation')
    plt.plot(Time,RotorTorqueFault,'r--',label='Blade mass fault operation')
    plt.title('Rotor Torque',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.xlabel('Time(s)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity and '+str(e)+'% blade mass fault at blade 1',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()
    plt.savefig(output_data+'/RotorQuantities.png',dpi = 200)
    plt.close('all')

    ## FFT

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(inches_x_FFT,inches_y_FFT)
    plt.subplot(3,1,1)
    RotorTiltMomentNormalFFT = fft(RotorTiltMomentNormal)
    RotorTiltMomentNormalFFT=np.abs(RotorTiltMomentNormalFFT)
    RotorTiltMomentNormalFFT=RotorTiltMomentNormalFFT/(N/2)
    RotorTiltMomentFaultFFT = fft(RotorTiltMomentFault)
    RotorTiltMomentFaultFFT=np.abs(RotorTiltMomentFaultFFT)
    RotorTiltMomentFaultFFT=RotorTiltMomentFaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],RotorTiltMomentNormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],RotorTiltMomentFaultFFT[0:cut],'r--',label='Blade mass fault operation FFT')
    plt.title('Rotor Quantities FFT\nTilt Moment',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    ymax=max(RotorTiltMomentFaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()

    plt.subplot(3,1,2)
    RotorYawMomentNormalFFT = fft(RotorYawMomentNormal)
    RotorYawMomentNormalFFT=np.abs(RotorYawMomentNormalFFT)
    RotorYawMomentNormalFFT=RotorYawMomentNormalFFT/(N/2)
    RotorYawMomentFaultFFT = fft(RotorYawMomentFault)
    RotorYawMomentFaultFFT=np.abs(RotorYawMomentFaultFFT)
    RotorYawMomentFaultFFT=RotorYawMomentFaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],RotorYawMomentNormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],RotorYawMomentFaultFFT[0:cut],'r--',label='Blade mass fault operation FFT')
    plt.title('Yaw Moment',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    ymax=max(RotorYawMomentFaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()

    plt.subplot(3,1,3)
    RotorTorqueNormalFFT = fft(RotorTorqueNormal)
    RotorTorqueNormalFFT=np.abs(RotorTorqueNormalFFT)
    RotorTorqueNormalFFT=RotorTorqueNormalFFT/(N/2)
    RotorTorqueFaultFFT = fft(RotorTorqueFault)
    RotorTorqueFaultFFT=np.abs(RotorTorqueFaultFFT)
    RotorTorqueFaultFFT=RotorTorqueFaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],RotorTorqueNormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],RotorTorqueFaultFFT[0:cut],'r--',label='Blade mass fault operation FFT')
    plt.title('Rotor torque',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.xlabel('Frequency (Hz)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity and '+str(e)+'% blade mass fault at blade 1',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    ymax=max(RotorTorqueFaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()
    
    plt.savefig(output_data+'/RotorQuantitiesFFT.png',dpi = 200)
    plt.close('all')


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

    TowerBaseNormalIndex = dataIndex.columns.get_loc("TwrBsMyt")
    TowerBaseNormalNormal = data_normal_col.iloc[2:,TowerBaseNormalIndex]
    TowerBaseNormalNormal = [float(x) for x in TowerBaseNormalNormal]
    TowerBaseNormalFault = data_fault_col.iloc[2:,TowerBaseNormalIndex]
    TowerBaseNormalFault = [float(x) for x in TowerBaseNormalFault]

    TowerBaseLateralIndex = dataIndex.columns.get_loc("TwrBsMxt")
    TowerBaseLateralNormal = data_normal_col.iloc[2:,TowerBaseLateralIndex]
    TowerBaseLateralNormal = [float(x) for x in TowerBaseLateralNormal]
    TowerBaseLateralFault = data_fault_col.iloc[2:,TowerBaseLateralIndex]
    TowerBaseLateralFault = [float(x) for x in TowerBaseLateralFault]

    TowerTorqueIndex = dataIndex.columns.get_loc("TwrBsMxt")
    TowerTorqueNormal = data_normal_col.iloc[2:,TowerTorqueIndex]
    TowerTorqueNormal = [float(x) for x in TowerTorqueNormal]
    TowerTorqueFault = data_fault_col.iloc[2:,TowerTorqueIndex]
    TowerTorqueFault = [float(x) for x in TowerTorqueFault]

    ## Time Series

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(inches_x_time_series,inches_y_time_series)
    plt.subplot(3,1,1)
    plt.title('Tower Moments\nBase Normal')
    plt.plot(Time,TowerBaseNormalNormal,label='Normal operation')
    plt.plot(Time,TowerBaseNormalFault,label='Blade mass fault operation')
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,2)
    plt.plot(Time,TowerBaseLateralNormal,label='Normal operation')
    plt.plot(Time,TowerBaseLateralFault,label='Blade mass fault operation')
    plt.title('Base Lateral',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,3)
    plt.plot(Time,TowerTorqueNormal,label = 'Normal operation')
    plt.plot(Time,TowerTorqueFault,label='Blade mass fault operation')
    plt.title('Torque',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.xlabel('Time(s)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity and '+str(e)+'% blade mass fault at blade 1',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.savefig(output_data+'/TowerMoments.png',dpi = 200)
    plt.close('all')

    ## FFT 

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(inches_x_FFT,inches_y_FFT)
    plt.subplot(3,1,1)
    TowerBaseNormalNormalFFT = fft(TowerBaseNormalNormal)
    TowerBaseNormalNormalFFT=np.abs(TowerBaseNormalNormalFFT)
    TowerBaseNormalNormalFFT=TowerBaseNormalNormalFFT/(N/2)
    TowerBaseNormalFaultFFT = fft(TowerBaseNormalFault)
    TowerBaseNormalFaultFFT=np.abs(TowerBaseNormalFaultFFT)
    TowerBaseNormalFaultFFT=TowerBaseNormalFaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],TowerBaseNormalNormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],TowerBaseNormalFaultFFT[0:cut],label='Blade mass fault operation FFT')
    plt.title('Tower base moments FFT\nNormal Moment',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    ymax= max(TowerBaseNormalFaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()

    plt.subplot(3,1,2)
    TowerBaseLateralNormalFFT = fft(TowerBaseLateralNormal)
    TowerBaseLateralNormalFFT=np.abs(TowerBaseLateralNormalFFT)
    TowerBaseLateralNormalFFT=TowerBaseLateralNormalFFT/(N/2)
    TowerBaseLateralFaultFFT = fft(TowerBaseLateralFault)
    TowerBaseLateralFaultFFT=np.abs(TowerBaseLateralFaultFFT)
    TowerBaseLateralFaultFFT=TowerBaseLateralFaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],TowerBaseLateralNormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],TowerBaseLateralFaultFFT[0:cut],label='Blade mass fault operation FFT')
    plt.title('Lateral Moment',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    ymax= max(TowerBaseLateralFaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()

    plt.subplot(3,1,3)
    TowerTorqueNormalFFT = fft(TowerTorqueNormal)
    TowerTorqueNormalFFT=np.abs(TowerTorqueNormalFFT)
    TowerTorqueNormalFFT=TowerTorqueNormalFFT/(N/2)
    TowerTorqueFaultFFT = fft(TowerTorqueFault)
    TowerTorqueFaultFFT=np.abs(TowerTorqueFaultFFT)
    TowerTorqueFaultFFT=TowerTorqueFaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],TowerTorqueNormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],TowerTorqueFaultFFT[0:cut],label='Blade mass fault operation FFT')
    plt.title('Tower torque',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.xlabel('Frequency (Hz)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity and '+str(e)+'% blade mass fault at blade 1',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    ymax= max(TowerTorqueFaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()
    
    plt.savefig(output_data+'/TowerMomentsFFT.png',dpi = 200)
    plt.close('all')


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

    PitchActuationoLoad1Index = dataIndex.columns.get_loc("RootMzc1")
    PitchActuationoLoad1Normal = data_normal_col.iloc[2:,PitchActuationoLoad1Index]
    PitchActuationoLoad1Normal = [float(x) for x in PitchActuationoLoad1Normal]
    PitchActuationoLoad1Fault = data_fault_col.iloc[2:,PitchActuationoLoad1Index]
    PitchActuationoLoad1Fault = [float(x) for x in PitchActuationoLoad1Fault]

    PitchActuationoLoad2Index = dataIndex.columns.get_loc("RootMzc2")
    PitchActuationoLoad2Normal = data_normal_col.iloc[2:,PitchActuationoLoad2Index]
    PitchActuationoLoad2Normal = [float(x) for x in PitchActuationoLoad2Normal]
    PitchActuationoLoad2Fault = data_fault_col.iloc[2:,PitchActuationoLoad2Index]
    PitchActuationoLoad2Fault = [float(x) for x in PitchActuationoLoad2Fault]

    PitchActuationoLoad3Index = dataIndex.columns.get_loc("RootMzc3")
    PitchActuationoLoad3Normal = data_normal_col.iloc[2:,PitchActuationoLoad3Index]
    PitchActuationoLoad3Normal = [float(x) for x in PitchActuationoLoad3Normal]
    PitchActuationoLoad3Fault = data_fault_col.iloc[2:,PitchActuationoLoad3Index]
    PitchActuationoLoad3Fault = [float(x) for x in PitchActuationoLoad3Fault]

    ## Time Series

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(inches_x_time_series,inches_y_time_series)
    plt.subplot(3,1,1)
    plt.plot(Time,PitchActuationoLoad1Normal,label='Normal operation')
    plt.plot(Time,PitchActuationoLoad1Fault,label='Blade mass fault operation')
    plt.title('Pitch actuation loads\nBlade 1',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,2)
    plt.plot(Time,PitchActuationoLoad2Normal,label='Normal operation')
    plt.plot(Time,PitchActuationoLoad2Fault,label='Blade mass fault operation')
    plt.title('Blade 2',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(3,1,3)
    plt.plot(Time,PitchActuationoLoad3Normal,label='Normal operation')
    plt.plot(Time,PitchActuationoLoad3Fault,label='Blade mass fault operation')
    plt.title(' Blade 3',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.xlabel('Time(s)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity and '+str(e)+'% blade mass fault at blade 1',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.savefig(output_data+'/PitchActuationLoads.png',dpi = 200)
    plt.close('all')

    ## FFT

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(inches_x_FFT,inches_y_FFT)
    plt.subplot(3,1,1)
    PitchActuationoLoad1NormalFFT = fft(PitchActuationoLoad1Normal)
    PitchActuationoLoad1NormalFFT=np.abs(PitchActuationoLoad1NormalFFT)
    PitchActuationoLoad1NormalFFT=PitchActuationoLoad1NormalFFT/(N/2)
    PitchActuationoLoad1FaultFFT = fft(PitchActuationoLoad1Fault)
    PitchActuationoLoad1FaultFFT=np.abs(PitchActuationoLoad1FaultFFT)
    PitchActuationoLoad1FaultFFT=PitchActuationoLoad1FaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],PitchActuationoLoad1NormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],PitchActuationoLoad1FaultFFT[0:cut],label='Blade mass fault operation FFT')
    plt.title('Pitch actuation loads FFT\nBlade 1',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    ymax= max(PitchActuationoLoad1FaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()

    plt.subplot(3,1,2)
    PitchActuationoLoad2NormalFFT = fft(PitchActuationoLoad2Normal)
    PitchActuationoLoad2NormalFFT=np.abs(PitchActuationoLoad2NormalFFT)
    PitchActuationoLoad2NormalFFT=PitchActuationoLoad2NormalFFT/(N/2)
    PitchActuationoLoad2FaultFFT = fft(PitchActuationoLoad2Fault)
    PitchActuationoLoad2FaultFFT=np.abs(PitchActuationoLoad2FaultFFT)
    PitchActuationoLoad2FaultFFT=PitchActuationoLoad2FaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],PitchActuationoLoad2NormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],PitchActuationoLoad2FaultFFT[0:cut],label='Blade mass fault operation FFT')
    plt.title('Blade 2',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    ymax= max(PitchActuationoLoad2FaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()

    plt.subplot(3,1,3)
    PitchActuationoLoad3NormalFFT = fft(PitchActuationoLoad3Normal)
    PitchActuationoLoad3NormalFFT=np.abs(PitchActuationoLoad3NormalFFT)
    PitchActuationoLoad3NormalFFT=PitchActuationoLoad3NormalFFT/(N/2)
    PitchActuationoLoad3FaultFFT = fft(PitchActuationoLoad3Fault)
    PitchActuationoLoad3FaultFFT=np.abs(PitchActuationoLoad3FaultFFT)
    PitchActuationoLoad3FaultFFT=PitchActuationoLoad3FaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],PitchActuationoLoad3NormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],PitchActuationoLoad3FaultFFT[0:cut],label='Blade mass fault operation FFT')
    plt.title('Blade 3',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.xlabel('Frequency (Hz)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity and '+str(e)+'% blade mass fault at blade 1',fontsize=font_size)
    plt.box(on=None)
    plt.tick_params(axis='y',labelsize = tick_size)
    ymax= max(PitchActuationoLoad3FaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()
    
    plt.savefig(output_data+'/PitchActuationLoadsFFT.png',dpi = 200)
    plt.close('all')


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

    TowerTopAccelerationNormalIndex = dataIndex.columns.get_loc("YawBrTAxp")
    TowerTopAccelerationNormalNormal = data_normal_col.iloc[2:,TowerTopAccelerationNormalIndex]
    TowerTopAccelerationNormalNormal = [float(x) for x in TowerTopAccelerationNormalNormal]
    TowerTopAccelerationNormalFault = data_fault_col.iloc[2:,TowerTopAccelerationNormalIndex]
    TowerTopAccelerationNormalFault = [float(x) for x in TowerTopAccelerationNormalFault]

    TowerTopAccelerationLaterallIndex = dataIndex.columns.get_loc("YawBrTAyp")
    TowerTopAccelerationLateralNormal = data_normal_col.iloc[2:,TowerTopAccelerationLaterallIndex]
    TowerTopAccelerationLateralNormal = [float(x) for x in TowerTopAccelerationLateralNormal]
    TowerTopAccelerationLateralFault = data_fault_col.iloc[2:,TowerTopAccelerationLaterallIndex]
    TowerTopAccelerationLateralFault = [float(x) for x in TowerTopAccelerationLateralFault]

    ## Time Series

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(inches_x_time_series,inches_y_time_series)
    plt.subplot(2,1,1)
    plt.plot(Time,TowerTopAccelerationNormalNormal,label='Normal operation')
    plt.plot(Time,TowerTopAccelerationNormalFault,'r--',label='Blade mass fault operation')
    plt.title('Tower Top Accelerations\nNormal direction',fontsize=font_size)
    plt.ylabel('m/s²',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(2,1,2)
    plt.plot(Time,TowerTopAccelerationLateralNormal,label='Normal operation')
    plt.plot(Time,TowerTopAccelerationLateralFault,'r--',label='Blade mass fault operation')
    plt.title('Lateral direction',fontsize=font_size)
    plt.ylabel('m/s²',fontsize=font_size)
    plt.xlabel('Time(s)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity and '+str(e)+'% blade mass fault at blade 1',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.savefig(output_data+'/TowerTopAccelerations.png',dpi = 200)
    plt.close('all')

    ## FFT

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(inches_x_FFT,inches_y_FFT)
    plt.subplot(2,1,1)
    TowerTopAccelerationNormalNormalFFT = fft(TowerTopAccelerationNormalNormal)
    TowerTopAccelerationNormalNormalFFT=np.abs(TowerTopAccelerationNormalNormalFFT)
    TowerTopAccelerationNormalNormalFFT=TowerTopAccelerationNormalNormalFFT/(N/2)
    TowerTopAccelerationNormalFaultFFT = fft(TowerTopAccelerationNormalFault)
    TowerTopAccelerationNormalFaultFFT=np.abs(TowerTopAccelerationNormalFaultFFT)
    TowerTopAccelerationNormalFaultFFT=TowerTopAccelerationNormalFaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],TowerTopAccelerationNormalNormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],TowerTopAccelerationNormalFaultFFT[0:cut],'r--',label='Blade mass fault operation FFT')
    plt.title('Tower top accelerations FFT\nNormal direction',fontsize=font_size)
    plt.ylabel('m/s²',fontsize=font_size) 
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    ymax= max(TowerTopAccelerationNormalFaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()

    plt.subplot(2,1,2)
    TowerTopAccelerationLateralNormalFFT = fft(TowerTopAccelerationLateralNormal)
    TowerTopAccelerationLateralNormalFFT=np.abs(TowerTopAccelerationLateralNormalFFT)
    TowerTopAccelerationLateralNormalFFT=TowerTopAccelerationLateralNormalFFT/(N/2)
    TowerTopAccelerationLateralFaultFFT = fft(TowerTopAccelerationLateralFault)
    TowerTopAccelerationLateralFaultFFT=np.abs(TowerTopAccelerationLateralFaultFFT)
    TowerTopAccelerationLateralFaultFFT=TowerTopAccelerationLateralFaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],TowerTopAccelerationLateralNormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],TowerTopAccelerationLateralFaultFFT[0:cut],'r--',label='Blade mass fault operation FFT')
    plt.title('Lateral direction',fontsize=font_size)
    plt.ylabel('m/s²',fontsize=font_size)
    plt.xlabel('Frequency (Hz)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity and '+str(e)+'% blade mass fault at blade 1',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)   
    ymax= max(TowerTopAccelerationLateralFaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()

    plt.savefig(output_data+'/TowerTopAccelerationsFFT.png',dpi = 200)
    plt.close('all')

 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

    TowerMidNormalIndex = dataIndex.columns.get_loc("TwHt1MLyt")
    TowerMidNormalNormal = data_normal_col.iloc[2:,TowerMidNormalIndex]
    TowerMidNormalNormal = [float(x) for x in TowerMidNormalNormal]
    TowerMidNormalFault = data_fault_col.iloc[2:,TowerMidNormalIndex]
    TowerMidNormalFault = [float(x) for x in TowerMidNormalFault]

    TowerMidLateralIndex = dataIndex.columns.get_loc("TwHt1MLxt")
    TowerMidLateralNormal = data_normal_col.iloc[2:,TowerMidLateralIndex]
    TowerMidLateralNormal = [float(x) for x in TowerMidLateralNormal]
    TowerMidLateralFault = data_fault_col.iloc[2:,TowerMidLateralIndex]
    TowerMidLateralFault = [float(x) for x in TowerMidLateralFault]

    ## Time Series

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(inches_x_time_series,inches_y_time_series)
    plt.subplot(2,1,1)
    plt.plot(Time,TowerMidNormalNormal,label='Normal operation')
    plt.plot(Time,TowerMidNormalFault,label='Blade mass fault operation')
    plt.title('Tower mid Moments\nNormal',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(2,1,2)
    plt.plot(Time,TowerMidLateralNormal,label='Normal operation')
    plt.plot(Time,TowerMidLateralFault,label='Blade mass fault operation')
    plt.title('Lateral',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.xlabel('Time (s)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity and '+str(e)+'% blade mass fault at blade 1',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.savefig(output_data+'/TowerMidMoments.png',dpi = 200)
    plt.close('all')

    ## FFT

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(inches_x_FFT,inches_y_FFT)
    plt.subplot(2,1,1)
    TowerMidNormalNormalFFT = fft(TowerMidNormalNormal)
    TowerMidNormalNormalFFT=np.abs(TowerMidNormalNormalFFT)
    TowerMidNormalNormalFFT=TowerMidNormalNormalFFT/(N/2)
    TowerMidNormalFaultFFT = fft(TowerMidNormalFault)
    TowerMidNormalFaultFFT=np.abs(TowerMidNormalFaultFFT)
    TowerMidNormalFaultFFT=TowerMidNormalFaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],TowerMidNormalNormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],TowerMidNormalFaultFFT[0:cut],label='Blade mass fault operation FFT')
    plt.title('Tower mid moments FFT\nNormal',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    ymax= max(TowerMidNormalFaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()

    plt.subplot(2,1,2)
    TowerMidLateralNormalFFT = fft(TowerMidLateralNormal)
    TowerMidLateralNormalFFT=np.abs(TowerMidLateralNormalFFT)
    TowerMidLateralNormalFFT=TowerMidLateralNormalFFT/(N/2)
    TowerMidLateralFaultFFT = fft(TowerMidLateralFault)
    TowerMidLateralFaultFFT=np.abs(TowerMidLateralFaultFFT)
    TowerMidLateralFaultFFT=TowerMidLateralFaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],TowerMidLateralNormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],TowerMidLateralFaultFFT[0:cut],label='Blade mass fault operation FFT')
    plt.title('Lateral',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.xlabel('Frequency (Hz)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity and '+str(e)+'% blade mass fault at blade 1',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    ymax= max(TowerMidLateralFaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()

    plt.savefig(output_data+'/TowerMidMomentsFFT.png',dpi = 200)
    plt.close('all')


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

    TowerTopNormalIndex = dataIndex.columns.get_loc("YawBrMyp")
    TowerTopNormalNormal = data_normal_col.iloc[2:,TowerTopNormalIndex]
    TowerTopNormalNormal = [float(x) for x in TowerTopNormalNormal]
    TowerTopNormalFault = data_fault_col.iloc[2:,TowerTopNormalIndex]
    TowerTopNormalFault = [float(x) for x in TowerTopNormalFault]

    TowerTopLateralIndex = dataIndex.columns.get_loc("YawBrMxp")
    TowerTopLateralNormal = data_normal_col.iloc[2:,TowerTopLateralIndex]
    TowerTopLateralNormal = [float(x) for x in TowerTopLateralNormal]
    TowerTopLateralFault = data_fault_col.iloc[2:,TowerTopLateralIndex]
    TowerTopLateralFault = [float(x) for x in TowerTopLateralFault]

    ## Time Series

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(inches_x_time_series,inches_y_time_series)
    plt.subplot(2,1,1)
    plt.plot(Time,TowerTopNormalNormal,label='Normal operation')
    plt.plot(Time,TowerTopNormalFault,'r--',label='Blade mass fault operation')
    plt.title('Tower top Moments\nNormal',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(2,1,2)
    plt.plot(Time,TowerTopLateralNormal,label='Normal operation')
    plt.plot(Time,TowerTopLateralFault,'r--',label='Blade mass fault operation')
    plt.title('Lateral',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.xlabel('Time (s)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity and '+str(e)+'% blade mass fault at blade 1',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.savefig(output_data+'/TowerTopMoments.png',dpi = 200)
    plt.close('all')

    ## FFT

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(inches_x_FFT,inches_y_FFT)
    plt.subplot(2,1,1)
    TowerTopMomentNormalNormalFFT = fft(TowerTopNormalNormal)
    TowerTopMomentNormalNormalFFT=np.abs(TowerTopMomentNormalNormalFFT)
    TowerTopMomentNormalNormalFFT=TowerTopMomentNormalNormalFFT/(N/2)
    TowerTopNormalFaultFFT = fft(TowerTopNormalFault)
    TowerTopNormalFaultFFT=np.abs(TowerTopNormalFaultFFT)
    TowerTopNormalFaultFFT=TowerTopNormalFaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],TowerTopMomentNormalNormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],TowerTopNormalFaultFFT[0:cut],'r--',label='Blade mass fault operation FFT')
    plt.title('Tower top Moments FFT\nNormal',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    ymax= max(TowerTopNormalFaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()

    plt.subplot(2,1,2)
    TowerTopLateralNormalFFT = fft(TowerTopLateralNormal)
    TowerTopLateralNormalFFT=np.abs(TowerTopLateralNormalFFT)
    TowerTopLateralNormalFFT=TowerTopLateralNormalFFT/(N/2)
    TowerTopLateralFaultFFT = fft(TowerTopLateralFault)
    TowerTopLateralFaultFFT=np.abs(TowerTopLateralFaultFFT)
    TowerTopLateralFaultFFT=TowerTopLateralFaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],TowerTopLateralNormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],TowerTopLateralFaultFFT[0:cut],'r--',label='Blade mass fault operation FFT')
    plt.title('Lateral',fontsize=font_size)
    plt.ylabel('kN.m',fontsize=font_size)
    plt.xlabel('Frequency (Hz)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity and '+str(e)+'% blade mass fault at blade 1',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    ymax= max(TowerTopLateralFaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()

    plt.savefig(output_data+'/TowerTopMomentsFFT.png',dpi = 200)
    plt.close('all')


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

    RotorPowerIndex = dataIndex.columns.get_loc("RotPwr")
    RotorPowerNormal = data_normal_col.iloc[2:,RotorPowerIndex]
    RotorPowerNormal = [float(x) for x in RotorPowerNormal]
    RotorPowerFault = data_fault_col.iloc[2:,RotorPowerIndex]
    RotorPowerFault = [float(x) for x in RotorPowerFault]

    GeneratorSpeedIndex = dataIndex.columns.get_loc("GenSpeed")
    GeneratorSpeedNormal = data_normal_col.iloc[2:,GeneratorSpeedIndex]
    GeneratorSpeedNormal = [float(x) for x in GeneratorSpeedNormal]
    GeneratorSpeedFault = data_fault_col.iloc[2:,GeneratorSpeedIndex]
    GeneratorSpeedFault = [float(x) for x in GeneratorSpeedFault]

    RotorSpeedIndex = dataIndex.columns.get_loc("RotSpeed")
    RotorSpeedNormal = data_normal_col.iloc[2:,RotorSpeedIndex]
    RotorSpeedNormal = [float(x) for x in RotorSpeedNormal]
    RotorSpeedFault = data_fault_col.iloc[2:,RotorSpeedIndex]
    RotorSpeedFault = [float(x) for x in RotorSpeedFault]

    AzimuthAngleIndex = dataIndex.columns.get_loc("Azimuth")
    AzimuthAngleNormal = data_normal_col.iloc[2:,AzimuthAngleIndex]
    AzimuthAngleNormal = [float(x) for x in AzimuthAngleNormal]
    AzimuthAngleFault = data_fault_col.iloc[2:,AzimuthAngleIndex]
    AzimuthAngleFault = [float(x) for x in AzimuthAngleFault]

    ## Time Series

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(inches_x_time_series,inches_y_time_series)   
    plt.subplot(4,1,1)
    plt.plot(Time,RotorPowerNormal,label='Normal operation')
    plt.plot(Time,RotorPowerFault,label='Blade mass fault operation')
    plt.title('General quantities\nPower',fontsize=font_size)
    plt.ylabel('MW',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(4,1,2)
    plt.plot(Time,GeneratorSpeedNormal,label='Normal operation')
    plt.plot(Time,GeneratorSpeedFault,label='Blade mass fault operation')
    plt.title('Generator Speed',fontsize=font_size)
    plt.ylabel('RPM',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(4,1,3)
    plt.plot(Time,RotorSpeedNormal,label='Normal operation')
    plt.plot(Time,RotorSpeedFault,label='Blade mass fault operation')
    plt.title('Rotor Speed',fontsize=font_size)
    plt.ylabel('RPM',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.subplot(4,1,4)
    plt.plot(Time,AzimuthAngleNormal,label='Normal operation')
    plt.plot(Time,AzimuthAngleFault,label='Blade mass fault operation')
    plt.title('Rotor Azimuth Angle',fontsize=font_size)
    plt.ylabel('Degrees',fontsize=font_size)
    plt.xlabel('Time (s)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity and '+str(e)+'% blade mass fault at blade 1',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    plt.tight_layout()

    plt.savefig(output_data+'/Quantities.png',dpi = 200)
    plt.close('all')

    ## FFT

    plt.figure()
    figure = plt.gcf()
    figure.set_size_inches(inches_x_FFT,inches_y_FFT)
    plt.subplot(3,1,1)
    RotorPowerNormalFFT = fft(RotorPowerNormal)
    RotorPowerNormalFFT=np.abs(RotorPowerNormalFFT)
    RotorPowerNormalFFT=RotorPowerNormalFFT/(N/2)
    RotorPowerFaultFFT = fft(RotorPowerFault)
    RotorPowerFaultFFT=np.abs(RotorPowerFaultFFT)
    RotorPowerFaultFFT=RotorPowerFaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],RotorPowerNormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],RotorPowerFaultFFT[0:cut],label='Blade mass fault operation FFT')
    plt.title('General quantities FFT\nPower',fontsize=font_size)
    plt.ylabel('kW',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    ymax= max(RotorPowerFaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()

    plt.subplot(3,1,2)
    GeneratorSpeedNormalFFT = fft(GeneratorSpeedNormal)
    GeneratorSpeedNormalFFT=np.abs(GeneratorSpeedNormalFFT)
    GeneratorSpeedNormalFFT=GeneratorSpeedNormalFFT/(N/2)
    GeneratorSpeedFaultFFT = fft(GeneratorSpeedFault)
    GeneratorSpeedFaultFFT=np.abs(GeneratorSpeedFaultFFT)
    GeneratorSpeedFaultFFT=GeneratorSpeedFaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],GeneratorSpeedNormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],GeneratorSpeedFaultFFT[0:cut],label='Blade mass fault operation FFT')
    plt.title('Generator Speed',fontsize=font_size)
    plt.ylabel('RPM',fontsize=font_size)
    plt.legend(fontsize=legend_size,frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='x',labelbottom=False)
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.box(on=None)
    ymax= max(GeneratorSpeedFaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()

    plt.subplot(3,1,3)
    RotorSpeedNormalFFT = fft(RotorSpeedNormal)
    RotorSpeedNormalFFT=np.abs(RotorSpeedNormalFFT)
    RotorSpeedNormalFFT=RotorSpeedNormalFFT/(N/2)
    RotorSpeedFaultFFT = fft(RotorSpeedFault)
    RotorSpeedFaultFFT=np.abs(RotorSpeedFaultFFT)
    RotorSpeedFaultFFT=RotorSpeedFaultFFT/(N/2)
    plt.plot(Freq_mirror[0:cut],RotorSpeedNormalFFT[0:cut],label = 'Normal operation FFT')
    plt.plot(Freq_mirror[0:cut],RotorSpeedFaultFFT[0:cut],label='Blade mass fault operation FFT')
    plt.title('Rotor Speed',fontsize=font_size)
    plt.ylabel('RPM',fontsize=font_size)
    plt.legend(frameon=False,bbox_to_anchor=(legend_positionX,legend_positionY))
    plt.tick_params(axis='y',labelsize = tick_size)
    plt.xlabel('Frequency (Hz)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity and '+str(e)+'% blade mass fault at blade 1',fontsize=font_size)
    plt.box(on=None)
    ymax= max(RotorSpeedFaultFFT[y0:yf])
    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    plt.tight_layout()

    plt.savefig(output_data+'/QuantitiesFFT.png',dpi = 200)

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

    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(e)+'massfault-'+str(n)+'/Collective pitch controller')==False:
        print('Run your turbine with '+str(v)+'m/s wind speed '+str(h)+'hub heigh '+str(t)+'% turbulence intensity with '+str(s)+' seconds of duration first')
    else:
        fault_col= path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User Outputs - Mass Fault/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(e)+'massfault-'+str(n)+'/Collective pitch controller/'
   
    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User Outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/Collective pitch controller')==False:
        print('Run your turbine with '+str(v)+'m/s wind speed '+str(h)+'hub heigh '+str(t)+'% turbulence intensity with '+str(s)+' seconds of duration first')
    else:
        normal_col= path_fast+turbinefast+'-'+str(v)+'ms/Sfunc Outputs - User Outputs/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/Collective pitch controller/'        

    if os.path.exists(fault_col+'Output Data')==False:
        os.mkdir(fault_col+'Output Data')

    output_data = fault_col+'Output Data/'

    standard_normal_col=open(normal_col+out).read().splitlines()
    standard_fault_col= open(fault_col+out_fault).read().splitlines()

    out = out[0:len(out)-4]
    out_fault = out_fault[0:len(out)-4]


    ## NEW OUT COLLECTIVE NORMAL

    normal_noHeader_col = open(output_data+str(v)+'ms-'+str(t)+'ti-'+'NormalnoHeader.out','w')
                            
    i = 0
    for linha in standard_normal_col:
        if i >5:
            normal_noHeader_col.write(linha+'\n')
        else:
            i=i+1
    normal_noHeader_col.close()
    
    normal_noHeader_col = output_data+str(v)+'ms-'+str(t)+'ti-'+'NormalnoHeader.out'
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

    fault_noHeader_col = open(output_data+str(v)+'ms-'+str(t)+'ti-'+str(e)+'MassFaultnoHeader.out','w')
                            
    i = 0
    for linha in standard_fault_col:
        if i >5:
            fault_noHeader_col.write(linha+'\n')
        else:
            i=i+1
    fault_noHeader_col.close()
    
    fault_noHeader_col = output_data+str(v)+'ms-'+str(t)+'ti-'+str(e)+'MassFaultnoHeader.out'
    
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
        plt.plot(Time,fig_normal_col[i],label='Normal Operation - Collective Pitch Controller')
        plt.plot(Time,fig_fault_col[i],label='Fault Operation - Collective Pitch Controller')
        plt.title(output[i+1])
        plt.ylabel(legend[i+1])
        plt.xlabel('Time\nWind speed at '+str(v)+'m/s and '+str(t)+'% turbulence intensity')
        plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
        plt.box(on=None)
        plt.savefig(output_data+output[i+1]+'.png',bbox_inches='tight')
        plt.close('all')
