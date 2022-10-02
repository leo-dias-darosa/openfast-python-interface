import sys
import os
import subprocess
import shutil
import matlab.engine
import fast_nrel as fst
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os,glob,subprocess
from scipy.fftpack import fft, ifft
import random
from random import randrange, uniform

def report(parameters):
    
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

        path_modules=path_modules+'/'
        path_fast = path_fast+'/'
        
        fast_input = open(path_fast+turbinefast).read().splitlines()
        turbinefast = turbinefast[0:len(turbinefast)-4]

        sim_path = path_fast+turbinefast+' - Customized Simulation - Simulink/'
        
        Simulation = 'Customized FAST'

        simulated_file = path_fast+turbinefast+' - Customized Simulation - Simulink/'+turbinefast+'-'+str(v)+'ms/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'.sfunc'
        
        ####################################### Get modules used #######################################
        
        ElastoStatus=''
        BeamdynStatus = ''
        ServoStatus=''
        AeroStatus=''
        HydroStatus=''
        SubStatus=''
        MoorStatus=''
        IceStatus=''
        
        ## Elasto
        Elasto_line = fast_input[12]
        
        for i in Elasto_line:
                if i=='':
                        pass
                elif i=='0':
                        ElastoStatus='Disabled'
                        BeamdynStatus='Disabled'
                        break
                elif i=='1':
                        ElastoStatus='Enabled'
                        BeamdynStatus='Disabled'
                        break
                
                elif i=='2':
                        ElastoStatus='Enabled'
                        BeamdynStatus='Enabled'
                        break
                
        ## Servo
        Servo_line = fast_input[15]

        for i in Servo_line:
                if i=='':
                        pass
                elif i=='0':
                        ServoStatus='Disabled'
                        break
                elif i=='1':
                        ServoStatus='Enabled'
                        break

        ## Aero
        Aero_line = fast_input[14]

        for i in Aero_line:
                if i=='':
                        pass
                elif i=='0':
                        AeroStatus='Disabled'
                        break
                elif i=='1':
                        AeroStatus='Aerodyn v14'
                        break
                elif i=='2':
                        AeroStatus='Aerodyn v15'
                        break

        ## Hydro
        Hydro_line = fast_input[16]

        for i in Hydro_line:
                if i=='':
                        pass
                elif i=='0':
                        HydroStatus='Disabled'
                        break
                elif i=='1':
                        HydroStatus='Enabled'
                        break


        ## Sub
        Sub_line = fast_input[17]

        for i in Sub_line:
                if i=='':
                        pass
                elif i=='0':
                        SubStatus='Disabled'
                        break
                elif i=='1':
                        SubStatus='Enabled'
                        break

        ## Moor
        Moor_line = fast_input[18]

        for i in Moor_line:
                if i=='':
                        pass
                elif i=='0':
                        MoorStatus='Disabled'
                        break
                elif i=='1':
                        MoorStatus='Enabled'
                        break

        ## Ice
        Ice_line = fast_input[19]

        for i in Ice_line:
                if i=='':
                        pass
                elif i=='0':
                        IceStatus='Disabled'
                        break
                elif i=='1':
                        IceStatus='Enabled'
                        break

        ##### Get Elastodyn SUMMARY 
                
        elasto_sum = open(simulated_file+'.ED.SUM').read().splitlines()
        ED_file_str = simulated_file+'ED.SUM'
        ed_str=''
        for i in ED_file_str:
                if i =='/':
                        ed_str=''
                else:
                        ed_str=ed_str+i

        ## DOFS
        
        DOF=0
        DOF_1_status = 'Disabled'
        DOF_2_status = 'Disabled'
        DOF_3_status = 'Disabled'
        DOF_4_status = 'Disabled'
        DOF_5_status = 'Disabled'
        DOF_6_status = 'Disabled'
        DOF_7_status = 'Disabled'
        DOF_8_status = 'Disabled'
        DOF_9_status = 'Disabled'
        DOF_10_status = 'Disabled'
        DOF_11_status = 'Disabled'
        DOF_12_status = 'Disabled'
        DOF_13_status = 'Disabled'
        DOF_14_status = 'Disabled'
        DOF_15_status = 'Disabled'
        DOF_16_status = 'Disabled'
        DOF_17_status = 'Disabled'
        DOF_18_status = 'Disabled'
        DOF_19_status = 'Disabled'
        DOF_20_status = 'Disabled'
        DOF_21_status = 'Disabled'
        DOF_22_status = 'Disabled'
        DOF_23_status = 'Disabled'
        DOF_24_status = 'Disabled'
        
        DOF_1=elasto_sum[8]
        for i in DOF_1:
                if i=='':
                        pass
                elif i=='D':
                        DOF_1_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_1_status = 'Enabled'
                        DOF = DOF+1
                        break
                        
        DOF_2=elasto_sum[9]
        for i in DOF_2:
                if i=='':
                        pass
                elif i=='D':
                        DOF_2_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_2_status = 'Enabled'
                        DOF = DOF+1
                        break
                
        DOF_3=elasto_sum[10]
        for i in DOF_3:
                if i=='':
                        pass
                elif i=='D':
                        DOF_3_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_3_status = 'Enabled'
                        DOF = DOF+1
                        break
        
        DOF_4=elasto_sum[11]
        for i in DOF_4:
                if i=='':
                        pass
                elif i=='D':
                        DOF_4_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_4_status = 'Enabled'
                        DOF = DOF+1
                        break
                
        DOF_5=elasto_sum[12]
        for i in DOF_5:
                if i=='':
                        pass
                elif i=='D':
                        DOF_5_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_5_status = 'Enabled'
                        DOF = DOF+1
                        break
                
        DOF_6=elasto_sum[13]
        for i in DOF_1:
                if i=='':
                        pass
                elif i=='D':
                        DOF_6_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_6_status = 'Enabled'
                        DOF = DOF+1
                        break
                
        DOF_7=elasto_sum[14]
        for i in DOF_7:
                if i=='':
                        pass
                elif i=='D':
                        DOF_7_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_7_status = 'Enabled'
                        DOF = DOF+1
                        break
                
        DOF_8=elasto_sum[15]
        for i in DOF_8:
                if i=='':
                        pass
                elif i=='D':
                        DOF_8_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_8_status = 'Enabled'
                        DOF = DOF+1
                        break
                
        DOF_9=elasto_sum[16]
        for i in DOF_9:
                if i=='':
                        pass
                elif i=='D':
                        DOF_9_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_9_status = 'Enabled'
                        DOF = DOF+1
                        break
                
        DOF_10=elasto_sum[17]
        for i in DOF_10:
                if i=='':
                        pass
                elif i=='D':
                        DOF_10_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_10_status = 'Enabled'
                        DOF = DOF+1
                        break
                
        DOF_11=elasto_sum[18]
        for i in DOF_11:
                if i=='':
                        pass
                elif i=='D':
                        DOF_11_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_11_status = 'Enabled'
                        DOF = DOF+1
                        break
                
        DOF_12=elasto_sum[19]
        for i in DOF_12:
                if i=='':
                        pass
                elif i=='D':
                        DOF_12_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_12_status = 'Enabled'
                        DOF = DOF+1
                        break
                
        DOF_13=elasto_sum[20]
        for i in DOF_13:
                if i=='':
                        pass
                elif i=='D':
                        DOF_13_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_13_status = 'Enabled'
                        DOF = DOF+1
                        break
                
        DOF_14=elasto_sum[21]
        for i in DOF_14:
                if i=='':
                        pass
                elif i=='D':
                        DOF_14_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_14_status = 'Enabled'
                        DOF = DOF+1
                        break
                
        DOF_15=elasto_sum[22]
        for i in DOF_15:
                if i=='':
                        pass
                elif i=='D':
                        DOF_15_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_15_status = 'Enabled'
                        DOF = DOF+1
                        break
                
        DOF_16=elasto_sum[23]
        for i in DOF_16:
                if i=='':
                        pass
                elif i=='D':
                        DOF_16_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_16_status = 'Enabled'
                        DOF = DOF+1
                        break
                
        DOF_17=elasto_sum[24]
        for i in DOF_17:
                if i=='':
                        pass
                elif i=='D':
                        DOF_17_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_17_status = 'Enabled'
                        DOF = DOF+1
                        break
                
        DOF_18=elasto_sum[25]
        for i in DOF_18:
                if i=='':
                        pass
                elif i=='D':
                        DOF_18_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_18_status = 'Enabled'
                        DOF = DOF+1
                        break
                
        DOF_19=elasto_sum[26]
        for i in DOF_19:
                if i=='':
                        pass
                elif i=='D':
                        DOF_19_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_19_status = 'Enabled'
                        DOF = DOF+1
                        break
                
        DOF_20=elasto_sum[27]
        for i in DOF_20:
                if i=='':
                        pass
                elif i=='D':
                        DOF_20_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_20_status = 'Enabled'
                        DOF = DOF+1
                        break
                
        DOF_21=elasto_sum[28]
        for i in DOF_21:
                if i=='':
                        pass
                elif i=='D':
                        DOF_21_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_21_status = 'Enabled'
                        DOF = DOF+1
                        break
                
        DOF_22=elasto_sum[29]
        for i in DOF_22:
                if i=='':
                        pass
                elif i=='D':
                        DOF_22_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_22_status = 'Enabled'
                        DOF = DOF+1
                        break
                
        DOF_23=elasto_sum[30]
        for i in DOF_23:
                if i=='':
                        pass
                elif i=='D':
                        DOF_23_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_23_status = 'Enabled'
                        DOF = DOF+1
                        break
                
        DOF_24=elasto_sum[31]
        for i in DOF_24:
                if i=='':
                        pass
                elif i=='D':
                        DOF_24_status = 'Disabled'
                        break
                elif i=='E':
                        DOF_24_status = 'Enabled'
                        DOF = DOF+1
                        break

        ## Turbine properties
        # hub height
        
        hub_height_line = elasto_sum[41]

        hub_height_list = hub_height_line.split()
        hub_height = hub_height_list[2]

        # Rotor mass

        Rotor_mass_line = elasto_sum[48]

        Rotor_mass_list = Rotor_mass_line.split()
        Rotor_mass = Rotor_mass_list[3]
        
        # Rotor inertia

        Rotor_inertia_line = elasto_sum[49]

        Rotor_inertia_list = Rotor_inertia_line.split()
        Rotor_inertia = Rotor_inertia_list[3]

        # Tower-top mass

        Tower_top_mass_line = elasto_sum[60]

        Tower_top_mass_list = Tower_top_mass_line.split()
        Tower_top_mass = Tower_top_mass_list[3]

        ## Tower mass
                        
        Tower_mass_line = elasto_sum[61]

        Tower_mass_list = Tower_mass_line.split()
        Tower_mass = Tower_mass_list[3]

        ## Platform mass
        
        Platform_mass_line=elasto_sum[62]

        Platform_mass_list = Platform_mass_line.split()
        Platform_mass = Platform_mass_list[3]
        
        ## Mass with platform
        
        mass_with_plt_line=elasto_sum[63]

        mass_with_plt_list = mass_with_plt_line.split()
        mass_with_plt = mass_with_plt_list[4]

        ## Blades mass
                        
        blade_mass_line = elasto_sum[52]

        blade_mass = blade_mass_line.split()
        blade_1_mass = blade_mass[2]
        blade_2_mass = blade_mass[3]
        blade_3_mass = blade_mass[4]

        ## First mass moment

        blade_first_mass_moment_line = elasto_sum[53]

        blade_first_mass_moment_list = blade_first_mass_moment_line.split()
        blade_1_first_mass_moment_= blade_first_mass_moment_list[4]
        blade_2_first_mass_moment_= blade_first_mass_moment_list[5]
        blade_3_first_mass_moment_= blade_first_mass_moment_list[6]

        ## Second mass moment

        blade_second_mass_moment_line = elasto_sum[54]
        
        blade_second_mass_moment_list = blade_second_mass_moment_line.split()
        blade_1_second_mass_moment_= blade_second_mass_moment_list[4]
        blade_2_second_mass_moment_= blade_second_mass_moment_list[5]
        blade_3_second_mass_moment_= blade_second_mass_moment_list[6]

        ## Center of mass
        Blade_cm_line = elasto_sum[55]

        Blade_cm_list=Blade_cm_line.split()
        Blade_1_cm=Blade_cm_list[4]
        Blade_2_cm=Blade_cm_list[5]
        Blade_3_cm=Blade_cm_list[6]

#################################################################################################  AERODYNAMIC SUMMARY ################################################################################################

        aero_sum = open(simulated_file+'.AD.SUM').read().splitlines()
        AD_file_str = simulated_file+'AD.SUM'
        Ad_str=''
        for i in AD_file_str:
                if i =='/':
                        Ad_str=''
                else:
                        Ad_str=Ad_str+i

        aero_file = open(path_fast+turbinefast+' - Customized Simulation - Simulink/'+turbinefast+'-'+str(v)+'ms/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/Aero.dat').read().splitlines()

        air_density_line=aero_file[12].split()
        air_density=air_density_line[0]

####################################################################################################### GET DATA #####################################################################################################
        
        ## Lists
        
        # Min
        
        flap1min=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        flap2min=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        flap3min=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        edge1min=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        edge2min=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        edge3min=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        tiltmin=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        yawmin=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        Rtorquemin=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        TwrBsNmin=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        TwrBsLmin=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        TwrTqmin=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        pitchactuationload1min=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        pitchactuationload2min=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        pitchactuationload3min=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        TwrTopAccNormalmin=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        TwrTopAccLatmin=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        TwrTopMomentNormalmin=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        TwrTopMomentLateralmin=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        
        Powermin=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        GenSpeedmin=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        RotSpeedmin=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        
        # Mean

        flap1mean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        flap2mean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        flap3mean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        edge1mean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        edge2mean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        edge3mean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        tiltmean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        yawmean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        Rtorquemean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        TwrBsNmean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        TwrBsLmean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        TwrTqmean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        pitchactuationload1mean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        pitchactuationload2mean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        pitchactuationload3mean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        TwrTopAccNormalmean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        TwrTopAccLatmean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        TwrTopMomentNormalmean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        TwrTopMomentLateralmean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        
        Powermean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        GenSpeedmean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        RotSpeedmean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        # Max

        flap1max=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        flap2max=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        flap3max=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        edge1max=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        edge2max=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        edge3max=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        tiltmax=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        yawmax=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        Rtorquemax=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        TwrBsNmax=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        TwrBsLmax=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        TwrTqmax=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        pitchactuationload1max=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        pitchactuationload2max=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        pitchactuationload3max=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        TwrTopAccNormalmax=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        TwrTopAccLatmax=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        TwrTopMomentNormalmax=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        TwrTopMomentLateralmax=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        Powermax=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        GenSpeedmax=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        RotSpeedmax=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        # Std.dev

        flap1dev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        flap2dev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        flap3dev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        
        edge1dev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        edge2dev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        edge3dev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        tiltdev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        yawdev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        Rtorquedev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        TwrBsNdev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        TwrBsLdev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        TwrTqdev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        pitchactuationload1dev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        pitchactuationload2dev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        pitchactuationload3dev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        TwrTopAccNormaldev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        TwrTopAccLatdev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        TwrTopMomentNormaldev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        TwrTopMomentLateraldev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        
        Powerdev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        GenSpeeddev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        RotSpeeddev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        mppt_speeds=[]
        speed_control_speeds=[]

        wind_speed=np.arange(3.0,25.0,0.5)
        
        for v in wind_speed:
                Index = int(v)-3
                for turb in range(t,t+1):
                        if os.path.exists(path_fast+turbinefast+' - Customized Simulation - Simulink/'+turbinefast+'-'+str(v)+'ms/'+turbinefast+'-'+str(v)+'ms-'+str(turb)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/'+turbinefast+'-'+str(v)+'ms-'+str(turb)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'.sfunc.out')==False:
                                pass
                        else:
                                read_path = path_fast+turbinefast+' - Customized Simulation - Simulink/'+turbinefast+'-'+str(v)+'ms/'+turbinefast+'-'+str(v)+'ms-'+str(turb)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/'

                                out_file = read_path+turbinefast+'-'+str(v)+'ms-'+str(turb)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'.sfunc.out'

                                out_file_noHeaderStr = out_file[0:len(out_file)-4]+"noHeader.out"
                                out_file_csv = out_file[0:len(out_file)-4]+"noHeader.csv"

                                dataIndex =  pd.read_csv(out_file_csv)
                                data_normal_col = pd.read_csv(out_file_csv,header=None)
                        
                        ## Flapwise bending moment

                                BladeRootFlapWiseM1Index = dataIndex.columns.get_loc("RootMxb1")
                                BladeRootFlapWiseM1Normal = data_normal_col.iloc[2:,BladeRootFlapWiseM1Index]
                                BladeRootFlapWiseM1Normal = [float(x) for x in BladeRootFlapWiseM1Normal]

                                BladeRootFlapWiseM2Index = dataIndex.columns.get_loc("RootMxb2")
                                BladeRootFlapWiseM2Normal = data_normal_col.iloc[2:,BladeRootFlapWiseM2Index]
                                BladeRootFlapWiseM2Normal = [float(x) for x in BladeRootFlapWiseM2Normal]

                                BladeRootFlapWiseM3Index = dataIndex.columns.get_loc("RootMxb3")
                                BladeRootFlapWiseM3Normal = data_normal_col.iloc[2:,BladeRootFlapWiseM3Index]
                                BladeRootFlapWiseM3Normal = [float(x) for x in BladeRootFlapWiseM3Normal]

                                flap1min[Index].append(round(np.min(BladeRootFlapWiseM1Normal),3))
                                flap1mean[Index].append(round(np.mean(BladeRootFlapWiseM1Normal),3))
                                flap1max[Index].append(round(np.max(BladeRootFlapWiseM1Normal),3))
                                flap1dev[Index].append(np.std(BladeRootFlapWiseM1Normal))

                                flap2min[Index].append(round(np.min(BladeRootFlapWiseM2Normal),3))
                                flap2mean[Index].append(round(np.mean(BladeRootFlapWiseM2Normal),3))
                                flap2max[Index].append(np.max(BladeRootFlapWiseM2Normal))
                                flap2dev[Index].append(np.std(BladeRootFlapWiseM2Normal))

                                flap3min[Index].append(round(np.min(BladeRootFlapWiseM3Normal),3))
                                flap3mean[Index].append(round(np.mean(BladeRootFlapWiseM3Normal),3))
                                flap3max[Index].append(round(np.max(BladeRootFlapWiseM3Normal),3))
                                flap3dev[Index].append(np.std(BladeRootFlapWiseM3Normal))

                        ## Edgwise bending moment

                                BladeRootEdgeWiseM1Index = dataIndex.columns.get_loc("RootMyb1")
                                BladeRootEdgeWiseM1Normal = data_normal_col.iloc[2:,BladeRootEdgeWiseM1Index]
                                BladeRootEdgeWiseM1Normal = [float(x) for x in BladeRootEdgeWiseM1Normal]

                                BladeRootEdgeWiseM2Index = dataIndex.columns.get_loc("RootMyb2")
                                BladeRootEdgeWiseM2Normal = data_normal_col.iloc[2:,BladeRootEdgeWiseM2Index]
                                BladeRootEdgeWiseM2Normal = [float(x) for x in BladeRootEdgeWiseM2Normal]

                                BladeRootEdgeWiseM3Index = dataIndex.columns.get_loc("RootMyb3")
                                BladeRootEdgeWiseM3Normal = data_normal_col.iloc[2:,BladeRootEdgeWiseM3Index]
                                BladeRootEdgeWiseM3Normal = [float(x) for x in BladeRootEdgeWiseM3Normal]

                                edge1min[Index].append(round(np.min(BladeRootEdgeWiseM1Normal),3))
                                edge1mean[Index].append(round(np.mean(BladeRootEdgeWiseM1Normal),3))
                                edge1max[Index].append(round(np.max(BladeRootEdgeWiseM1Normal),3))
                                edge1dev[Index].append(np.std(BladeRootEdgeWiseM1Normal))

                                edge2min[Index].append(round(np.min(BladeRootEdgeWiseM2Normal),3))
                                edge2mean[Index].append(round(np.mean(BladeRootEdgeWiseM2Normal),3))
                                edge2max[Index].append(round(np.max(BladeRootEdgeWiseM2Normal),3))
                                edge2dev[Index].append(np.std(BladeRootEdgeWiseM2Normal))

                                edge3min[Index].append(round(np.min(BladeRootEdgeWiseM3Normal),3))
                                edge3mean[Index].append(round(np.mean(BladeRootEdgeWiseM3Normal),3))
                                edge3max[Index].append(round(np.max(BladeRootEdgeWiseM3Normal),3))
                                edge3dev[Index].append(np.std(BladeRootEdgeWiseM3Normal))

                        ## Rotor moments

                                RotorTiltMomentIndex = dataIndex.columns.get_loc("LSSTipMys")
                                RotorTiltMomentNormal = data_normal_col.iloc[2:,RotorTiltMomentIndex]
                                RotorTiltMomentNormal = [float(x) for x in RotorTiltMomentNormal]
                        
                                RotorYawMomentIndex = dataIndex.columns.get_loc("LssTipMzs")
                                RotorYawMomentNormal = data_normal_col.iloc[2:,RotorYawMomentIndex]
                                RotorYawMomentNormal = [float(x) for x in RotorYawMomentNormal]

                                RotorTorqueIndex = dataIndex.columns.get_loc("LSShftMxa")
                                RotorTorqueNormal = data_normal_col.iloc[2:,RotorTorqueIndex]
                                RotorTorqueNormal = [float(x) for x in RotorTorqueNormal]

                                tiltmin[Index].append(round(np.min(RotorTiltMomentNormal),3))
                                tiltmean[Index].append(round(np.mean(RotorTiltMomentNormal),3))
                                tiltmax[Index].append(round(np.max(RotorTiltMomentNormal),3))
                                tiltdev[Index].append(np.std(RotorTiltMomentNormal))

                                yawmin[Index].append(round(np.min(RotorYawMomentNormal),3))
                                yawmean[Index].append(round(np.mean(RotorYawMomentNormal),3))
                                yawmax[Index].append(round(np.max(RotorYawMomentNormal),3))
                                yawdev[Index].append(np.std(RotorYawMomentNormal))

                                Rtorquemin[Index].append(round(np.min(RotorTorqueNormal),3))
                                Rtorquemean[Index].append(round(np.mean(RotorTorqueNormal),3))
                                Rtorquemax[Index].append(round(np.max(RotorTorqueNormal),3))
                                Rtorquedev[Index].append(np.std(RotorTorqueNormal))

                        ## Tower moments

                                TowerBaseNormalIndex = dataIndex.columns.get_loc("TwrBsMyt")
                                TowerBaseNormalNormal = data_normal_col.iloc[2:,TowerBaseNormalIndex]
                                TowerBaseNormalNormal = [float(x) for x in TowerBaseNormalNormal]

                                TowerBaseLateralIndex = dataIndex.columns.get_loc("TwrBsMxt")
                                TowerBaseLateralNormal = data_normal_col.iloc[2:,TowerBaseLateralIndex]
                                TowerBaseLateralNormal = [float(x) for x in TowerBaseLateralNormal]

                                TowerTorqueIndex = dataIndex.columns.get_loc("TwrBsMxt")
                                TowerTorqueNormal = data_normal_col.iloc[2:,TowerTorqueIndex]
                                TowerTorqueNormal = [float(x) for x in TowerTorqueNormal]

                                TwrBsNmin[Index].append(round(np.min(TowerBaseNormalNormal),3))
                                TwrBsNmean[Index].append(round(np.mean(TowerBaseNormalNormal),3))
                                TwrBsNmax[Index].append(round(np.max(TowerBaseNormalNormal),3))
                                TwrBsNdev[Index].append(np.std(TowerBaseNormalNormal))

                                TwrBsLmin[Index].append(round(np.min(TowerBaseLateralNormal),3))
                                TwrBsLmean[Index].append(round(np.mean(TowerBaseLateralNormal),3))
                                TwrBsLmax[Index].append(round(np.max(TowerBaseLateralNormal),3))
                                TwrBsLdev[Index].append(np.std(TowerBaseLateralNormal))

                                TwrTqmin[Index].append(round(np.min(TowerTorqueNormal),3))
                                TwrTqmean[Index].append(round(np.mean(TowerTorqueNormal),3))
                                TwrTqmax[Index].append(round(np.max(TowerTorqueNormal),3))
                                TwrTqdev[Index].append(np.std(TowerTorqueNormal))

                        ## Pitch actuation loads

                                PitchActuationoLoad1Index = dataIndex.columns.get_loc("RootMzc1")
                                PitchActuationoLoad1Normal = data_normal_col.iloc[2:,PitchActuationoLoad1Index]
                                PitchActuationoLoad1Normal = [float(x) for x in PitchActuationoLoad1Normal]

                                PitchActuationoLoad2Index = dataIndex.columns.get_loc("RootMzc2")
                                PitchActuationoLoad2Normal = data_normal_col.iloc[2:,PitchActuationoLoad2Index]
                                PitchActuationoLoad2Normal = [float(x) for x in PitchActuationoLoad2Normal]

                                PitchActuationoLoad3Index = dataIndex.columns.get_loc("RootMzc3")
                                PitchActuationoLoad3Normal = data_normal_col.iloc[2:,PitchActuationoLoad3Index]
                                PitchActuationoLoad3Normal = [float(x) for x in PitchActuationoLoad3Normal]

                                pitchactuationload1min[Index].append(round(np.min(PitchActuationoLoad1Normal),3))
                                pitchactuationload1mean[Index].append(round(np.mean(PitchActuationoLoad1Normal),3))
                                pitchactuationload1max[Index].append(round(np.max(PitchActuationoLoad1Normal),3))
                                pitchactuationload1dev[Index].append(np.std(PitchActuationoLoad1Normal))

                                pitchactuationload2min[Index].append(round(np.min(PitchActuationoLoad2Normal),3))
                                pitchactuationload2mean[Index].append(round(np.mean(PitchActuationoLoad2Normal),3))
                                pitchactuationload2max[Index].append(round(np.max(PitchActuationoLoad2Normal),3))
                                pitchactuationload2dev[Index].append(np.std(PitchActuationoLoad2Normal))

                                pitchactuationload3min[Index].append(round(np.min(PitchActuationoLoad3Normal),3))
                                pitchactuationload3mean[Index].append(round(np.mean(PitchActuationoLoad3Normal),3))
                                pitchactuationload3max[Index].append(round(np.max(PitchActuationoLoad3Normal),3))
                                pitchactuationload3dev[Index].append(np.std(PitchActuationoLoad3Normal))

                        ## Tower top accelerations
                                
                                TowerTopAccelerationNormalIndex = dataIndex.columns.get_loc("YawBrTAxp")
                                TowerTopAccelerationNormalNormal = data_normal_col.iloc[2:,TowerTopAccelerationNormalIndex]
                                TowerTopAccelerationNormalNormal = [float(x) for x in TowerTopAccelerationNormalNormal]

                                TowerTopAccelerationLaterallIndex = dataIndex.columns.get_loc("YawBrTAyp")
                                TowerTopAccelerationLateralNormal = data_normal_col.iloc[2:,TowerTopAccelerationLaterallIndex]
                                TowerTopAccelerationLateralNormal = [float(x) for x in TowerTopAccelerationLateralNormal]

                                TwrTopAccNormalmin[Index].append(round(np.min(TowerTopAccelerationNormalNormal),3))
                                TwrTopAccNormalmean[Index].append(round(np.mean(TowerTopAccelerationNormalNormal),3))
                                TwrTopAccNormalmax[Index].append(round(np.max(TowerTopAccelerationNormalNormal),3))
                                TwrTopAccNormaldev[Index].append(np.std(TowerTopAccelerationNormalNormal))

                                TwrTopAccLatmin[Index].append(round(np.min(TowerTopAccelerationLateralNormal),3))
                                TwrTopAccLatmean[Index].append(round(np.mean(TowerTopAccelerationLateralNormal),3))
                                TwrTopAccLatmax[Index].append(round(np.max(TowerTopAccelerationLateralNormal),3))
                                TwrTopAccLatdev[Index].append(np.std(TowerTopAccelerationLateralNormal))

                        ## Tower top moments
                                
                                TowerTopNormalIndex = dataIndex.columns.get_loc("YawBrMyp")
                                TowerTopNormalNormal = data_normal_col.iloc[2:,TowerTopNormalIndex]
                                TowerTopNormalNormal = [float(x) for x in TowerTopNormalNormal]

                                TowerTopLateralIndex = dataIndex.columns.get_loc("YawBrMxp")
                                TowerTopLateralNormal = data_normal_col.iloc[2:,TowerTopLateralIndex]
                                TowerTopLateralNormal = [float(x) for x in TowerTopLateralNormal]

                                TwrTopMomentNormalmin[Index].append(round(np.min(TowerTopNormalNormal),3))
                                TwrTopMomentNormalmean[Index].append(round(np.mean(TowerTopNormalNormal),3))
                                TwrTopMomentNormalmax[Index].append(round(np.max(TowerTopNormalNormal),3))
                                TwrTopMomentNormaldev[Index].append(np.std(TowerTopNormalNormal))

                                TwrTopMomentLateralmin[Index].append(round(np.min(TowerTopLateralNormal),3))
                                TwrTopMomentLateralmean[Index].append(round(np.mean(TowerTopLateralNormal),3))
                                TwrTopMomentLateralmax[Index].append(round(np.max(TowerTopLateralNormal),3))
                                TwrTopMomentLateraldev[Index].append(np.std(TowerTopLateralNormal))

                        ## Other quantities
                                
                                RotorPowerIndex = dataIndex.columns.get_loc("GenPwr")
                                RotorPowerNormal = data_normal_col.iloc[2:,RotorPowerIndex]
                                RotorPowerNormal = [float(x) for x in RotorPowerNormal]

                                GeneratorSpeedIndex = dataIndex.columns.get_loc("GenSpeed")
                                GeneratorSpeedNormal = data_normal_col.iloc[2:,GeneratorSpeedIndex]
                                GeneratorSpeedNormal = [float(x) for x in GeneratorSpeedNormal]

                                RotorSpeedIndex = dataIndex.columns.get_loc("RotSpeed")
                                RotorSpeedNormal = data_normal_col.iloc[2:,RotorSpeedIndex]
                                RotorSpeedNormal = [float(x) for x in RotorSpeedNormal]

                                Powermin[Index].append(round(np.min(RotorPowerNormal),3))
                                Powermean[Index].append(round(np.mean(RotorPowerNormal),3))
                                Powermax[Index].append(round(np.max(RotorPowerNormal),3))
                                Powerdev[Index].append(np.std(RotorPowerNormal))

                                GenSpeedmin[Index].append(round(np.min(GeneratorSpeedNormal),3))
                                GenSpeedmean[Index].append(round(np.mean(GeneratorSpeedNormal),3))
                                GenSpeedmax[Index].append(round(np.max(GeneratorSpeedNormal),3))
                                GenSpeeddev[Index].append(np.std(GeneratorSpeedNormal))

                                RotSpeedmin[Index].append(round(np.min(RotorSpeedNormal),3))
                                RotSpeedmean[Index].append(round(np.mean(RotorSpeedNormal),3))
                                RotSpeedmax[Index].append(round(np.max(RotorSpeedNormal),3))
                                RotSpeeddev[Index].append(np.std(RotorSpeedNormal))

                        ## Blade pitch angle


                                Blade1PitchAngleIndex = dataIndex.columns.get_loc("BldPitch1")
                                Blade1PitchAngle = data_normal_col.iloc[2:,Blade1PitchAngleIndex]
                                Blade1PitchAngle = [float(x) for x in Blade1PitchAngle]

                                Blade2PitchAngleIndex = dataIndex.columns.get_loc("BldPitch2")
                                Blade2PitchAngle = data_normal_col.iloc[2:,Blade2PitchAngleIndex]
                                Blade2PitchAngle = [float(x) for x in Blade2PitchAngle]

                                Blade3PitchAngleIndex = dataIndex.columns.get_loc("BldPitch3")
                                Blade3PitchAngle = data_normal_col.iloc[2:,Blade3PitchAngleIndex]
                                Blade3PitchAngle = [float(x) for x in Blade3PitchAngle]

                                if (np.mean(Blade1PitchAngle) or np.mean(Blade2PitchAngle) or np.mean(Blade3PitchAngle))<3:
                                        mppt_speeds.append(v)
                                elif (np.mean(Blade1PitchAngle) or np.mean(Blade2PitchAngle) or np.mean(Blade3PitchAngle))>5 and ((np.mean(Blade1PitchAngle) or np.mean(Blade2PitchAngle) or np.mean(Blade3PitchAngle))<80):
                                        speed_control_speeds.append(v)
                                          
        ## FOR PLOTTING


        mppt_plot = random.choice(mppt_speeds)
        speed_control_plot = random.choice(speed_control_speeds)

        mppt_folder = path_fast+turbinefast+' - Customized Simulation - Simulink/'+turbinefast+'-'+str(mppt_plot)+'ms/'+turbinefast+'-'+str(mppt_plot)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/Output Data/'
        speed_control_folder = path_fast+turbinefast+' - Customized Simulation - Simulink/'+turbinefast+'-'+str(speed_control_plot)+'ms/'+turbinefast+'-'+str(speed_control_plot)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/Output Data/'

        ## For number of files
        
        number_of_files = []
        for i in range(len(flap1min)):
                number_of_files.append(len(flap1min[i]))
        
        ## Min
                                          
        for i in range(len(flap1min)):
                if not flap1min[i]:
                        flap1min[i]='-'
                else:
                        flap1min[i]=round(np.min(flap1min[i]),3)
                        
        for i in range(len(flap2min)):
                if not flap2min[i]:
                        flap2min[i]='-'
                else:
                        flap2min[i]=round(np.min(flap2min[i]),3)
                        
        for i in range(len(flap3min)):
                if not flap3min[i]:
                        flap3min[i]='-'
                else:
                        flap3min[i]=round(np.min(flap3min[i]),3)

        for i in range(len(edge1min)):
                if not edge1min[i]:
                        edge1min[i]='-'
                else:
                        edge1min[i]=round(np.min(edge1min[i]),3)
                        
        for i in range(len(edge2min)):
                if not edge2min[i]:
                        edge2min[i]='-'
                else:
                        edge2min[i]=round(np.min(edge2min[i]),3)
                        
        for i in range(len(edge3min)):
                if not edge3min[i]:
                        edge3min[i]='-'
                else:
                        edge3min[i]=round(np.min(edge3min[i]),3)

        for i in range(len(tiltmin)):
                if not tiltmin[i]:
                        tiltmin[i]='-'
                else:
                        tiltmin[i]=round(np.min(tiltmin[i]),3)
                        
        for i in range(len(yawmin)):
                if not yawmin[i]:
                        yawmin[i]='-'
                else:
                        yawmin[i]=round(np.min(yawmin[i]),3)
                        
        for i in range(len(Rtorquemin)):
                if not Rtorquemin[i]:
                        Rtorquemin[i]='-'
                else:
                        Rtorquemin[i]=round(np.min(Rtorquemin[i]),3)

        for i in range(len(TwrBsNmin)):
                if not TwrBsNmin[i]:
                        TwrBsNmin[i]='-'
                else:
                        TwrBsNmin[i]=round(np.min(TwrBsNmin[i]),3)
                        
        for i in range(len(TwrBsLmin)):
                if not TwrBsLmin[i]:
                        TwrBsLmin[i]='-'
                else:
                        TwrBsLmin[i]=round(np.min(TwrBsLmin[i]),3)
                        
        for i in range(len(TwrTqmin)):
                if not TwrTqmin[i]:
                        TwrTqmin[i]='-'
                else:
                        TwrTqmin[i]=round(np.min(TwrTqmin[i]),3)

        for i in range(len(pitchactuationload1min)):
                if not pitchactuationload1min[i]:
                        pitchactuationload1min[i]='-'
                else:
                        pitchactuationload1min[i]=round(np.min(pitchactuationload1min[i]),3)
                        
        for i in range(len(pitchactuationload2min)):
                if not pitchactuationload2min[i]:
                        pitchactuationload2min[i]='-'
                else:
                        pitchactuationload2min[i]=round(np.min(pitchactuationload2min[i]),3)

        for i in range(len(pitchactuationload3min)):
                if not pitchactuationload3min[i]:
                        pitchactuationload3min[i]='-'
                else:
                        pitchactuationload3min[i]=round(np.min(pitchactuationload3min[i]),3)

        for i in range(len(TwrTopAccNormalmin)):
                if not TwrTopAccNormalmin[i]:
                        TwrTopAccNormalmin[i]='-'
                else:
                        TwrTopAccNormalmin[i]=round(np.min(TwrTopAccNormalmin[i]),3)

        for i in range(len(TwrTopAccLatmin)):
                if not TwrTopAccLatmin[i]:
                        TwrTopAccLatmin[i]='-'
                else:
                        TwrTopAccLatmin[i]=round(np.min(TwrTopAccLatmin[i]),3)

        for i in range(len(TwrTopMomentNormalmin)):
                if not TwrTopMomentNormalmin[i]:
                        TwrTopMomentNormalmin[i]='-'
                else:
                        TwrTopMomentNormalmin[i]=round(np.min(TwrTopMomentNormalmin[i]),3)

        for i in range(len(TwrTopMomentLateralmin)):
                if not TwrTopMomentLateralmin[i]:
                        TwrTopMomentLateralmin[i]='-'
                else:
                        TwrTopMomentLateralmin[i]=round(np.min(TwrTopMomentLateralmin[i]),3)

        for i in range(len(Powermin)):
                if not Powermin[i]:
                        Powermin[i]='-'
                else:
                        Powermin[i]=round(np.min(Powermin[i]),3)

        for i in range(len(GenSpeedmin)):
                if not GenSpeedmin[i]:
                        GenSpeedmin[i]='-'
                else:
                        GenSpeedmin[i]=round(np.min(GenSpeedmin[i]),3)

        for i in range(len(RotSpeedmin)):
                if not RotSpeedmin[i]:
                        RotSpeedmin[i]='-'
                else:
                        RotSpeedmin[i]=round(np.min(RotSpeedmin[i]),3)
                                          
        ## Mean

        for i in range(len(flap1mean)):
                if not flap1mean[i]:
                        flap1mean[i]='-'
                else:
                        flap1mean[i]=round(np.mean(flap1mean[i]),3)
                        
        for i in range(len(flap2mean)):
                if not flap2mean[i]:
                        flap2mean[i]='-'
                else:
                        flap2mean[i]=round(np.mean(flap2mean[i]),3)
                        
        for i in range(len(flap3mean)):
                if not flap3mean[i]:
                        flap3mean[i]='-'
                else:
                        flap3mean[i]=round(np.mean(flap3mean[i]),3)

        for i in range(len(edge1mean)):
                if not edge1mean[i]:
                        edge1mean[i]='-'
                else:
                        edge1mean[i]=round(np.mean(edge1mean[i]),3)
                        
        for i in range(len(edge2mean)):
                if not edge2mean[i]:
                        edge2mean[i]='-'
                else:
                        edge2mean[i]=round(np.mean(edge2mean[i]),3)
                        
        for i in range(len(edge3mean)):
                if not edge3mean[i]:
                        edge3mean[i]='-'
                else:
                        edge3mean[i]=round(np.mean(edge3mean[i]),3)

        for i in range(len(tiltmean)):
                if not tiltmean[i]:
                        tiltmean[i]='-'
                else:
                        tiltmean[i]=round(np.mean(tiltmean[i]),3)
                        
        for i in range(len(yawmean)):
                if not yawmean[i]:
                        yawmean[i]='-'
                else:
                        yawmean[i]=round(np.mean(yawmean[i]),3)
                        
        for i in range(len(Rtorquemean)):
                if not Rtorquemean[i]:
                        Rtorquemean[i]='-'
                else:
                        Rtorquemean[i]=round(np.mean(Rtorquemean[i]),3)

        for i in range(len(TwrBsNmean)):
                if not TwrBsNmean[i]:
                        TwrBsNmean[i]='-'
                else:
                        TwrBsNmean[i]=round(np.mean(TwrBsNmean[i]),3)
                        
        for i in range(len(TwrBsLmean)):
                if not TwrBsLmean[i]:
                        TwrBsLmean[i]='-'
                else:
                        TwrBsLmean[i]=round(np.mean(TwrBsLmean[i]),3)
                        
        for i in range(len(TwrTqmean)):
                if not TwrTqmean[i]:
                        TwrTqmean[i]='-'
                else:
                        TwrTqmean[i]=round(np.mean(TwrTqmean[i]),3)
                        
        for i in range(len(pitchactuationload1mean)):
                if not pitchactuationload1mean[i]:
                        pitchactuationload1mean[i]='-'
                else:
                        pitchactuationload1mean[i]=round(np.mean(pitchactuationload1mean[i]),3)
                        
        for i in range(len(pitchactuationload2mean)):
                if not pitchactuationload2mean[i]:
                        pitchactuationload2mean[i]='-'
                else:
                        pitchactuationload2mean[i]=round(np.mean(pitchactuationload2mean[i]),3)

        for i in range(len(pitchactuationload3mean)):
                if not pitchactuationload3mean[i]:
                        pitchactuationload3mean[i]='-'
                else:
                        pitchactuationload3mean[i]=round(np.mean(pitchactuationload3mean[i]),3)

        for i in range(len(TwrTopAccNormalmean)):
                if not TwrTopAccNormalmean[i]:
                        TwrTopAccNormalmean[i]='-'
                else:
                        TwrTopAccNormalmean[i]=round(np.mean(TwrTopAccNormalmean[i]),3)

        for i in range(len(TwrTopAccLatmean)):
                if not TwrTopAccLatmean[i]:
                        TwrTopAccLatmean[i]='-'
                else:
                        TwrTopAccLatmean[i]=round(np.mean(TwrTopAccLatmean[i]),3)

        for i in range(len(TwrTopMomentNormalmean)):
                if not TwrTopMomentNormalmean[i]:
                        TwrTopMomentNormalmean[i]='-'
                else:
                        TwrTopMomentNormalmean[i]=round(np.mean(TwrTopMomentNormalmean[i]),3)

        for i in range(len(TwrTopMomentLateralmean)):
                if not TwrTopMomentLateralmean[i]:
                        TwrTopMomentLateralmean[i]='-'
                else:
                        TwrTopMomentLateralmean[i]=round(np.mean(TwrTopMomentLateralmean[i]),3)

        for i in range(len(Powermean)):
                if not Powermean[i]:
                        Powermean[i]='-'
                else:
                        Powermean[i]=round(np.mean(Powermean[i]),3)

        for i in range(len(GenSpeedmean)):
                if not GenSpeedmean[i]:
                        GenSpeedmean[i]='-'
                else:
                        GenSpeedmean[i]=round(np.mean(GenSpeedmean[i]),3)

        for i in range(len(RotSpeedmean)):
                if not RotSpeedmean[i]:
                        RotSpeedmean[i]='-'
                else:
                        RotSpeedmean[i]=round(np.mean(RotSpeedmean[i]),3)

        ## Max
                                          
        for i in range(len(flap1max)):
                if not flap1max[i]:
                        flap1max[i]='-'
                else:
                        flap1max[i]=round(np.max(flap1max[i]),3)
                        
        for i in range(len(flap2max)):
                if not flap2max[i]:
                        flap2max[i]='-'
                else:
                        flap2max[i]=round(np.max(flap2max[i]),3)
                        
        for i in range(len(flap3max)):
                if not flap3max[i]:
                        flap3max[i]='-'
                else:
                        flap3max[i]=round(np.max(flap3max[i]),3)

        for i in range(len(edge1max)):
                if not edge1max[i]:
                        edge1max[i]='-'
                else:
                        edge1max[i]=round(np.max(edge1max[i]),3)
                        
        for i in range(len(edge2max)):
                if not edge2max[i]:
                        edge2max[i]='-'
                else:
                        edge2max[i]=round(np.max(edge2max[i]),3)
                        
        for i in range(len(edge3max)):
                if not edge3max[i]:
                        edge3max[i]='-'
                else:
                        edge3max[i]=round(np.max(edge3max[i]),3)

        for i in range(len(tiltmax)):
                if not tiltmax[i]:
                        tiltmax[i]='-'
                else:
                        tiltmax[i]=round(np.max(tiltmax[i]),3)
                        
        for i in range(len(yawmax)):
                if not yawmax[i]:
                        yawmax[i]='-'
                else:
                        yawmax[i]=round(np.max(yawmax[i]),3)
                        
        for i in range(len(Rtorquemax)):
                if not Rtorquemax[i]:
                        Rtorquemax[i]='-'
                else:
                        Rtorquemax[i]=round(np.max(Rtorquemax[i]),3)

        for i in range(len(TwrBsNmax)):
                if not TwrBsNmax[i]:
                        TwrBsNmax[i]='-'
                else:
                        TwrBsNmax[i]=round(np.max(TwrBsNmax[i]),3)
                        
        for i in range(len(TwrBsLmax)):
                if not TwrBsLmax[i]:
                        TwrBsLmax[i]='-'
                else:
                        TwrBsLmax[i]=round(np.max(TwrBsLmax[i]),3)
                        
        for i in range(len(TwrTqmax)):
                if not TwrTqmax[i]:
                        TwrTqmax[i]='-'
                else:
                        TwrTqmax[i]=round(np.max(TwrTqmax[i]),3)
                        
        for i in range(len(pitchactuationload1max)):
                if not pitchactuationload1max[i]:
                        pitchactuationload1max[i]='-'
                else:
                        pitchactuationload1max[i]=round(np.max(pitchactuationload1max[i]),3)
                        
        for i in range(len(pitchactuationload2max)):
                if not pitchactuationload2max[i]:
                        pitchactuationload2max[i]='-'
                else:
                        pitchactuationload2max[i]=round(np.max(pitchactuationload2max[i]),3)

        for i in range(len(pitchactuationload3max)):
                if not pitchactuationload3max[i]:
                        pitchactuationload3max[i]='-'
                else:
                        pitchactuationload3max[i]=round(np.max(pitchactuationload3max[i]),3)

        for i in range(len(TwrTopAccNormalmax)):
                if not TwrTopAccNormalmax[i]:
                        TwrTopAccNormalmax[i]='-'
                else:
                        TwrTopAccNormalmax[i]=round(np.max(TwrTopAccNormalmax[i]),3)

        for i in range(len(TwrTopAccLatmax)):
                if not TwrTopAccLatmax[i]:
                        TwrTopAccLatmax[i]='-'
                else:
                        TwrTopAccLatmax[i]=round(np.max(TwrTopAccLatmax[i]),3)

        for i in range(len(TwrTopMomentNormalmax)):
                if not TwrTopMomentNormalmax[i]:
                        TwrTopMomentNormalmax[i]='-'
                else:
                        TwrTopMomentNormalmax[i]=round(np.max(TwrTopMomentNormalmax[i]),3)

        for i in range(len(TwrTopMomentLateralmax)):
                if not TwrTopMomentLateralmax[i]:
                        TwrTopMomentLateralmax[i]='-'
                else:
                        TwrTopMomentLateralmax[i]=round(np.max(TwrTopMomentLateralmax[i]),3)

        for i in range(len(Powermax)):
                if not Powermax[i]:
                        Powermax[i]='-'
                else:
                        Powermax[i]=round(np.max(Powermax[i]),3)

        for i in range(len(GenSpeedmax)):
                if not GenSpeedmax[i]:
                        GenSpeedmax[i]='-'
                else:
                        GenSpeedmax[i]=round(np.max(GenSpeedmax[i]),3)

        for i in range(len(RotSpeedmax)):
                if not RotSpeedmax[i]:
                        RotSpeedmax[i]='-'
                else:
                        RotSpeedmax[i]=round(np.max(RotSpeedmax[i]),3)

        ## Deviation

        for i in range(len(flap1dev)):
                if not flap1dev[i]:
                        flap1dev[i]='-'
                else:
                        flap1dev[i]=round(np.mean(flap1dev[i]),3)
                        
        for i in range(len(flap2dev)):
                if not flap2dev[i]:
                        flap2dev[i]='-'
                else:
                        flap2dev[i]=round(np.mean(flap2dev[i]),3)
                        
        for i in range(len(flap3dev)):
                if not flap3dev[i]:
                        flap3dev[i]='-'
                else:
                        flap3dev[i]=round(np.mean(flap3dev[i]),3)

        for i in range(len(edge1dev)):
                if not edge1dev[i]:
                        edge1dev[i]='-'
                else:
                        edge1dev[i]=round(np.mean(edge1dev[i]),3)
                        
        for i in range(len(edge2dev)):
                if not edge2dev[i]:
                        edge2dev[i]='-'
                else:
                        edge2dev[i]=round(np.mean(edge2dev[i]),3)
                        
        for i in range(len(edge3dev)):
                if not edge3dev[i]:
                        edge3dev[i]='-'
                else:
                        edge3dev[i]=round(np.mean(edge3dev[i]),3)

        for i in range(len(tiltdev)):
                if not tiltdev[i]:
                        tiltdev[i]='-'
                else:
                        tiltdev[i]=round(np.mean(tiltdev[i]),3)
                        
        for i in range(len(yawdev)):
                if not yawdev[i]:
                        yawdev[i]='-'
                else:
                        yawdev[i]=round(np.mean(yawdev[i]),3)
                        
        for i in range(len(Rtorquedev)):
                if not Rtorquedev[i]:
                        Rtorquedev[i]='-'
                else:
                        Rtorquedev[i]=round(np.mean(Rtorquedev[i]),3)

        for i in range(len(TwrBsNdev)):
                if not TwrBsNdev[i]:
                        TwrBsNdev[i]='-'
                else:
                        TwrBsNdev[i]=round(np.mean(TwrBsNdev[i]),3)
                        
        for i in range(len(TwrBsLdev)):
                if not TwrBsLdev[i]:
                        TwrBsLdev[i]='-'
                else:
                        TwrBsLdev[i]=round(np.mean(TwrBsLdev[i]),3)
                        
        for i in range(len(TwrTqdev)):
                if not TwrTqdev[i]:
                        TwrTqdev[i]='-'
                else:
                        TwrTqdev[i]=round(np.mean(TwrTqdev[i]),3)
                        
        for i in range(len(pitchactuationload1dev)):
                if not pitchactuationload1dev[i]:
                        pitchactuationload1dev[i]='-'
                else:
                        pitchactuationload1dev[i]=round(np.mean(pitchactuationload1dev[i]),3)
                        
        for i in range(len(pitchactuationload2dev)):
                if not pitchactuationload2dev[i]:
                        pitchactuationload2dev[i]='-'
                else:
                        pitchactuationload2dev[i]=round(np.mean(pitchactuationload2dev[i]),3)

        for i in range(len(pitchactuationload3dev)):
                if not pitchactuationload3dev[i]:
                        pitchactuationload3dev[i]='-'
                else:
                        pitchactuationload3dev[i]=round(np.mean(pitchactuationload3dev[i]),3)

        for i in range(len(TwrTopAccNormaldev)):
                if not TwrTopAccNormaldev[i]:
                        TwrTopAccNormaldev[i]='-'
                else:
                        TwrTopAccNormaldev[i]=round(np.mean(TwrTopAccNormaldev[i]),3)

        for i in range(len(TwrTopAccLatdev)):
                if not TwrTopAccLatdev[i]:
                        TwrTopAccLatdev[i]='-'
                else:
                        TwrTopAccLatdev[i]=round(np.mean(TwrTopAccLatdev[i]),3)

        for i in range(len(TwrTopMomentNormaldev)):
                if not TwrTopMomentNormaldev[i]:
                        TwrTopMomentNormaldev[i]='-'
                else:
                        TwrTopMomentNormaldev[i]=round(np.mean(TwrTopMomentNormaldev[i]),3)

        for i in range(len(TwrTopMomentLateraldev)):
                if not TwrTopMomentLateraldev[i]:
                        TwrTopMomentLateraldev[i]='-'
                else:
                        TwrTopMomentLateraldev[i]=round(np.mean(TwrTopMomentLateraldev[i]),3)

        for i in range(len(Powerdev)):
                if not Powerdev[i]:
                        Powerdev[i]='-'
                else:
                        Powerdev[i]=round(np.mean(Powerdev[i]),3)

        for i in range(len(GenSpeeddev)):
                if not GenSpeeddev[i]:
                        GenSpeeddev[i]='-'
                else:
                        GenSpeeddev[i]=round(np.mean(GenSpeeddev[i]),3)

        for i in range(len(RotSpeeddev)):
                if not RotSpeeddev[i]:
                        RotSpeeddev[i]='-'
                else:
                        RotSpeeddev[i]=round(np.mean(RotSpeeddev[i]),3)

   
######################################################################################################## Report ######################################################################################################
        
        header = r'''\documentclass[12pt]{article}

        \usepackage[utf8]{inputenc}
        \usepackage{indentfirst}
        \usepackage[a4paper,left=1cm,right=2cm,top=2cm,bottom=3cm]{geometry}
        \usepackage[T1]{fontenc}
        \usepackage[tablename=Table]{caption} %table
        \usepackage[figurename=Figure]{caption} %figure
        \usepackage{lmodern}
        \usepackage{float}
        \usepackage{authblk}
        \usepackage{booktabs}
        \usepackage{nomencl} 
        \usepackage{microtype}
        \usepackage[english,hyperpageref]{backref}
        \usepackage{graphicx}

        \makeindex

        \begin{document}
        '''

        footer = r'''\end{document}'''

        main = r'''
            \title{\textbf{{\Huge '''+turbinefast+' '+Simulation+r''' Simulation Report}}} % 
            \author{Fast Interface} %autor
            \maketitle %title autor data
            \thispagestyle{empty} % no enumeration at page
            \newpage 
            
            \setcounter{page}{1} % new page count
            \pagenumbering{Roman} % Roman numerals
            \tableofcontents % summary
            \newpage
            
            \setcounter{page}{1} % new page count
            \pagenumbering{arabic} % Arabic numeral
            
            \section{Introduction}

            This report was created using the FAST INTERFACE program for automated simulations of National Renewable Energy Resources (NREL) software Fatigue, Aerodynamics, Strucutures and Turbulence (FAST).
            It has the objective to expose the results of the simulations proposed by the user via the FAST INTERFACE in a PDF file. This report is organized as follow: second section describes used parameters
            for the simulation such as wind, aerodynamics and elastodynamics characteristics and FAST modules used. Third section describes the output parameters of the simulation based on IEC 61400.13
            fundamental loads quantitites. Fourth section is about the plots and tables of the results of the simulations

            \section{Customized simulation and turbine model characteristics}

            The wind turbine model used for simulations and to generate this report was the '''+turbinefast+r'''.fst model file.

            \subsection{About the simulation}

            The modules enabled for the simulations are showed in Table \ref{tab:SimulationMods}.

            \begin{table}[H]
            \centering
            \begin{tabular}{@{}cc@{}}
            \toprule
            \multicolumn{2}{c}{\textbf{Simulation Modules}} \\ \midrule
             InflowWind                      & Enabled    \\
             ElastoDyn                      & '''+ElastoStatus+r'''    \\
             BeamDyn                      & '''+BeamdynStatus+r'''    \\
             AeroDyn                   & '''+AeroStatus+r'''    \\
             ServoDyn                     & '''+ServoStatus+r'''    \\
             HydroDyn                     & '''+HydroStatus+r'''    \\
             SubDyn                     & '''+SubStatus+r'''    \\
             MoorDyn                      & '''+MoorStatus+r'''    \\
             IceDyn                     & '''+IceStatus+r'''    \\
            \bottomrule
            \end{tabular}
            \caption{Simulation Modules}
            \label{tab:SimulationMods}
            \end{table}
        
            For simulation, time-steps used by FAST and modules is showed in Table \ref{tab:TimeStep}.
        
            \begin{table}[H]
            \centering
            \begin{tabular}{@{}cc@{}}
            \toprule
            \multicolumn{2}{c}{\textbf{Simulation time-step}} \\ \midrule
             FAST time-step                      & '''+str((1/frequency)/10)+r''' s   \\
             Modules time-step                      & '''+str((1/frequency)/10)+r''' s    \\
             FAST output time-step                   & '''+str(1/frequency)+r''' s   \\
            \bottomrule
            \end{tabular}
            \caption{Simulation time-step}
            \label{tab:TimeStep}
            \end{table}

            \subsection{Turbine model}
        
            The turbine model primary (input) file used for simulations was "'''+turbinefast+r'''.fst". This turbine model was simulated with '''+str(DOF)+r''' of the 25 degrees of freedom(DOF) enabled, as in
            Table \ref{ElastoSumDOF}.

            \begin{table}[H]
            \centering
            \begin{tabular}{@{}cc@{}}
            \toprule
            \multicolumn{2}{c}{\textbf{Degrees of freedom of simulation}} \\ \midrule
             Platform horizontal surge translation                    & '''+DOF_1_status+r''' \\
             Platform horizontal sway translation                     & '''+DOF_2_status+r'''\\
             Platform vertical heave translation                      & '''+DOF_3_status+r'''    \\
             Platform roll tilt rotation                              & '''+DOF_4_status+r'''    \\
             Platform pitch tilt rotation                             & '''+DOF_5_status+r'''    \\
             Platform yaw rotation                                    & '''+DOF_6_status+r'''    \\
             1st tower fore-aft bending mode                          & '''+DOF_7_status+r'''    \\
             1st tower side-to-side bending mode                      & '''+DOF_8_status+r'''    \\
             2nd tower fore-aft bending mode                          & '''+DOF_9_status+r'''    \\
             2nd tower side-to-side bending mode                      & '''+DOF_10_status+r'''    \\
             Nacelle yaw                                              & '''+DOF_11_status+r'''    \\
             Rotor-furl                                               & '''+DOF_12_status+r'''    \\
             Variable speed generator                                 & '''+DOF_13_status+r'''    \\
             Drivetrain rotational-flexibility                        & '''+DOF_14_status+r'''    \\
             Tail-furl                                                & '''+DOF_15_status+r'''    \\
             1st flapwise bending-mode of blade 1                     & '''+DOF_16_status+r'''    \\
             1st edgewise bending-mode of blade 1                     & '''+DOF_17_status+r''' \\
             2nd flapwise bending-mode of blade 1                     & '''+DOF_18_status+r'''\\
             1st flapwise bending-mode of blade 2                     & '''+DOF_19_status+r'''    \\
             1st edgewise bending-mode of blade 2                     & '''+DOF_20_status+r'''    \\
             2nd flapwise bending-mode of blade 2                     & '''+DOF_21_status+r'''    \\
             1st flapwise bending-mode of blade 3                     & '''+DOF_22_status+r'''    \\
             1st edgewise bending-mode of blade 3                     & '''+DOF_23_status+r'''    \\
             2nd flapwise bending-mode of blade 3                     & '''+DOF_24_status+r'''    \\
            \bottomrule
            \end{tabular}
            \caption{ElastoDyn Summary}
            \label{tab:ElastoSumDOF}
            \end{table}

            Elastodynamic module calculate a few parameters of the turbine, showed in Table \ref{tab:ElastoSum}.
             
            \begin{table}[H]
            \centering
            \begin{tabular}{@{}cc@{}}
            \toprule
            \multicolumn{2}{c}{\textbf{ElastoDyn summary calculated properties}} \\ \midrule
             Hub Height      & '''+hub_height+r''' (m)        \\
             Rotor Mass      & '''+Rotor_mass+r''' (kg)     \\
             Rotor Inertia   & '''+Rotor_inertia+r''' (kg/m2)  \\
             Tower-top mass  & '''+Tower_top_mass+r''' (kg)     \\
             Tower mass      & '''+Tower_mass+r''' (kg)     \\
             Plataform mass  & '''+Platform_mass+r''' (kg)     \\
             Mass including platform & '''+mass_with_plt+r''' (kg)     \\
            \bottomrule
            \end{tabular}
            \caption{ElastoDyn Summary}
            \label{tab:ElastoSum}
            \end{table}

            Blades characteristics as mass, first mass moment, second mass moment and center of mass are show in Table \ref{tab:bladecharactheristics}.
            
            \begin{table}[H]
            \centering
            \begin{tabular}{@{}ccll@{}}
            \toprule
            \multicolumn{4}{c}{\textbf{Blade mass properties}} \\ \midrule
             Property & Blade 1 & \multicolumn{1}{c}{Blade 2} & \multicolumn{1}{c}{Blade 3} \\
             Mass (kg) & '''+blade_1_mass+r''' & '''+blade_2_mass+r''' & '''+blade_3_mass+r''' \\
             First mass moment (kg/m2) & '''+blade_1_first_mass_moment_+r''' & '''+blade_2_first_mass_moment_+r''' & '''+blade_3_first_mass_moment_+r''' \\
             Second mass moment (kg/m2)& '''+blade_1_second_mass_moment_+r''' & '''+blade_2_second_mass_moment_+r''' & '''+blade_3_second_mass_moment_+r'''  \\
             Center of mass (m)& '''+Blade_1_cm+r''' & '''+Blade_2_cm+r''' & '''+Blade_3_cm+r'''  \\
            \bottomrule
            \end{tabular}
            \caption{Blade characteristics}
            \label{tab:bladecharactheristics}
            \end{table}

            For more informations about turbine configuration, look at "'''+ed_str+r'''" for the ElastoDyn output summary file.

            \subsection{Aerodynamic characteristics}

             Aerodynamic characteristics of the simulation were extracted from the '''+AeroStatus+r''' module file. Because many contents between both versions of AeroDyn (v14 and v15) are very different,
             it is better for the user to check the simulations features in the AeroDyn output summary file "'''+Ad_str+r'''".
        
            \subsection{Output parameters}


            FAST can output more than 200 parameters, so besides the output parameters selected by user, the FAST INTERFACE software included parameters accordingly to IEC61400-13 fundamental load quantities as
            standard. Fundamentals loads are the basic loads on critical locations of the wind turbine, and the loading in all relevant structural components of it can be derived from them. This can not be changed,
            because the report plots are based on those. Table \ref{tab:FundamentalQuantities1} shows the quantities and each FAST output variable related to it.

            \begin{table}[H]
            \caption{Fundamental load quantities}
            \label{tab:FundalmentalLoads1}
            \centering
            \begin{tabular}{@{}cc@{}}
            \toprule
            \multicolumn{2}{c}{\textbf{Load quantities}} \\ \midrule
            Blade root flatwise bending moment & RootMybi, i = Blade          \\
	    Blade root edgewise bending moment & RootMxbi, i = Blade             \\
	    Rotor tilt moment                  & LSSTipMys                    \\
	    Rotor yaw moment                   & LssTipMzs                    \\
	    Rotor torque                       & LSShftMxa                    \\
	    Tower base normal                  & TwrBsMyt                    \\
	    Tower base lateral moment          & TwrBsMxt                    \\  \bottomrule
            \label{tab:FundamentalQuantities1}
            \end{tabular}
            \end{table}
            
            Wind turbines with rated power greater than 1.5 MW and a rotor diameter greater than 75 m have additional requirements, as shown in Table \ref{tab:FundalmentalLoads2}.
            The similarity of blade behavior is verified through a second blade measurement.

            \begin{table}[H]
            \caption{Fundamental load quantities for wind turbines with 1.5 MW rated power or more}
            \label{tab:FundalmentalLoads2}
            \centering
            \begin{tabular}{@{}cc@{}}
            \toprule
            \multicolumn{2}{c}{\textbf{Load quantities}} \\ \midrule
	    Blade flatwise bending moment distribution & 2 blades mandatory \\
	    Blade edgewise bending moment distribution & 2 blades mandatory \\
	    Blade torsional frequency and damping & Can only be calculated \\
	    Pitch actuation loads & RootMzci, i = Blade\\
	    Tower top acceleration in normal direction & YawBrTAxp \\
	    Tower top acceleration in lateral direction & YawBrTAyp \\
	    Tower mid normal moment & TwHtiMLyt, i = Strain Gauge \\
	    Tower mid lateral moment & TwHtiMLxt , i = Strain Gauge\\
	    Tower top normal moment & YawBrMyp \\
	    Tower top lateral moment & YawBrMxp \\
	    Tower torque & TwrBsMzt \\ \bottomrule
            \end{tabular}
            \end{table}

            In addition to the mechanical output parameters, the IEC61400-13 requests other quantities. A few of those that are outputed by FAST INTERFACE are showed in Table \ref{tab:OtherQuantities}

            \begin{table}[H]
            \caption{Others operation quantities}
            \label{tab:OtherQuantities}
            \centering
            \begin{tabular}{@{}cc@{}}
            \toprule
            \multicolumn{2}{c}{\textbf{Load quantities}} \\ \midrule
	    Electrical Power & GenPwr \\
	    Rotor Speed & RotSpeed \\
	    Rotor Azimuth Angle & Azimuth \\
	    Pitch angle & PtchPMzci , i = blade\\ \bottomrule
            \end{tabular}
            \end{table}

            \section{Simulation results}

            Simulations results were obtained from FAST output files. Those files come in a .txt format, and FAST INTERFACE handle them to get necessary data for plotting in this section. For any purpose,
            .csv files are generated from each of the simulation output .txt, so the user can work already with this format if wanted.

            As mentioned before, the output results are based in the IEC 61400-13 fundamental loads quantities. Time-series and Fast-Fourier-Transform (FFT) plots for each of the quantities available in FAST
            outputs are showed in the next sections, as well as tables with statistical data.

            \subsection{Statistical data}

            This section shows statistcs binned data of the IEC 61400-13 outputs for each of the wind speeds requested by the user from the customized simulation. The wind speed bins not requested/simulated are
            marked with a '-' in the quantities tables. The bin data is showed in Table \ref{tab:BinnedData}.
            
            \newpage

            \subsubsection{Blades roots flapwise bending moments}

            Table \ref{tab:Blade1FlapwiseMomentoRoot} shows the flapwise bending moment at the root of blade 1.

            \begin{table}[H]
            \caption{Blade 1 root flapwise bending moment}
            \label{tab:Blade1FlapwiseMomentoRoot}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (kN.m)} & \textbf{Mean (kN.m)} & \textbf{Max (kN.m)} & \textbf{Std dev.(kN.m)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(flap1min[0])+r'''& '''+str(flap1mean[0])+r''' & '''+str(flap1max[0])+r''' & '''+str(flap1dev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(flap1min[1])+r'''& '''+str(flap1mean[1])+r''' & '''+str(flap1max[1])+r''' & '''+str(flap1dev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(flap1min[2])+r'''& '''+str(flap1mean[2])+r''' & '''+str(flap1max[2])+r''' & '''+str(flap1dev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(flap1min[3])+r'''& '''+str(flap1mean[3])+r''' & '''+str(flap1max[3])+r''' & '''+str(flap1dev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(flap1min[4])+r'''& '''+str(flap1mean[4])+r''' & '''+str(flap1max[4])+r''' & '''+str(flap1dev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(flap1min[5])+r'''& '''+str(flap1mean[5])+r''' & '''+str(flap1max[5])+r''' & '''+str(flap1dev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(flap1min[6])+r'''& '''+str(flap1mean[6])+r''' & '''+str(flap1max[6])+r''' & '''+str(flap1dev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(flap1min[7])+r'''& '''+str(flap1mean[7])+r''' & '''+str(flap1max[7])+r''' & '''+str(flap1dev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(flap1min[8])+r'''& '''+str(flap1mean[8])+r''' & '''+str(flap1max[8])+r''' & '''+str(flap1dev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(flap1min[9])+r'''& '''+str(flap1mean[9])+r''' & '''+str(flap1max[9])+r''' & '''+str(flap1dev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(flap1min[10])+r'''& '''+str(flap1mean[10])+r''' & '''+str(flap1max[10])+r''' & '''+str(flap1dev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(flap1min[11])+r'''& '''+str(flap1mean[11])+r''' & '''+str(flap1max[11])+r''' & '''+str(flap1dev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(flap1min[12])+r'''& '''+str(flap1mean[12])+r''' & '''+str(flap1max[12])+r''' & '''+str(flap1dev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(flap1min[13])+r'''& '''+str(flap1mean[13])+r''' & '''+str(flap1max[13])+r''' & '''+str(flap1dev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(flap1min[14])+r'''& '''+str(flap1mean[14])+r''' & '''+str(flap1max[14])+r''' & '''+str(flap1dev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(flap1min[15])+r'''& '''+str(flap1mean[15])+r''' & '''+str(flap1max[15])+r''' & '''+str(flap1dev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(flap1min[16])+r'''& '''+str(flap1mean[16])+r''' & '''+str(flap1max[16])+r''' & '''+str(flap1dev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(flap1min[17])+r'''& '''+str(flap1mean[17])+r''' & '''+str(flap1max[17])+r''' & '''+str(flap1dev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(flap1min[18])+r'''& '''+str(flap1mean[18])+r''' & '''+str(flap1max[18])+r''' & '''+str(flap1dev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(flap1min[19])+r'''& '''+str(flap1mean[19])+r''' & '''+str(flap1max[19])+r''' & '''+str(flap1dev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(flap1min[20])+r'''& '''+str(flap1mean[20])+r''' & '''+str(flap1max[20])+r''' & '''+str(flap1dev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(flap1min[21])+r'''& '''+str(flap1mean[21])+r''' & '''+str(flap1max[21])+r''' & '''+str(flap1dev[21])+r''' \\ \hline
            \end{tabular}
            \egroup
            \end{table}

            \newpage
            
            Table \ref{tab:Blade2FlapwiseMomentoRoot} shows the flapwise bending moment at the root of blade 2.

            \begin{table}[H]
            \caption{Blade 2 root flapwise bending moment}
            \label{tab:Blade2FlapwiseMomentoRoot}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (kN.m)} & \textbf{Mean (kN.m)} & \textbf{Max (kN.m)} & \textbf{Std dev.(kN.m)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(flap2min[0])+r'''& '''+str(flap2mean[0])+r''' & '''+str(flap2max[0])+r''' & '''+str(flap2dev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(flap2min[1])+r'''& '''+str(flap2mean[1])+r''' & '''+str(flap2max[1])+r''' & '''+str(flap2dev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(flap2min[2])+r'''& '''+str(flap2mean[2])+r''' & '''+str(flap2max[2])+r''' & '''+str(flap2dev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(flap2min[3])+r'''& '''+str(flap2mean[3])+r''' & '''+str(flap2max[3])+r''' & '''+str(flap2dev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(flap2min[4])+r'''& '''+str(flap2mean[4])+r''' & '''+str(flap2max[4])+r''' & '''+str(flap2dev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(flap2min[5])+r'''& '''+str(flap2mean[5])+r''' & '''+str(flap2max[5])+r''' & '''+str(flap2dev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(flap2min[6])+r'''& '''+str(flap2mean[6])+r''' & '''+str(flap2max[6])+r''' & '''+str(flap2dev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(flap2min[7])+r'''& '''+str(flap2mean[7])+r''' & '''+str(flap2max[7])+r''' & '''+str(flap2dev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(flap2min[8])+r'''& '''+str(flap2mean[8])+r''' & '''+str(flap2max[8])+r''' & '''+str(flap2dev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(flap2min[9])+r'''& '''+str(flap2mean[9])+r''' & '''+str(flap2max[9])+r''' & '''+str(flap2dev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(flap2min[10])+r'''& '''+str(flap2mean[10])+r''' & '''+str(flap2max[10])+r''' & '''+str(flap2dev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(flap2min[11])+r'''& '''+str(flap2mean[11])+r''' & '''+str(flap2max[11])+r''' & '''+str(flap2dev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(flap2min[12])+r'''& '''+str(flap2mean[12])+r''' & '''+str(flap2max[12])+r''' & '''+str(flap2dev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(flap2min[13])+r'''& '''+str(flap2mean[13])+r''' & '''+str(flap2max[13])+r''' & '''+str(flap2dev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(flap2min[14])+r'''& '''+str(flap2mean[14])+r''' & '''+str(flap2max[14])+r''' & '''+str(flap2dev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(flap2min[15])+r'''& '''+str(flap2mean[15])+r''' & '''+str(flap2max[15])+r''' & '''+str(flap2dev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(flap2min[16])+r'''& '''+str(flap2mean[16])+r''' & '''+str(flap2max[16])+r''' & '''+str(flap2dev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(flap2min[17])+r'''& '''+str(flap2mean[17])+r''' & '''+str(flap2max[17])+r''' & '''+str(flap2dev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(flap2min[18])+r'''& '''+str(flap2mean[18])+r''' & '''+str(flap2max[18])+r''' & '''+str(flap2dev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(flap2min[19])+r'''& '''+str(flap2mean[19])+r''' & '''+str(flap2max[19])+r''' & '''+str(flap2dev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(flap2min[20])+r'''& '''+str(flap2mean[20])+r''' & '''+str(flap2max[20])+r''' & '''+str(flap2dev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(flap2min[21])+r'''& '''+str(flap2mean[21])+r''' & '''+str(flap2max[21])+r''' & '''+str(flap2dev[21])+r''' \\ \hline
            \end{tabular}
            \egroup
            \end{table}

            \newpage

            Table \ref{tab:Blade3FlapwiseMomentoRoot} shows the flapwise bending moment at the root of blade 3.

            \begin{table}[H]
            \caption{Blade 3 root flapwise bending moment}
            \label{tab:Blade3FlapwiseMomentoRoot}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (kN.m)} & \textbf{Mean (kN.m)} & \textbf{Max (kN.m)} & \textbf{Std dev.(kN.m)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(flap3min[0])+r'''& '''+str(flap3mean[0])+r''' & '''+str(flap3max[0])+r''' & '''+str(flap3dev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(flap3min[1])+r'''& '''+str(flap3mean[1])+r''' & '''+str(flap3max[1])+r''' & '''+str(flap3dev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(flap3min[2])+r'''& '''+str(flap3mean[2])+r''' & '''+str(flap3max[2])+r''' & '''+str(flap3dev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(flap3min[3])+r'''& '''+str(flap3mean[3])+r''' & '''+str(flap3max[3])+r''' & '''+str(flap3dev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(flap3min[4])+r'''& '''+str(flap3mean[4])+r''' & '''+str(flap3max[4])+r''' & '''+str(flap3dev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(flap3min[5])+r'''& '''+str(flap3mean[5])+r''' & '''+str(flap3max[5])+r''' & '''+str(flap3dev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(flap3min[6])+r'''& '''+str(flap3mean[6])+r''' & '''+str(flap3max[6])+r''' & '''+str(flap3dev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(flap3min[7])+r'''& '''+str(flap3mean[7])+r''' & '''+str(flap3max[7])+r''' & '''+str(flap3dev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(flap3min[8])+r'''& '''+str(flap3mean[8])+r''' & '''+str(flap3max[8])+r''' & '''+str(flap3dev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(flap3min[9])+r'''& '''+str(flap3mean[9])+r''' & '''+str(flap3max[9])+r''' & '''+str(flap3dev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(flap3min[10])+r'''& '''+str(flap3mean[10])+r''' & '''+str(flap3max[10])+r''' & '''+str(flap3dev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(flap3min[11])+r'''& '''+str(flap3mean[11])+r''' & '''+str(flap3max[11])+r''' & '''+str(flap3dev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(flap3min[12])+r'''& '''+str(flap3mean[12])+r''' & '''+str(flap3max[12])+r''' & '''+str(flap3dev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(flap3min[13])+r'''& '''+str(flap3mean[13])+r''' & '''+str(flap3max[13])+r''' & '''+str(flap3dev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(flap3min[14])+r'''& '''+str(flap3mean[14])+r''' & '''+str(flap3max[14])+r''' & '''+str(flap3dev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(flap3min[15])+r'''& '''+str(flap3mean[15])+r''' & '''+str(flap3max[15])+r''' & '''+str(flap3dev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(flap3min[16])+r'''& '''+str(flap3mean[16])+r''' & '''+str(flap3max[16])+r''' & '''+str(flap3dev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(flap3min[17])+r'''& '''+str(flap3mean[17])+r''' & '''+str(flap3max[17])+r''' & '''+str(flap3dev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(flap3min[18])+r'''& '''+str(flap3mean[18])+r''' & '''+str(flap3max[18])+r''' & '''+str(flap3dev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(flap3min[19])+r'''& '''+str(flap3mean[19])+r''' & '''+str(flap3max[19])+r''' & '''+str(flap3dev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(flap3min[20])+r'''& '''+str(flap3mean[20])+r''' & '''+str(flap3max[20])+r''' & '''+str(flap3dev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(flap3min[21])+r'''& '''+str(flap3mean[21])+r''' & '''+str(flap3max[21])+r''' & '''+str(flap3dev[21])+r''' \\ \hline     
            \end{tabular}
            \egroup
            \end{table}

            \newpage        
            
            \subsubsection{Blades roots edgewise bending moments}

            Table \ref{tab:Blade1EdgewiseMomentoRoot} shows the edgewise bending moment at the root of blade 1.

            \begin{table}[H]
            \caption{Blade 1 root edgewise bending moment}
            \label{tab:Blade1EdgewiseMomentoRoot}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (kN.m)} & \textbf{Mean (kN.m)} & \textbf{Max (kN.m)} & \textbf{Std dev.(kN.m)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(edge1min[0])+r'''& '''+str(edge1mean[0])+r''' & '''+str(edge1max[0])+r''' & '''+str(edge1dev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(edge1min[1])+r'''& '''+str(edge1mean[1])+r''' & '''+str(edge1max[1])+r''' & '''+str(edge1dev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(edge1min[2])+r'''& '''+str(edge1mean[2])+r''' & '''+str(edge1max[2])+r''' & '''+str(edge1dev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(edge1min[3])+r'''& '''+str(edge1mean[3])+r''' & '''+str(edge1max[3])+r''' & '''+str(edge1dev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(edge1min[4])+r'''& '''+str(edge1mean[4])+r''' & '''+str(edge1max[4])+r''' & '''+str(edge1dev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(edge1min[5])+r'''& '''+str(edge1mean[5])+r''' & '''+str(edge1max[5])+r''' & '''+str(edge1dev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(edge1min[6])+r'''& '''+str(edge1mean[6])+r''' & '''+str(edge1max[6])+r''' & '''+str(edge1dev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(edge1min[7])+r'''& '''+str(edge1mean[7])+r''' & '''+str(edge1max[7])+r''' & '''+str(edge1dev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(edge1min[8])+r'''& '''+str(edge1mean[8])+r''' & '''+str(edge1max[8])+r''' & '''+str(edge1dev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(edge1min[9])+r'''& '''+str(edge1mean[9])+r''' & '''+str(edge1max[9])+r''' & '''+str(edge1dev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(edge1min[10])+r'''& '''+str(edge1mean[10])+r''' & '''+str(edge1max[10])+r''' & '''+str(edge1dev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(edge1min[11])+r'''& '''+str(edge1mean[11])+r''' & '''+str(edge1max[11])+r''' & '''+str(edge1dev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(edge1min[12])+r'''& '''+str(edge1mean[12])+r''' & '''+str(edge1max[12])+r''' & '''+str(edge1dev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(edge1min[13])+r'''& '''+str(edge1mean[13])+r''' & '''+str(edge1max[13])+r''' & '''+str(edge1dev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(edge1min[14])+r'''& '''+str(edge1mean[14])+r''' & '''+str(edge1max[14])+r''' & '''+str(edge1dev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(edge1min[15])+r'''& '''+str(edge1mean[15])+r''' & '''+str(edge1max[15])+r''' & '''+str(edge1dev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(edge1min[16])+r'''& '''+str(edge1mean[16])+r''' & '''+str(edge1max[16])+r''' & '''+str(edge1dev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(edge1min[17])+r'''& '''+str(edge1mean[17])+r''' & '''+str(edge1max[17])+r''' & '''+str(edge1dev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(edge1min[18])+r'''& '''+str(edge1mean[18])+r''' & '''+str(edge1max[18])+r''' & '''+str(edge1dev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(edge1min[19])+r'''& '''+str(edge1mean[19])+r''' & '''+str(edge1max[19])+r''' & '''+str(edge1dev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(edge1min[20])+r'''& '''+str(edge1mean[20])+r''' & '''+str(edge1max[20])+r''' & '''+str(edge1dev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(edge1min[21])+r'''& '''+str(edge1mean[21])+r''' & '''+str(edge1max[21])+r''' & '''+str(edge1dev[21])+r''' \\ \hline
            \end{tabular}
            \egroup
            \end{table}

            \newpage  

            Table \ref{tab:Blade2EdgewiseMomentoRoot} shows the edgewise bending moment at the root of blade 2.

            \begin{table}[H]
            \caption{Blade 2 root edgewise bending moment}
            \label{tab:Blade2EdgewiseMomentoRoot}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (kN.m)} & \textbf{Mean (kN.m)} & \textbf{Max (kN.m)} & \textbf{Std dev.(kN.m)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(edge2min[0])+r'''& '''+str(edge2mean[0])+r''' & '''+str(edge2max[0])+r''' & '''+str(edge2dev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(edge2min[1])+r'''& '''+str(edge2mean[1])+r''' & '''+str(edge2max[1])+r''' & '''+str(edge2dev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(edge2min[2])+r'''& '''+str(edge2mean[2])+r''' & '''+str(edge2max[2])+r''' & '''+str(edge2dev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(edge2min[3])+r'''& '''+str(edge2mean[3])+r''' & '''+str(edge2max[3])+r''' & '''+str(edge2dev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(edge2min[4])+r'''& '''+str(edge2mean[4])+r''' & '''+str(edge2max[4])+r''' & '''+str(edge2dev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(edge2min[5])+r'''& '''+str(edge2mean[5])+r''' & '''+str(edge2max[5])+r''' & '''+str(edge2dev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(edge2min[6])+r'''& '''+str(edge2mean[6])+r''' & '''+str(edge2max[6])+r''' & '''+str(edge2dev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(edge2min[7])+r'''& '''+str(edge2mean[7])+r''' & '''+str(edge2max[7])+r''' & '''+str(edge2dev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(edge2min[8])+r'''& '''+str(edge2mean[8])+r''' & '''+str(edge2max[8])+r''' & '''+str(edge2dev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(edge2min[9])+r'''& '''+str(edge2mean[9])+r''' & '''+str(edge2max[9])+r''' & '''+str(edge2dev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(edge2min[10])+r'''& '''+str(edge2mean[10])+r''' & '''+str(edge2max[10])+r''' & '''+str(edge2dev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(edge2min[11])+r'''& '''+str(edge2mean[11])+r''' & '''+str(edge2max[11])+r''' & '''+str(edge2dev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(edge2min[12])+r'''& '''+str(edge2mean[12])+r''' & '''+str(edge2max[12])+r''' & '''+str(edge2dev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(edge2min[13])+r'''& '''+str(edge2mean[13])+r''' & '''+str(edge2max[13])+r''' & '''+str(edge2dev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(edge2min[14])+r'''& '''+str(edge2mean[14])+r''' & '''+str(edge2max[14])+r''' & '''+str(edge2dev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(edge2min[15])+r'''& '''+str(edge2mean[15])+r''' & '''+str(edge2max[15])+r''' & '''+str(edge2dev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(edge2min[16])+r'''& '''+str(edge2mean[16])+r''' & '''+str(edge2max[16])+r''' & '''+str(edge2dev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(edge2min[17])+r'''& '''+str(edge2mean[17])+r''' & '''+str(edge2max[17])+r''' & '''+str(edge2dev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(edge2min[18])+r'''& '''+str(edge2mean[18])+r''' & '''+str(edge2max[18])+r''' & '''+str(edge2dev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(edge2min[19])+r'''& '''+str(edge2mean[19])+r''' & '''+str(edge2max[19])+r''' & '''+str(edge2dev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(edge2min[20])+r'''& '''+str(edge2mean[20])+r''' & '''+str(edge2max[20])+r''' & '''+str(edge2dev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(edge2min[21])+r'''& '''+str(edge2mean[21])+r''' & '''+str(edge2max[21])+r''' & '''+str(edge2dev[21])+r''' \\ \hline
            \end{tabular}
            \egroup
            \end{table}

            \newpage  
            
            Table \ref{tab:Blade3EdgewiseMomentoRoot} shows the edgewise bending moment at the root of blade 3.

            \begin{table}[H]
            \caption{Blade 3 root edgewise bending moment}
            \label{tab:Blade3EdgewiseMomentoRoot}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (kN.m)} & \textbf{Mean (kN.m)} & \textbf{Max (kN.m)} & \textbf{Std dev.(kN.m)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(edge3min[0])+r'''& '''+str(edge3mean[0])+r''' & '''+str(edge3max[0])+r''' & '''+str(edge3dev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(edge3min[1])+r'''& '''+str(edge3mean[1])+r''' & '''+str(edge3max[1])+r''' & '''+str(edge3dev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(edge3min[2])+r'''& '''+str(edge3mean[2])+r''' & '''+str(edge3max[2])+r''' & '''+str(edge3dev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(edge3min[3])+r'''& '''+str(edge3mean[3])+r''' & '''+str(edge3max[3])+r''' & '''+str(edge3dev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(edge3min[4])+r'''& '''+str(edge3mean[4])+r''' & '''+str(edge3max[4])+r''' & '''+str(edge3dev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(edge3min[5])+r'''& '''+str(edge3mean[5])+r''' & '''+str(edge3max[5])+r''' & '''+str(edge3dev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(edge3min[6])+r'''& '''+str(edge3mean[6])+r''' & '''+str(edge3max[6])+r''' & '''+str(edge3dev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(edge3min[7])+r'''& '''+str(edge3mean[7])+r''' & '''+str(edge3max[7])+r''' & '''+str(edge3dev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(edge3min[8])+r'''& '''+str(edge3mean[8])+r''' & '''+str(edge3max[8])+r''' & '''+str(edge3dev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(edge3min[9])+r'''& '''+str(edge3mean[9])+r''' & '''+str(edge3max[9])+r''' & '''+str(edge3dev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(edge3min[10])+r'''& '''+str(edge3mean[10])+r''' & '''+str(edge3max[10])+r''' & '''+str(edge3dev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(edge3min[11])+r'''& '''+str(edge3mean[11])+r''' & '''+str(edge3max[11])+r''' & '''+str(edge3dev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(edge3min[12])+r'''& '''+str(edge3mean[12])+r''' & '''+str(edge3max[12])+r''' & '''+str(edge3dev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(edge3min[13])+r'''& '''+str(edge3mean[13])+r''' & '''+str(edge3max[13])+r''' & '''+str(edge3dev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(edge3min[14])+r'''& '''+str(edge3mean[14])+r''' & '''+str(edge3max[14])+r''' & '''+str(edge3dev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(edge3min[15])+r'''& '''+str(edge3mean[15])+r''' & '''+str(edge3max[15])+r''' & '''+str(edge3dev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(edge3min[16])+r'''& '''+str(edge3mean[16])+r''' & '''+str(edge3max[16])+r''' & '''+str(edge3dev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(edge3min[17])+r'''& '''+str(edge3mean[17])+r''' & '''+str(edge3max[17])+r''' & '''+str(edge3dev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(edge3min[18])+r'''& '''+str(edge3mean[18])+r''' & '''+str(edge3max[18])+r''' & '''+str(edge3dev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(edge3min[19])+r'''& '''+str(edge3mean[19])+r''' & '''+str(edge3max[19])+r''' & '''+str(edge3dev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(edge3min[20])+r'''& '''+str(edge3mean[20])+r''' & '''+str(edge3max[20])+r''' & '''+str(edge3dev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(edge3min[21])+r'''& '''+str(edge3mean[21])+r''' & '''+str(edge3max[21])+r''' & '''+str(edge3dev[21])+r''' \\ \hline
            \end{tabular}
            \egroup
            \end{table}

            \newpage  

            \subsubsection{Rotor moments}

            Table \ref{tab:RotorTilt} shows the rotor tilt moment.

            \begin{table}[H]
            \caption{Rotor tilt moment}
            \label{tab:RotorTilt}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (kN.m)} & \textbf{Mean (kN.m)} & \textbf{Max (kN.m)} & \textbf{Std dev.(kN.m)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(tiltmin[0])+r'''& '''+str(tiltmean[0])+r''' & '''+str(tiltmax[0])+r''' & '''+str(tiltdev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(tiltmin[1])+r'''& '''+str(tiltmean[1])+r''' & '''+str(tiltmax[1])+r''' & '''+str(tiltdev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(tiltmin[2])+r'''& '''+str(tiltmean[2])+r''' & '''+str(tiltmax[2])+r''' & '''+str(tiltdev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(tiltmin[3])+r'''& '''+str(tiltmean[3])+r''' & '''+str(tiltmax[3])+r''' & '''+str(tiltdev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(tiltmin[4])+r'''& '''+str(tiltmean[4])+r''' & '''+str(tiltmax[4])+r''' & '''+str(tiltdev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(tiltmin[5])+r'''& '''+str(tiltmean[5])+r''' & '''+str(tiltmax[5])+r''' & '''+str(tiltdev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(tiltmin[6])+r'''& '''+str(tiltmean[6])+r''' & '''+str(tiltmax[6])+r''' & '''+str(tiltdev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(tiltmin[7])+r'''& '''+str(tiltmean[7])+r''' & '''+str(tiltmax[7])+r''' & '''+str(tiltdev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(tiltmin[8])+r'''& '''+str(tiltmean[8])+r''' & '''+str(tiltmax[8])+r''' & '''+str(tiltdev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(tiltmin[9])+r'''& '''+str(tiltmean[9])+r''' & '''+str(tiltmax[9])+r''' & '''+str(tiltdev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(tiltmin[10])+r'''& '''+str(tiltmean[10])+r''' & '''+str(tiltmax[10])+r''' & '''+str(tiltdev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(tiltmin[11])+r'''& '''+str(tiltmean[11])+r''' & '''+str(tiltmax[11])+r''' & '''+str(tiltdev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(tiltmin[12])+r'''& '''+str(tiltmean[12])+r''' & '''+str(tiltmax[12])+r''' & '''+str(tiltdev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(tiltmin[13])+r'''& '''+str(tiltmean[13])+r''' & '''+str(tiltmax[13])+r''' & '''+str(tiltdev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(tiltmin[14])+r'''& '''+str(tiltmean[14])+r''' & '''+str(tiltmax[14])+r''' & '''+str(tiltdev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(tiltmin[15])+r'''& '''+str(tiltmean[15])+r''' & '''+str(tiltmax[15])+r''' & '''+str(tiltdev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(tiltmin[16])+r'''& '''+str(tiltmean[16])+r''' & '''+str(tiltmax[16])+r''' & '''+str(tiltdev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(tiltmin[17])+r'''& '''+str(tiltmean[17])+r''' & '''+str(tiltmax[17])+r''' & '''+str(tiltdev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(tiltmin[18])+r'''& '''+str(tiltmean[18])+r''' & '''+str(tiltmax[18])+r''' & '''+str(tiltdev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(tiltmin[19])+r'''& '''+str(tiltmean[19])+r''' & '''+str(tiltmax[19])+r''' & '''+str(tiltdev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(tiltmin[20])+r'''& '''+str(tiltmean[20])+r''' & '''+str(tiltmax[20])+r''' & '''+str(tiltdev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(tiltmin[21])+r'''& '''+str(tiltmean[21])+r''' & '''+str(tiltmax[21])+r''' & '''+str(tiltdev[21])+r''' \\ \hline
            \end{tabular}
            \egroup
            \end{table}

            \newpage  

            Table \ref{tab:RotorTilt} shows the rotor yaw moment.

            \begin{table}[H]
            \caption{Rotor yaw moment}
            \label{tab:RotorYaw}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (kN.m)} & \textbf{Mean (kN.m)} & \textbf{Max (kN.m)} & \textbf{Std dev.(kN.m)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(yawmin[0])+r'''& '''+str(yawmean[0])+r''' & '''+str(yawmax[0])+r''' & '''+str(yawdev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(yawmin[1])+r'''& '''+str(yawmean[1])+r''' & '''+str(yawmax[1])+r''' & '''+str(yawdev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(yawmin[2])+r'''& '''+str(yawmean[2])+r''' & '''+str(yawmax[2])+r''' & '''+str(yawdev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(yawmin[3])+r'''& '''+str(yawmean[3])+r''' & '''+str(yawmax[3])+r''' & '''+str(yawdev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(yawmin[4])+r'''& '''+str(yawmean[4])+r''' & '''+str(yawmax[4])+r''' & '''+str(yawdev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(yawmin[5])+r'''& '''+str(yawmean[5])+r''' & '''+str(yawmax[5])+r''' & '''+str(yawdev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(yawmin[6])+r'''& '''+str(yawmean[6])+r''' & '''+str(yawmax[6])+r''' & '''+str(yawdev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(yawmin[7])+r'''& '''+str(yawmean[7])+r''' & '''+str(yawmax[7])+r''' & '''+str(yawdev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(yawmin[8])+r'''& '''+str(yawmean[8])+r''' & '''+str(yawmax[8])+r''' & '''+str(yawdev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(yawmin[9])+r'''& '''+str(yawmean[9])+r''' & '''+str(yawmax[9])+r''' & '''+str(yawdev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(yawmin[10])+r'''& '''+str(yawmean[10])+r''' & '''+str(yawmax[10])+r''' & '''+str(yawdev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(yawmin[11])+r'''& '''+str(yawmean[11])+r''' & '''+str(yawmax[11])+r''' & '''+str(yawdev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(yawmin[12])+r'''& '''+str(yawmean[12])+r''' & '''+str(yawmax[12])+r''' & '''+str(yawdev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(yawmin[13])+r'''& '''+str(yawmean[13])+r''' & '''+str(yawmax[13])+r''' & '''+str(yawdev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(yawmin[14])+r'''& '''+str(yawmean[14])+r''' & '''+str(yawmax[14])+r''' & '''+str(yawdev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(yawmin[15])+r'''& '''+str(yawmean[15])+r''' & '''+str(yawmax[15])+r''' & '''+str(yawdev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(yawmin[16])+r'''& '''+str(yawmean[16])+r''' & '''+str(yawmax[16])+r''' & '''+str(yawdev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(yawmin[17])+r'''& '''+str(yawmean[17])+r''' & '''+str(yawmax[17])+r''' & '''+str(yawdev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(yawmin[18])+r'''& '''+str(yawmean[18])+r''' & '''+str(yawmax[18])+r''' & '''+str(yawdev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(yawmin[19])+r'''& '''+str(yawmean[19])+r''' & '''+str(yawmax[19])+r''' & '''+str(yawdev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(yawmin[20])+r'''& '''+str(yawmean[20])+r''' & '''+str(yawmax[20])+r''' & '''+str(yawdev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(yawmin[21])+r'''& '''+str(yawmean[21])+r''' & '''+str(yawmax[21])+r''' & '''+str(yawdev[21])+r''' \\ \hline
            \end{tabular}
            \egroup
            \end{table}

            \newpage  

            Table \ref{tab:RotorTorque} shows the rotor torque.

            \begin{table}[H]
            \caption{Rotor torque}
            \label{tab:RotorTorque}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (kN.m)} & \textbf{Mean (kN.m)} & \textbf{Max (kN.m)} & \textbf{Std dev.(kN.m)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(Rtorquemin[0])+r'''& '''+str(Rtorquemean[0])+r''' & '''+str(Rtorquemax[0])+r''' & '''+str(Rtorquedev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(Rtorquemin[1])+r'''& '''+str(Rtorquemean[1])+r''' & '''+str(Rtorquemax[1])+r''' & '''+str(Rtorquedev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(Rtorquemin[2])+r'''& '''+str(Rtorquemean[2])+r''' & '''+str(Rtorquemax[2])+r''' & '''+str(Rtorquedev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(Rtorquemin[3])+r'''& '''+str(Rtorquemean[3])+r''' & '''+str(Rtorquemax[3])+r''' & '''+str(Rtorquedev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(Rtorquemin[4])+r'''& '''+str(Rtorquemean[4])+r''' & '''+str(Rtorquemax[4])+r''' & '''+str(Rtorquedev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(Rtorquemin[5])+r'''& '''+str(Rtorquemean[5])+r''' & '''+str(Rtorquemax[5])+r''' & '''+str(Rtorquedev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(Rtorquemin[6])+r'''& '''+str(Rtorquemean[6])+r''' & '''+str(Rtorquemax[6])+r''' & '''+str(Rtorquedev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(Rtorquemin[7])+r'''& '''+str(Rtorquemean[7])+r''' & '''+str(Rtorquemax[7])+r''' & '''+str(Rtorquedev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(Rtorquemin[8])+r'''& '''+str(Rtorquemean[8])+r''' & '''+str(Rtorquemax[8])+r''' & '''+str(Rtorquedev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(Rtorquemin[9])+r'''& '''+str(Rtorquemean[9])+r''' & '''+str(Rtorquemax[9])+r''' & '''+str(Rtorquedev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(Rtorquemin[10])+r'''& '''+str(Rtorquemean[10])+r''' & '''+str(Rtorquemax[10])+r''' & '''+str(Rtorquedev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(Rtorquemin[11])+r'''& '''+str(Rtorquemean[11])+r''' & '''+str(Rtorquemax[11])+r''' & '''+str(Rtorquedev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(Rtorquemin[12])+r'''& '''+str(Rtorquemean[12])+r''' & '''+str(Rtorquemax[12])+r''' & '''+str(Rtorquedev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(Rtorquemin[13])+r'''& '''+str(Rtorquemean[13])+r''' & '''+str(Rtorquemax[13])+r''' & '''+str(Rtorquedev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(Rtorquemin[14])+r'''& '''+str(Rtorquemean[14])+r''' & '''+str(Rtorquemax[14])+r''' & '''+str(Rtorquedev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(Rtorquemin[15])+r'''& '''+str(Rtorquemean[15])+r''' & '''+str(Rtorquemax[15])+r''' & '''+str(Rtorquedev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(Rtorquemin[16])+r'''& '''+str(Rtorquemean[16])+r''' & '''+str(Rtorquemax[16])+r''' & '''+str(Rtorquedev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(Rtorquemin[17])+r'''& '''+str(Rtorquemean[17])+r''' & '''+str(Rtorquemax[17])+r''' & '''+str(Rtorquedev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(Rtorquemin[18])+r'''& '''+str(Rtorquemean[18])+r''' & '''+str(Rtorquemax[18])+r''' & '''+str(Rtorquedev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(Rtorquemin[19])+r'''& '''+str(Rtorquemean[19])+r''' & '''+str(Rtorquemax[19])+r''' & '''+str(Rtorquedev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(Rtorquemin[20])+r'''& '''+str(Rtorquemean[20])+r''' & '''+str(Rtorquemax[20])+r''' & '''+str(Rtorquedev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(Rtorquemin[21])+r'''& '''+str(Rtorquemean[21])+r''' & '''+str(Rtorquemax[21])+r''' & '''+str(Rtorquedev[21])+r''' \\ \hline
            \end{tabular}
            \egroup
            \end{table}

            \newpage  

            \subsubsection{Tower base moments}

            Table \ref{tab:TowerBaseNormalMoment} shows the tower base normal moment.

            \begin{table}[H]
            \caption{Tower base normal moment}
            \label{tab:TowerBaseNormalMoment}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (kN.m)} & \textbf{Mean (kN.m)} & \textbf{Max (kN.m)} & \textbf{Std dev.(kN.m)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(TwrBsNmin[0])+r'''& '''+str(TwrBsNmean[0])+r''' & '''+str(TwrBsNmax[0])+r''' & '''+str(TwrBsNdev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(TwrBsNmin[1])+r'''& '''+str(TwrBsNmean[1])+r''' & '''+str(TwrBsNmax[1])+r''' & '''+str(TwrBsNdev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(TwrBsNmin[2])+r'''& '''+str(TwrBsNmean[2])+r''' & '''+str(TwrBsNmax[2])+r''' & '''+str(TwrBsNdev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(TwrBsNmin[3])+r'''& '''+str(TwrBsNmean[3])+r''' & '''+str(TwrBsNmax[3])+r''' & '''+str(TwrBsNdev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(TwrBsNmin[4])+r'''& '''+str(TwrBsNmean[4])+r''' & '''+str(TwrBsNmax[4])+r''' & '''+str(TwrBsNdev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(TwrBsNmin[5])+r'''& '''+str(TwrBsNmean[5])+r''' & '''+str(TwrBsNmax[5])+r''' & '''+str(TwrBsNdev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(TwrBsNmin[6])+r'''& '''+str(TwrBsNmean[6])+r''' & '''+str(TwrBsNmax[6])+r''' & '''+str(TwrBsNdev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(TwrBsNmin[7])+r'''& '''+str(TwrBsNmean[7])+r''' & '''+str(TwrBsNmax[7])+r''' & '''+str(TwrBsNdev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(TwrBsNmin[8])+r'''& '''+str(TwrBsNmean[8])+r''' & '''+str(TwrBsNmax[8])+r''' & '''+str(TwrBsNdev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(TwrBsNmin[9])+r'''& '''+str(TwrBsNmean[9])+r''' & '''+str(TwrBsNmax[9])+r''' & '''+str(TwrBsNdev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(TwrBsNmin[10])+r'''& '''+str(TwrBsNmean[10])+r''' & '''+str(TwrBsNmax[10])+r''' & '''+str(TwrBsNdev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(TwrBsNmin[11])+r'''& '''+str(TwrBsNmean[11])+r''' & '''+str(TwrBsNmax[11])+r''' & '''+str(TwrBsNdev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(TwrBsNmin[12])+r'''& '''+str(TwrBsNmean[12])+r''' & '''+str(TwrBsNmax[12])+r''' & '''+str(TwrBsNdev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(TwrBsNmin[13])+r'''& '''+str(TwrBsNmean[13])+r''' & '''+str(TwrBsNmax[13])+r''' & '''+str(TwrBsNdev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(TwrBsNmin[14])+r'''& '''+str(TwrBsNmean[14])+r''' & '''+str(TwrBsNmax[14])+r''' & '''+str(TwrBsNdev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(TwrBsNmin[15])+r'''& '''+str(TwrBsNmean[15])+r''' & '''+str(TwrBsNmax[15])+r''' & '''+str(TwrBsNdev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(TwrBsNmin[16])+r'''& '''+str(TwrBsNmean[16])+r''' & '''+str(TwrBsNmax[16])+r''' & '''+str(TwrBsNdev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(TwrBsNmin[17])+r'''& '''+str(TwrBsNmean[17])+r''' & '''+str(TwrBsNmax[17])+r''' & '''+str(TwrBsNdev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(TwrBsNmin[18])+r'''& '''+str(TwrBsNmean[18])+r''' & '''+str(TwrBsNmax[18])+r''' & '''+str(TwrBsNdev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(TwrBsNmin[19])+r'''& '''+str(TwrBsNmean[19])+r''' & '''+str(TwrBsNmax[19])+r''' & '''+str(TwrBsNdev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(TwrBsNmin[20])+r'''& '''+str(TwrBsNmean[20])+r''' & '''+str(TwrBsNmax[20])+r''' & '''+str(TwrBsNdev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(TwrBsNmin[21])+r'''& '''+str(TwrBsNmean[21])+r''' & '''+str(TwrBsNmax[21])+r''' & '''+str(TwrBsNdev[21])+r''' \\ \hline
            \end{tabular}
            \egroup
            \end{table}

            \newpage  

            Table \ref{tab:TowerBaseLateralMoment} shows the tower base lateral moment.

            \begin{table}[H]
            \caption{Tower base lateral moment}
            \label{tab:TowerBaseLateralMoment}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (kN.m)} & \textbf{Mean (kN.m)} & \textbf{Max (kN.m)} & \textbf{Std dev.(kN.m)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(TwrBsLmin[0])+r'''& '''+str(TwrBsLmean[0])+r''' & '''+str(TwrBsLmax[0])+r''' & '''+str(TwrBsLdev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(TwrBsLmin[1])+r'''& '''+str(TwrBsLmean[1])+r''' & '''+str(TwrBsLmax[1])+r''' & '''+str(TwrBsLdev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(TwrBsLmin[2])+r'''& '''+str(TwrBsLmean[2])+r''' & '''+str(TwrBsLmax[2])+r''' & '''+str(TwrBsLdev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(TwrBsLmin[3])+r'''& '''+str(TwrBsLmean[3])+r''' & '''+str(TwrBsLmax[3])+r''' & '''+str(TwrBsLdev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(TwrBsLmin[4])+r'''& '''+str(TwrBsLmean[4])+r''' & '''+str(TwrBsLmax[4])+r''' & '''+str(TwrBsLdev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(TwrBsLmin[5])+r'''& '''+str(TwrBsLmean[5])+r''' & '''+str(TwrBsLmax[5])+r''' & '''+str(TwrBsLdev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(TwrBsLmin[6])+r'''& '''+str(TwrBsLmean[6])+r''' & '''+str(TwrBsLmax[6])+r''' & '''+str(TwrBsLdev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(TwrBsLmin[7])+r'''& '''+str(TwrBsLmean[7])+r''' & '''+str(TwrBsLmax[7])+r''' & '''+str(TwrBsLdev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(TwrBsLmin[8])+r'''& '''+str(TwrBsLmean[8])+r''' & '''+str(TwrBsLmax[8])+r''' & '''+str(TwrBsLdev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(TwrBsLmin[9])+r'''& '''+str(TwrBsLmean[9])+r''' & '''+str(TwrBsLmax[9])+r''' & '''+str(TwrBsLdev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(TwrBsLmin[10])+r'''& '''+str(TwrBsLmean[10])+r''' & '''+str(TwrBsLmax[10])+r''' & '''+str(TwrBsLdev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(TwrBsLmin[11])+r'''& '''+str(TwrBsLmean[11])+r''' & '''+str(TwrBsLmax[11])+r''' & '''+str(TwrBsLdev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(TwrBsLmin[12])+r'''& '''+str(TwrBsLmean[12])+r''' & '''+str(TwrBsLmax[12])+r''' & '''+str(TwrBsLdev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(TwrBsLmin[13])+r'''& '''+str(TwrBsLmean[13])+r''' & '''+str(TwrBsLmax[13])+r''' & '''+str(TwrBsLdev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(TwrBsLmin[14])+r'''& '''+str(TwrBsLmean[14])+r''' & '''+str(TwrBsLmax[14])+r''' & '''+str(TwrBsLdev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(TwrBsLmin[15])+r'''& '''+str(TwrBsLmean[15])+r''' & '''+str(TwrBsLmax[15])+r''' & '''+str(TwrBsLdev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(TwrBsLmin[16])+r'''& '''+str(TwrBsLmean[16])+r''' & '''+str(TwrBsLmax[16])+r''' & '''+str(TwrBsLdev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(TwrBsLmin[17])+r'''& '''+str(TwrBsLmean[17])+r''' & '''+str(TwrBsLmax[17])+r''' & '''+str(TwrBsLdev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(TwrBsLmin[18])+r'''& '''+str(TwrBsLmean[18])+r''' & '''+str(TwrBsLmax[18])+r''' & '''+str(TwrBsLdev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(TwrBsLmin[19])+r'''& '''+str(TwrBsLmean[19])+r''' & '''+str(TwrBsLmax[19])+r''' & '''+str(TwrBsLdev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(TwrBsLmin[20])+r'''& '''+str(TwrBsLmean[20])+r''' & '''+str(TwrBsLmax[20])+r''' & '''+str(TwrBsLdev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(TwrBsLmin[21])+r'''& '''+str(TwrBsLmean[21])+r''' & '''+str(TwrBsLmax[21])+r''' & '''+str(TwrBsLdev[21])+r''' \\ \hline
            \end{tabular}
            \egroup
            \end{table}

            \newpage  

            Table \ref{tab:TowerTorque} shows the tower torque.
            
            \begin{table}[H]
            \caption{Tower torque}
            \label{tab:TowerTorque}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (kN.m)} & \textbf{Mean (kN.m)} & \textbf{Max (kN.m)} & \textbf{Std dev.(kN.m)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(TwrTqmin[0])+r'''& '''+str(TwrTqmean[0])+r''' & '''+str(TwrTqmax[0])+r''' & '''+str(TwrTqdev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(TwrTqmin[1])+r'''& '''+str(TwrTqmean[1])+r''' & '''+str(TwrTqmax[1])+r''' & '''+str(TwrTqdev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(TwrTqmin[2])+r'''& '''+str(TwrTqmean[2])+r''' & '''+str(TwrTqmax[2])+r''' & '''+str(TwrTqdev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(TwrTqmin[3])+r'''& '''+str(TwrTqmean[3])+r''' & '''+str(TwrTqmax[3])+r''' & '''+str(TwrTqdev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(TwrTqmin[4])+r'''& '''+str(TwrTqmean[4])+r''' & '''+str(TwrTqmax[4])+r''' & '''+str(TwrTqdev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(TwrTqmin[5])+r'''& '''+str(TwrTqmean[5])+r''' & '''+str(TwrTqmax[5])+r''' & '''+str(TwrTqdev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(TwrTqmin[6])+r'''& '''+str(TwrTqmean[6])+r''' & '''+str(TwrTqmax[6])+r''' & '''+str(TwrTqdev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(TwrTqmin[7])+r'''& '''+str(TwrTqmean[7])+r''' & '''+str(TwrTqmax[7])+r''' & '''+str(TwrTqdev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(TwrTqmin[8])+r'''& '''+str(TwrTqmean[8])+r''' & '''+str(TwrTqmax[8])+r''' & '''+str(TwrTqdev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(TwrTqmin[9])+r'''& '''+str(TwrTqmean[9])+r''' & '''+str(TwrTqmax[9])+r''' & '''+str(TwrTqdev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(TwrTqmin[10])+r'''& '''+str(TwrTqmean[10])+r''' & '''+str(TwrTqmax[10])+r''' & '''+str(TwrTqdev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(TwrTqmin[11])+r'''& '''+str(TwrTqmean[11])+r''' & '''+str(TwrTqmax[11])+r''' & '''+str(TwrTqdev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(TwrTqmin[12])+r'''& '''+str(TwrTqmean[12])+r''' & '''+str(TwrTqmax[12])+r''' & '''+str(TwrTqdev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(TwrTqmin[13])+r'''& '''+str(TwrTqmean[13])+r''' & '''+str(TwrTqmax[13])+r''' & '''+str(TwrTqdev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(TwrTqmin[14])+r'''& '''+str(TwrTqmean[14])+r''' & '''+str(TwrTqmax[14])+r''' & '''+str(TwrTqdev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(TwrTqmin[15])+r'''& '''+str(TwrTqmean[15])+r''' & '''+str(TwrTqmax[15])+r''' & '''+str(TwrTqdev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(TwrTqmin[16])+r'''& '''+str(TwrTqmean[16])+r''' & '''+str(TwrTqmax[16])+r''' & '''+str(TwrTqdev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(TwrTqmin[17])+r'''& '''+str(TwrTqmean[17])+r''' & '''+str(TwrTqmax[17])+r''' & '''+str(TwrTqdev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(TwrTqmin[18])+r'''& '''+str(TwrTqmean[18])+r''' & '''+str(TwrTqmax[18])+r''' & '''+str(TwrTqdev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(TwrTqmin[19])+r'''& '''+str(TwrTqmean[19])+r''' & '''+str(TwrTqmax[19])+r''' & '''+str(TwrTqdev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(TwrTqmin[20])+r'''& '''+str(TwrTqmean[20])+r''' & '''+str(TwrTqmax[20])+r''' & '''+str(TwrTqdev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(TwrTqmin[21])+r'''& '''+str(TwrTqmean[21])+r''' & '''+str(TwrTqmax[21])+r''' & '''+str(TwrTqdev[21])+r''' \\ \hline
            \end{tabular}
            \egroup
            \end{table}

            \newpage  

            \subsubsection{Pitch actuation loads}

            Table \ref{tab:PitchActLoad1} shows the pitch actuation load at blade 1.

            \begin{table}[H]
            \caption{Blade 1 pitch actuation load}
            \label{tab:PitchActLoad1}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (kN.m)} & \textbf{Mean (kN.m)} & \textbf{Max (kN.m)} & \textbf{Std dev.(kN.m)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(pitchactuationload1min[0])+r'''& '''+str(pitchactuationload1mean[0])+r''' & '''+str(pitchactuationload1max[0])+r''' & '''+str(pitchactuationload1dev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(pitchactuationload1min[1])+r'''& '''+str(pitchactuationload1mean[1])+r''' & '''+str(pitchactuationload1max[1])+r''' & '''+str(pitchactuationload1dev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(pitchactuationload1min[2])+r'''& '''+str(pitchactuationload1mean[2])+r''' & '''+str(pitchactuationload1max[2])+r''' & '''+str(pitchactuationload1dev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(pitchactuationload1min[3])+r'''& '''+str(pitchactuationload1mean[3])+r''' & '''+str(pitchactuationload1max[3])+r''' & '''+str(pitchactuationload1dev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(pitchactuationload1min[4])+r'''& '''+str(pitchactuationload1mean[4])+r''' & '''+str(pitchactuationload1max[4])+r''' & '''+str(pitchactuationload1dev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(pitchactuationload1min[5])+r'''& '''+str(pitchactuationload1mean[5])+r''' & '''+str(pitchactuationload1max[5])+r''' & '''+str(pitchactuationload1dev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(pitchactuationload1min[6])+r'''& '''+str(pitchactuationload1mean[6])+r''' & '''+str(pitchactuationload1max[6])+r''' & '''+str(pitchactuationload1dev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(pitchactuationload1min[7])+r'''& '''+str(pitchactuationload1mean[7])+r''' & '''+str(pitchactuationload1max[7])+r''' & '''+str(pitchactuationload1dev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(pitchactuationload1min[8])+r'''& '''+str(pitchactuationload1mean[8])+r''' & '''+str(pitchactuationload1max[8])+r''' & '''+str(pitchactuationload1dev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(pitchactuationload1min[9])+r'''& '''+str(pitchactuationload1mean[9])+r''' & '''+str(pitchactuationload1max[9])+r''' & '''+str(pitchactuationload1dev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(pitchactuationload1min[10])+r'''& '''+str(pitchactuationload1mean[10])+r''' & '''+str(pitchactuationload1max[10])+r''' & '''+str(pitchactuationload1dev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(pitchactuationload1min[11])+r'''& '''+str(pitchactuationload1mean[11])+r''' & '''+str(pitchactuationload1max[11])+r''' & '''+str(pitchactuationload1dev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(pitchactuationload1min[12])+r'''& '''+str(pitchactuationload1mean[12])+r''' & '''+str(pitchactuationload1max[12])+r''' & '''+str(pitchactuationload1dev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(pitchactuationload1min[13])+r'''& '''+str(pitchactuationload1mean[13])+r''' & '''+str(pitchactuationload1max[13])+r''' & '''+str(pitchactuationload1dev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(pitchactuationload1min[14])+r'''& '''+str(pitchactuationload1mean[14])+r''' & '''+str(pitchactuationload1max[14])+r''' & '''+str(pitchactuationload1dev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(pitchactuationload1min[15])+r'''& '''+str(pitchactuationload1mean[15])+r''' & '''+str(pitchactuationload1max[15])+r''' & '''+str(pitchactuationload1dev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(pitchactuationload1min[16])+r'''& '''+str(pitchactuationload1mean[16])+r''' & '''+str(pitchactuationload1max[16])+r''' & '''+str(pitchactuationload1dev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(pitchactuationload1min[17])+r'''& '''+str(pitchactuationload1mean[17])+r''' & '''+str(pitchactuationload1max[17])+r''' & '''+str(pitchactuationload1dev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(pitchactuationload1min[18])+r'''& '''+str(pitchactuationload1mean[18])+r''' & '''+str(pitchactuationload1max[18])+r''' & '''+str(pitchactuationload1dev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(pitchactuationload1min[19])+r'''& '''+str(pitchactuationload1mean[19])+r''' & '''+str(pitchactuationload1max[19])+r''' & '''+str(pitchactuationload1dev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(pitchactuationload1min[20])+r'''& '''+str(pitchactuationload1mean[20])+r''' & '''+str(pitchactuationload1max[20])+r''' & '''+str(pitchactuationload1dev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(pitchactuationload1min[21])+r'''& '''+str(pitchactuationload1mean[21])+r''' & '''+str(pitchactuationload1max[21])+r''' & '''+str(pitchactuationload1dev[21])+r''' \\ \hline
            \end{tabular}
            \egroup
            \end{table}

            \newpage  

            Table \ref{tab:PitchActLoad2} shows the pitch actuation load at blade 2.

            \begin{table}[H]
            \caption{Blade 2 pitch actuation load}
            \label{tab:PitchActLoad2}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (kN.m)} & \textbf{Mean (kN.m)} & \textbf{Max (kN.m)} & \textbf{Std dev.(kN.m)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(pitchactuationload2min[0])+r'''& '''+str(pitchactuationload2mean[0])+r''' & '''+str(pitchactuationload2max[0])+r''' & '''+str(pitchactuationload2dev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(pitchactuationload2min[1])+r'''& '''+str(pitchactuationload2mean[1])+r''' & '''+str(pitchactuationload2max[1])+r''' & '''+str(pitchactuationload2dev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(pitchactuationload2min[2])+r'''& '''+str(pitchactuationload2mean[2])+r''' & '''+str(pitchactuationload2max[2])+r''' & '''+str(pitchactuationload2dev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(pitchactuationload2min[3])+r'''& '''+str(pitchactuationload2mean[3])+r''' & '''+str(pitchactuationload2max[3])+r''' & '''+str(pitchactuationload2dev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(pitchactuationload2min[4])+r'''& '''+str(pitchactuationload2mean[4])+r''' & '''+str(pitchactuationload2max[4])+r''' & '''+str(pitchactuationload2dev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(pitchactuationload2min[5])+r'''& '''+str(pitchactuationload2mean[5])+r''' & '''+str(pitchactuationload2max[5])+r''' & '''+str(pitchactuationload2dev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(pitchactuationload2min[6])+r'''& '''+str(pitchactuationload2mean[6])+r''' & '''+str(pitchactuationload2max[6])+r''' & '''+str(pitchactuationload2dev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(pitchactuationload2min[7])+r'''& '''+str(pitchactuationload2mean[7])+r''' & '''+str(pitchactuationload2max[7])+r''' & '''+str(pitchactuationload2dev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(pitchactuationload2min[8])+r'''& '''+str(pitchactuationload2mean[8])+r''' & '''+str(pitchactuationload2max[8])+r''' & '''+str(pitchactuationload2dev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(pitchactuationload2min[9])+r'''& '''+str(pitchactuationload2mean[9])+r''' & '''+str(pitchactuationload2max[9])+r''' & '''+str(pitchactuationload2dev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(pitchactuationload2min[10])+r'''& '''+str(pitchactuationload2mean[10])+r''' & '''+str(pitchactuationload2max[10])+r''' & '''+str(pitchactuationload2dev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(pitchactuationload2min[11])+r'''& '''+str(pitchactuationload2mean[11])+r''' & '''+str(pitchactuationload2max[11])+r''' & '''+str(pitchactuationload2dev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(pitchactuationload2min[12])+r'''& '''+str(pitchactuationload2mean[12])+r''' & '''+str(pitchactuationload2max[12])+r''' & '''+str(pitchactuationload2dev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(pitchactuationload2min[13])+r'''& '''+str(pitchactuationload2mean[13])+r''' & '''+str(pitchactuationload2max[13])+r''' & '''+str(pitchactuationload2dev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(pitchactuationload2min[14])+r'''& '''+str(pitchactuationload2mean[14])+r''' & '''+str(pitchactuationload2max[14])+r''' & '''+str(pitchactuationload2dev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(pitchactuationload2min[15])+r'''& '''+str(pitchactuationload2mean[15])+r''' & '''+str(pitchactuationload2max[15])+r''' & '''+str(pitchactuationload2dev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(pitchactuationload2min[16])+r'''& '''+str(pitchactuationload2mean[16])+r''' & '''+str(pitchactuationload2max[16])+r''' & '''+str(pitchactuationload2dev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(pitchactuationload2min[17])+r'''& '''+str(pitchactuationload2mean[17])+r''' & '''+str(pitchactuationload2max[17])+r''' & '''+str(pitchactuationload2dev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(pitchactuationload2min[18])+r'''& '''+str(pitchactuationload2mean[18])+r''' & '''+str(pitchactuationload2max[18])+r''' & '''+str(pitchactuationload2dev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(pitchactuationload2min[19])+r'''& '''+str(pitchactuationload2mean[19])+r''' & '''+str(pitchactuationload2max[19])+r''' & '''+str(pitchactuationload2dev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(pitchactuationload2min[20])+r'''& '''+str(pitchactuationload2mean[20])+r''' & '''+str(pitchactuationload2max[20])+r''' & '''+str(pitchactuationload2dev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(pitchactuationload2min[21])+r'''& '''+str(pitchactuationload2mean[21])+r''' & '''+str(pitchactuationload2max[21])+r''' & '''+str(pitchactuationload2dev[21])+r''' \\ \hline
            \end{tabular}
            \egroup
            \end{table}

            \newpage  

            Table \ref{tab:PitchActLoad3} shows the pitch actuation load at blade 3.

            \begin{table}[H]
            \caption{Blade 3 pitch actuation load}
            \label{tab:PitchActLoad3}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (kN.m)} & \textbf{Mean (kN.m)} & \textbf{Max (kN.m)} & \textbf{Std dev.(kN.m)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(pitchactuationload3min[0])+r'''& '''+str(pitchactuationload3mean[0])+r''' & '''+str(pitchactuationload3max[0])+r''' & '''+str(pitchactuationload3dev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(pitchactuationload3min[1])+r'''& '''+str(pitchactuationload3mean[1])+r''' & '''+str(pitchactuationload3max[1])+r''' & '''+str(pitchactuationload3dev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(pitchactuationload3min[2])+r'''& '''+str(pitchactuationload3mean[2])+r''' & '''+str(pitchactuationload3max[2])+r''' & '''+str(pitchactuationload3dev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(pitchactuationload3min[3])+r'''& '''+str(pitchactuationload3mean[3])+r''' & '''+str(pitchactuationload3max[3])+r''' & '''+str(pitchactuationload3dev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(pitchactuationload3min[4])+r'''& '''+str(pitchactuationload3mean[4])+r''' & '''+str(pitchactuationload3max[4])+r''' & '''+str(pitchactuationload3dev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(pitchactuationload3min[5])+r'''& '''+str(pitchactuationload3mean[5])+r''' & '''+str(pitchactuationload3max[5])+r''' & '''+str(pitchactuationload3dev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(pitchactuationload3min[6])+r'''& '''+str(pitchactuationload3mean[6])+r''' & '''+str(pitchactuationload3max[6])+r''' & '''+str(pitchactuationload3dev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(pitchactuationload3min[7])+r'''& '''+str(pitchactuationload3mean[7])+r''' & '''+str(pitchactuationload3max[7])+r''' & '''+str(pitchactuationload3dev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(pitchactuationload3min[8])+r'''& '''+str(pitchactuationload3mean[8])+r''' & '''+str(pitchactuationload3max[8])+r''' & '''+str(pitchactuationload3dev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(pitchactuationload3min[9])+r'''& '''+str(pitchactuationload3mean[9])+r''' & '''+str(pitchactuationload3max[9])+r''' & '''+str(pitchactuationload3dev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(pitchactuationload3min[10])+r'''& '''+str(pitchactuationload3mean[10])+r''' & '''+str(pitchactuationload3max[10])+r''' & '''+str(pitchactuationload3dev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(pitchactuationload3min[11])+r'''& '''+str(pitchactuationload3mean[11])+r''' & '''+str(pitchactuationload3max[11])+r''' & '''+str(pitchactuationload3dev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(pitchactuationload3min[12])+r'''& '''+str(pitchactuationload3mean[12])+r''' & '''+str(pitchactuationload3max[12])+r''' & '''+str(pitchactuationload3dev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(pitchactuationload3min[13])+r'''& '''+str(pitchactuationload3mean[13])+r''' & '''+str(pitchactuationload3max[13])+r''' & '''+str(pitchactuationload3dev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(pitchactuationload3min[14])+r'''& '''+str(pitchactuationload3mean[14])+r''' & '''+str(pitchactuationload3max[14])+r''' & '''+str(pitchactuationload3dev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(pitchactuationload3min[15])+r'''& '''+str(pitchactuationload3mean[15])+r''' & '''+str(pitchactuationload3max[15])+r''' & '''+str(pitchactuationload3dev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(pitchactuationload3min[16])+r'''& '''+str(pitchactuationload3mean[16])+r''' & '''+str(pitchactuationload3max[16])+r''' & '''+str(pitchactuationload3dev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(pitchactuationload3min[17])+r'''& '''+str(pitchactuationload3mean[17])+r''' & '''+str(pitchactuationload3max[17])+r''' & '''+str(pitchactuationload3dev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(pitchactuationload3min[18])+r'''& '''+str(pitchactuationload3mean[18])+r''' & '''+str(pitchactuationload3max[18])+r''' & '''+str(pitchactuationload3dev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(pitchactuationload3min[19])+r'''& '''+str(pitchactuationload3mean[19])+r''' & '''+str(pitchactuationload3max[19])+r''' & '''+str(pitchactuationload3dev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(pitchactuationload3min[20])+r'''& '''+str(pitchactuationload3mean[20])+r''' & '''+str(pitchactuationload3max[20])+r''' & '''+str(pitchactuationload3dev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(pitchactuationload3min[21])+r'''& '''+str(pitchactuationload3mean[21])+r''' & '''+str(pitchactuationload3max[21])+r''' & '''+str(pitchactuationload3dev[21])+r''' \\ \hline
            \end{tabular}
            \egroup
            \end{table}

            \newpage  

            \subsubsection{Tower top accelerations}

            Table \ref{tab:TowerTopAccNormal} shows the tower top acceleration in normal direction.

            \begin{table}[H]
            \caption{Tower top acceleration in normal direction}
            \label{tab:TowerTopAccNormal}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (m/s2)} & \textbf{Mean (m/s2)} & \textbf{Max (m/s2)} & \textbf{Std dev.(m/s2)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(TwrTopAccNormalmin[0])+r'''& '''+str(TwrTopAccNormalmean[0])+r''' & '''+str(TwrTopAccNormalmax[0])+r''' & '''+str(TwrTopAccNormaldev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(TwrTopAccNormalmin[1])+r'''& '''+str(TwrTopAccNormalmean[1])+r''' & '''+str(TwrTopAccNormalmax[1])+r''' & '''+str(TwrTopAccNormaldev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(TwrTopAccNormalmin[2])+r'''& '''+str(TwrTopAccNormalmean[2])+r''' & '''+str(TwrTopAccNormalmax[2])+r''' & '''+str(TwrTopAccNormaldev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(TwrTopAccNormalmin[3])+r'''& '''+str(TwrTopAccNormalmean[3])+r''' & '''+str(TwrTopAccNormalmax[3])+r''' & '''+str(TwrTopAccNormaldev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(TwrTopAccNormalmin[4])+r'''& '''+str(TwrTopAccNormalmean[4])+r''' & '''+str(TwrTopAccNormalmax[4])+r''' & '''+str(TwrTopAccNormaldev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(TwrTopAccNormalmin[5])+r'''& '''+str(TwrTopAccNormalmean[5])+r''' & '''+str(TwrTopAccNormalmax[5])+r''' & '''+str(TwrTopAccNormaldev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(TwrTopAccNormalmin[6])+r'''& '''+str(TwrTopAccNormalmean[6])+r''' & '''+str(TwrTopAccNormalmax[6])+r''' & '''+str(TwrTopAccNormaldev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(TwrTopAccNormalmin[7])+r'''& '''+str(TwrTopAccNormalmean[7])+r''' & '''+str(TwrTopAccNormalmax[7])+r''' & '''+str(TwrTopAccNormaldev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(TwrTopAccNormalmin[8])+r'''& '''+str(TwrTopAccNormalmean[8])+r''' & '''+str(TwrTopAccNormalmax[8])+r''' & '''+str(TwrTopAccNormaldev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(TwrTopAccNormalmin[9])+r'''& '''+str(TwrTopAccNormalmean[9])+r''' & '''+str(TwrTopAccNormalmax[9])+r''' & '''+str(TwrTopAccNormaldev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(TwrTopAccNormalmin[10])+r'''& '''+str(TwrTopAccNormalmean[10])+r''' & '''+str(TwrTopAccNormalmax[10])+r''' & '''+str(TwrTopAccNormaldev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(TwrTopAccNormalmin[11])+r'''& '''+str(TwrTopAccNormalmean[11])+r''' & '''+str(TwrTopAccNormalmax[11])+r''' & '''+str(TwrTopAccNormaldev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(TwrTopAccNormalmin[12])+r'''& '''+str(TwrTopAccNormalmean[12])+r''' & '''+str(TwrTopAccNormalmax[12])+r''' & '''+str(TwrTopAccNormaldev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(TwrTopAccNormalmin[13])+r'''& '''+str(TwrTopAccNormalmean[13])+r''' & '''+str(TwrTopAccNormalmax[13])+r''' & '''+str(TwrTopAccNormaldev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(TwrTopAccNormalmin[14])+r'''& '''+str(TwrTopAccNormalmean[14])+r''' & '''+str(TwrTopAccNormalmax[14])+r''' & '''+str(TwrTopAccNormaldev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(TwrTopAccNormalmin[15])+r'''& '''+str(TwrTopAccNormalmean[15])+r''' & '''+str(TwrTopAccNormalmax[15])+r''' & '''+str(TwrTopAccNormaldev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(TwrTopAccNormalmin[16])+r'''& '''+str(TwrTopAccNormalmean[16])+r''' & '''+str(TwrTopAccNormalmax[16])+r''' & '''+str(TwrTopAccNormaldev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(TwrTopAccNormalmin[17])+r'''& '''+str(TwrTopAccNormalmean[17])+r''' & '''+str(TwrTopAccNormalmax[17])+r''' & '''+str(TwrTopAccNormaldev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(TwrTopAccNormalmin[18])+r'''& '''+str(TwrTopAccNormalmean[18])+r''' & '''+str(TwrTopAccNormalmax[18])+r''' & '''+str(TwrTopAccNormaldev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(TwrTopAccNormalmin[19])+r'''& '''+str(TwrTopAccNormalmean[19])+r''' & '''+str(TwrTopAccNormalmax[19])+r''' & '''+str(TwrTopAccNormaldev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(TwrTopAccNormalmin[20])+r'''& '''+str(TwrTopAccNormalmean[20])+r''' & '''+str(TwrTopAccNormalmax[20])+r''' & '''+str(TwrTopAccNormaldev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(TwrTopAccNormalmin[21])+r'''& '''+str(TwrTopAccNormalmean[21])+r''' & '''+str(TwrTopAccNormalmax[21])+r''' & '''+str(TwrTopAccNormaldev[21])+r''' \\ \hline
            \end{tabular}
            \egroup
            \end{table}

            \newpage  

            Table \ref{tab:TowerTopAccLat} shows the tower top acceleration in lateral direction.

            \begin{table}[H]
            \caption{Tower top acceleration in lateral direction}
            \label{tab:TowerTopAccLat}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (m/s2)} & \textbf{Mean (m/s2)} & \textbf{Max (m/s2)} & \textbf{Std dev.(m/s2)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(TwrTopAccLatmin[0])+r'''& '''+str(TwrTopAccLatmean[0])+r''' & '''+str(TwrTopAccLatmax[0])+r''' & '''+str(TwrTopAccLatdev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(TwrTopAccLatmin[1])+r'''& '''+str(TwrTopAccLatmean[1])+r''' & '''+str(TwrTopAccLatmax[1])+r''' & '''+str(TwrTopAccLatdev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(TwrTopAccLatmin[2])+r'''& '''+str(TwrTopAccLatmean[2])+r''' & '''+str(TwrTopAccLatmax[2])+r''' & '''+str(TwrTopAccLatdev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(TwrTopAccLatmin[3])+r'''& '''+str(TwrTopAccLatmean[3])+r''' & '''+str(TwrTopAccLatmax[3])+r''' & '''+str(TwrTopAccLatdev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(TwrTopAccLatmin[4])+r'''& '''+str(TwrTopAccLatmean[4])+r''' & '''+str(TwrTopAccLatmax[4])+r''' & '''+str(TwrTopAccLatdev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(TwrTopAccLatmin[5])+r'''& '''+str(TwrTopAccLatmean[5])+r''' & '''+str(TwrTopAccLatmax[5])+r''' & '''+str(TwrTopAccLatdev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(TwrTopAccLatmin[6])+r'''& '''+str(TwrTopAccLatmean[6])+r''' & '''+str(TwrTopAccLatmax[6])+r''' & '''+str(TwrTopAccLatdev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(TwrTopAccLatmin[7])+r'''& '''+str(TwrTopAccLatmean[7])+r''' & '''+str(TwrTopAccLatmax[7])+r''' & '''+str(TwrTopAccLatdev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(TwrTopAccLatmin[8])+r'''& '''+str(TwrTopAccLatmean[8])+r''' & '''+str(TwrTopAccLatmax[8])+r''' & '''+str(TwrTopAccLatdev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(TwrTopAccLatmin[9])+r'''& '''+str(TwrTopAccLatmean[9])+r''' & '''+str(TwrTopAccLatmax[9])+r''' & '''+str(TwrTopAccLatdev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(TwrTopAccLatmin[10])+r'''& '''+str(TwrTopAccLatmean[10])+r''' & '''+str(TwrTopAccLatmax[10])+r''' & '''+str(TwrTopAccLatdev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(TwrTopAccLatmin[11])+r'''& '''+str(TwrTopAccLatmean[11])+r''' & '''+str(TwrTopAccLatmax[11])+r''' & '''+str(TwrTopAccLatdev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(TwrTopAccLatmin[12])+r'''& '''+str(TwrTopAccLatmean[12])+r''' & '''+str(TwrTopAccLatmax[12])+r''' & '''+str(TwrTopAccLatdev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(TwrTopAccLatmin[13])+r'''& '''+str(TwrTopAccLatmean[13])+r''' & '''+str(TwrTopAccLatmax[13])+r''' & '''+str(TwrTopAccLatdev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(TwrTopAccLatmin[14])+r'''& '''+str(TwrTopAccLatmean[14])+r''' & '''+str(TwrTopAccLatmax[14])+r''' & '''+str(TwrTopAccLatdev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(TwrTopAccLatmin[15])+r'''& '''+str(TwrTopAccLatmean[15])+r''' & '''+str(TwrTopAccLatmax[15])+r''' & '''+str(TwrTopAccLatdev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(TwrTopAccLatmin[16])+r'''& '''+str(TwrTopAccLatmean[16])+r''' & '''+str(TwrTopAccLatmax[16])+r''' & '''+str(TwrTopAccLatdev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(TwrTopAccLatmin[17])+r'''& '''+str(TwrTopAccLatmean[17])+r''' & '''+str(TwrTopAccLatmax[17])+r''' & '''+str(TwrTopAccLatdev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(TwrTopAccLatmin[18])+r'''& '''+str(TwrTopAccLatmean[18])+r''' & '''+str(TwrTopAccLatmax[18])+r''' & '''+str(TwrTopAccLatdev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(TwrTopAccLatmin[19])+r'''& '''+str(TwrTopAccLatmean[19])+r''' & '''+str(TwrTopAccLatmax[19])+r''' & '''+str(TwrTopAccLatdev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(TwrTopAccLatmin[20])+r'''& '''+str(TwrTopAccLatmean[20])+r''' & '''+str(TwrTopAccLatmax[20])+r''' & '''+str(TwrTopAccLatdev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(TwrTopAccLatmin[21])+r'''& '''+str(TwrTopAccLatmean[21])+r''' & '''+str(TwrTopAccLatmax[21])+r''' & '''+str(TwrTopAccLatdev[21])+r''' \\ \hline
            \end{tabular}
            \egroup
            \end{table}

            \newpage  

            \subsubsection{Tower top moments}

            Table \ref{tab:TowerTopNormal} shows the tower top normal moment.

            \begin{table}[H]
            \caption{Tower top normal moment}
            \label{tab:TowerTopNormal}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (kN.m)} & \textbf{Mean (kN.m)} & \textbf{Max (kN.m)} & \textbf{Std dev.(kN.m)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(TwrTopMomentNormalmin[0])+r'''& '''+str(TwrTopMomentNormalmean[0])+r''' & '''+str(TwrTopMomentNormalmax[0])+r''' & '''+str(TwrTopMomentNormaldev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(TwrTopMomentNormalmin[1])+r'''& '''+str(TwrTopMomentNormalmean[1])+r''' & '''+str(TwrTopMomentNormalmax[1])+r''' & '''+str(TwrTopMomentNormaldev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(TwrTopMomentNormalmin[2])+r'''& '''+str(TwrTopMomentNormalmean[2])+r''' & '''+str(TwrTopMomentNormalmax[2])+r''' & '''+str(TwrTopMomentNormaldev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(TwrTopMomentNormalmin[3])+r'''& '''+str(TwrTopMomentNormalmean[3])+r''' & '''+str(TwrTopMomentNormalmax[3])+r''' & '''+str(TwrTopMomentNormaldev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(TwrTopMomentNormalmin[4])+r'''& '''+str(TwrTopMomentNormalmean[4])+r''' & '''+str(TwrTopMomentNormalmax[4])+r''' & '''+str(TwrTopMomentNormaldev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(TwrTopMomentNormalmin[5])+r'''& '''+str(TwrTopMomentNormalmean[5])+r''' & '''+str(TwrTopMomentNormalmax[5])+r''' & '''+str(TwrTopMomentNormaldev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(TwrTopMomentNormalmin[6])+r'''& '''+str(TwrTopMomentNormalmean[6])+r''' & '''+str(TwrTopMomentNormalmax[6])+r''' & '''+str(TwrTopMomentNormaldev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(TwrTopMomentNormalmin[7])+r'''& '''+str(TwrTopMomentNormalmean[7])+r''' & '''+str(TwrTopMomentNormalmax[7])+r''' & '''+str(TwrTopMomentNormaldev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(TwrTopMomentNormalmin[8])+r'''& '''+str(TwrTopMomentNormalmean[8])+r''' & '''+str(TwrTopMomentNormalmax[8])+r''' & '''+str(TwrTopMomentNormaldev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(TwrTopMomentNormalmin[9])+r'''& '''+str(TwrTopMomentNormalmean[9])+r''' & '''+str(TwrTopMomentNormalmax[9])+r''' & '''+str(TwrTopMomentNormaldev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(TwrTopMomentNormalmin[10])+r'''& '''+str(TwrTopMomentNormalmean[10])+r''' & '''+str(TwrTopMomentNormalmax[10])+r''' & '''+str(TwrTopMomentNormaldev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(TwrTopMomentNormalmin[11])+r'''& '''+str(TwrTopMomentNormalmean[11])+r''' & '''+str(TwrTopMomentNormalmax[11])+r''' & '''+str(TwrTopMomentNormaldev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(TwrTopMomentNormalmin[12])+r'''& '''+str(TwrTopMomentNormalmean[12])+r''' & '''+str(TwrTopMomentNormalmax[12])+r''' & '''+str(TwrTopMomentNormaldev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(TwrTopMomentNormalmin[13])+r'''& '''+str(TwrTopMomentNormalmean[13])+r''' & '''+str(TwrTopMomentNormalmax[13])+r''' & '''+str(TwrTopMomentNormaldev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(TwrTopMomentNormalmin[14])+r'''& '''+str(TwrTopMomentNormalmean[14])+r''' & '''+str(TwrTopMomentNormalmax[14])+r''' & '''+str(TwrTopMomentNormaldev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(TwrTopMomentNormalmin[15])+r'''& '''+str(TwrTopMomentNormalmean[15])+r''' & '''+str(TwrTopMomentNormalmax[15])+r''' & '''+str(TwrTopMomentNormaldev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(TwrTopMomentNormalmin[16])+r'''& '''+str(TwrTopMomentNormalmean[16])+r''' & '''+str(TwrTopMomentNormalmax[16])+r''' & '''+str(TwrTopMomentNormaldev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(TwrTopMomentNormalmin[17])+r'''& '''+str(TwrTopMomentNormalmean[17])+r''' & '''+str(TwrTopMomentNormalmax[17])+r''' & '''+str(TwrTopMomentNormaldev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(TwrTopMomentNormalmin[18])+r'''& '''+str(TwrTopMomentNormalmean[18])+r''' & '''+str(TwrTopMomentNormalmax[18])+r''' & '''+str(TwrTopMomentNormaldev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(TwrTopMomentNormalmin[19])+r'''& '''+str(TwrTopMomentNormalmean[19])+r''' & '''+str(TwrTopMomentNormalmax[19])+r''' & '''+str(TwrTopMomentNormaldev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(TwrTopMomentNormalmin[20])+r'''& '''+str(TwrTopMomentNormalmean[20])+r''' & '''+str(TwrTopMomentNormalmax[20])+r''' & '''+str(TwrTopMomentNormaldev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(TwrTopMomentNormalmin[21])+r'''& '''+str(TwrTopMomentNormalmean[21])+r''' & '''+str(TwrTopMomentNormalmax[21])+r''' & '''+str(TwrTopMomentNormaldev[21])+r''' \\ \hline
            \end{tabular}
            \egroup
            \end{table}

            \newpage  

            Table \ref{tab:TowerTopLateral} shows the tower top lateral moment.

            \begin{table}[H]
            \caption{Tower top lateral}
            \label{tab:TowerTopLateral}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (kN.m)} & \textbf{Mean (kN.m)} & \textbf{Max (kN.m)} & \textbf{Std dev.(kN.m)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(TwrTopMomentLateralmin[0])+r'''& '''+str(TwrTopMomentLateralmean[0])+r''' & '''+str(TwrTopMomentLateralmax[0])+r''' & '''+str(TwrTopMomentLateraldev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(TwrTopMomentLateralmin[1])+r'''& '''+str(TwrTopMomentLateralmean[1])+r''' & '''+str(TwrTopMomentLateralmax[1])+r''' & '''+str(TwrTopMomentLateraldev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(TwrTopMomentLateralmin[2])+r'''& '''+str(TwrTopMomentLateralmean[2])+r''' & '''+str(TwrTopMomentLateralmax[2])+r''' & '''+str(TwrTopMomentLateraldev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(TwrTopMomentLateralmin[3])+r'''& '''+str(TwrTopMomentLateralmean[3])+r''' & '''+str(TwrTopMomentLateralmax[3])+r''' & '''+str(TwrTopMomentLateraldev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(TwrTopMomentLateralmin[4])+r'''& '''+str(TwrTopMomentLateralmean[4])+r''' & '''+str(TwrTopMomentLateralmax[4])+r''' & '''+str(TwrTopMomentLateraldev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(TwrTopMomentLateralmin[5])+r'''& '''+str(TwrTopMomentLateralmean[5])+r''' & '''+str(TwrTopMomentLateralmax[5])+r''' & '''+str(TwrTopMomentLateraldev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(TwrTopMomentLateralmin[6])+r'''& '''+str(TwrTopMomentLateralmean[6])+r''' & '''+str(TwrTopMomentLateralmax[6])+r''' & '''+str(TwrTopMomentLateraldev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(TwrTopMomentLateralmin[7])+r'''& '''+str(TwrTopMomentLateralmean[7])+r''' & '''+str(TwrTopMomentLateralmax[7])+r''' & '''+str(TwrTopMomentLateraldev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(TwrTopMomentLateralmin[8])+r'''& '''+str(TwrTopMomentLateralmean[8])+r''' & '''+str(TwrTopMomentLateralmax[8])+r''' & '''+str(TwrTopMomentLateraldev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(TwrTopMomentLateralmin[9])+r'''& '''+str(TwrTopMomentLateralmean[9])+r''' & '''+str(TwrTopMomentLateralmax[9])+r''' & '''+str(TwrTopMomentLateraldev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(TwrTopMomentLateralmin[10])+r'''& '''+str(TwrTopMomentLateralmean[10])+r''' & '''+str(TwrTopMomentLateralmax[10])+r''' & '''+str(TwrTopMomentLateraldev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(TwrTopMomentLateralmin[11])+r'''& '''+str(TwrTopMomentLateralmean[11])+r''' & '''+str(TwrTopMomentLateralmax[11])+r''' & '''+str(TwrTopMomentLateraldev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(TwrTopMomentLateralmin[12])+r'''& '''+str(TwrTopMomentLateralmean[12])+r''' & '''+str(TwrTopMomentLateralmax[12])+r''' & '''+str(TwrTopMomentLateraldev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(TwrTopMomentLateralmin[13])+r'''& '''+str(TwrTopMomentLateralmean[13])+r''' & '''+str(TwrTopMomentLateralmax[13])+r''' & '''+str(TwrTopMomentLateraldev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(TwrTopMomentLateralmin[14])+r'''& '''+str(TwrTopMomentLateralmean[14])+r''' & '''+str(TwrTopMomentLateralmax[14])+r''' & '''+str(TwrTopMomentLateraldev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(TwrTopMomentLateralmin[15])+r'''& '''+str(TwrTopMomentLateralmean[15])+r''' & '''+str(TwrTopMomentLateralmax[15])+r''' & '''+str(TwrTopMomentLateraldev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(TwrTopMomentLateralmin[16])+r'''& '''+str(TwrTopMomentLateralmean[16])+r''' & '''+str(TwrTopMomentLateralmax[16])+r''' & '''+str(TwrTopMomentLateraldev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(TwrTopMomentLateralmin[17])+r'''& '''+str(TwrTopMomentLateralmean[17])+r''' & '''+str(TwrTopMomentLateralmax[17])+r''' & '''+str(TwrTopMomentLateraldev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(TwrTopMomentLateralmin[18])+r'''& '''+str(TwrTopMomentLateralmean[18])+r''' & '''+str(TwrTopMomentLateralmax[18])+r''' & '''+str(TwrTopMomentLateraldev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(TwrTopMomentLateralmin[19])+r'''& '''+str(TwrTopMomentLateralmean[19])+r''' & '''+str(TwrTopMomentLateralmax[19])+r''' & '''+str(TwrTopMomentLateraldev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(TwrTopMomentLateralmin[20])+r'''& '''+str(TwrTopMomentLateralmean[20])+r''' & '''+str(TwrTopMomentLateralmax[20])+r''' & '''+str(TwrTopMomentLateraldev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(TwrTopMomentLateralmin[21])+r'''& '''+str(TwrTopMomentLateralmean[21])+r''' & '''+str(TwrTopMomentLateralmax[21])+r''' & '''+str(TwrTopMomentLateraldev[21])+r''' \\ \hline
            \end{tabular}
            \egroup
            \end{table}

            \newpage  

            \subsubsection{Other quantities}

            Table \ref{tab:Poweroutput} shows the power output.

            \begin{table}[H]
            \caption{Power}
            \label{tab:Poweroutput}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (kW)} & \textbf{Mean (kW)} & \textbf{Max (kW)} & \textbf{Std dev.(kW)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(Powermin[0])+r'''& '''+str(Powermean[0])+r''' & '''+str(Powermax[0])+r''' & '''+str(Powerdev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(Powermin[1])+r'''& '''+str(Powermean[1])+r''' & '''+str(Powermax[1])+r''' & '''+str(Powerdev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(Powermin[2])+r'''& '''+str(Powermean[2])+r''' & '''+str(Powermax[2])+r''' & '''+str(Powerdev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(Powermin[3])+r'''& '''+str(Powermean[3])+r''' & '''+str(Powermax[3])+r''' & '''+str(Powerdev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(Powermin[4])+r'''& '''+str(Powermean[4])+r''' & '''+str(Powermax[4])+r''' & '''+str(Powerdev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(Powermin[5])+r'''& '''+str(Powermean[5])+r''' & '''+str(Powermax[5])+r''' & '''+str(Powerdev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(Powermin[6])+r'''& '''+str(Powermean[6])+r''' & '''+str(Powermax[6])+r''' & '''+str(Powerdev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(Powermin[7])+r'''& '''+str(Powermean[7])+r''' & '''+str(Powermax[7])+r''' & '''+str(Powerdev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(Powermin[8])+r'''& '''+str(Powermean[8])+r''' & '''+str(Powermax[8])+r''' & '''+str(Powerdev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(Powermin[9])+r'''& '''+str(Powermean[9])+r''' & '''+str(Powermax[9])+r''' & '''+str(Powerdev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(Powermin[10])+r'''& '''+str(Powermean[10])+r''' & '''+str(Powermax[10])+r''' & '''+str(Powerdev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(Powermin[11])+r'''& '''+str(Powermean[11])+r''' & '''+str(Powermax[11])+r''' & '''+str(Powerdev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(Powermin[12])+r'''& '''+str(Powermean[12])+r''' & '''+str(Powermax[12])+r''' & '''+str(Powerdev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(Powermin[13])+r'''& '''+str(Powermean[13])+r''' & '''+str(Powermax[13])+r''' & '''+str(Powerdev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(Powermin[14])+r'''& '''+str(Powermean[14])+r''' & '''+str(Powermax[14])+r''' & '''+str(Powerdev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(Powermin[15])+r'''& '''+str(Powermean[15])+r''' & '''+str(Powermax[15])+r''' & '''+str(Powerdev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(Powermin[16])+r'''& '''+str(Powermean[16])+r''' & '''+str(Powermax[16])+r''' & '''+str(Powerdev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(Powermin[17])+r'''& '''+str(Powermean[17])+r''' & '''+str(Powermax[17])+r''' & '''+str(Powerdev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(Powermin[18])+r'''& '''+str(Powermean[18])+r''' & '''+str(Powermax[18])+r''' & '''+str(Powerdev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(Powermin[19])+r'''& '''+str(Powermean[19])+r''' & '''+str(Powermax[19])+r''' & '''+str(Powerdev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(Powermin[20])+r'''& '''+str(Powermean[20])+r''' & '''+str(Powermax[20])+r''' & '''+str(Powerdev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(Powermin[21])+r'''& '''+str(Powermean[21])+r''' & '''+str(Powermax[21])+r''' & '''+str(Powerdev[21])+r''' \\ \hline
            \end{tabular}
            \egroup
            \end{table}

            \newpage  

            Table \ref{tab:GenSpeed} shows the generator speed.

            \begin{table}[H]
            \caption{Generator Speed}
            \label{tab:GenSpeed}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (RPM)} & \textbf{Mean (RPM} & \textbf{Max (RPM)} & \textbf{Std dev.(RPM)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(GenSpeedmin[0])+r'''& '''+str(GenSpeedmean[0])+r''' & '''+str(GenSpeedmax[0])+r''' & '''+str(GenSpeeddev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(GenSpeedmin[1])+r'''& '''+str(GenSpeedmean[1])+r''' & '''+str(GenSpeedmax[1])+r''' & '''+str(GenSpeeddev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(GenSpeedmin[2])+r'''& '''+str(GenSpeedmean[2])+r''' & '''+str(GenSpeedmax[2])+r''' & '''+str(GenSpeeddev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(GenSpeedmin[3])+r'''& '''+str(GenSpeedmean[3])+r''' & '''+str(GenSpeedmax[3])+r''' & '''+str(GenSpeeddev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(GenSpeedmin[4])+r'''& '''+str(GenSpeedmean[4])+r''' & '''+str(GenSpeedmax[4])+r''' & '''+str(GenSpeeddev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(GenSpeedmin[5])+r'''& '''+str(GenSpeedmean[5])+r''' & '''+str(GenSpeedmax[5])+r''' & '''+str(GenSpeeddev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(GenSpeedmin[6])+r'''& '''+str(GenSpeedmean[6])+r''' & '''+str(GenSpeedmax[6])+r''' & '''+str(GenSpeeddev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(GenSpeedmin[7])+r'''& '''+str(GenSpeedmean[7])+r''' & '''+str(GenSpeedmax[7])+r''' & '''+str(GenSpeeddev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(GenSpeedmin[8])+r'''& '''+str(GenSpeedmean[8])+r''' & '''+str(GenSpeedmax[8])+r''' & '''+str(GenSpeeddev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(GenSpeedmin[9])+r'''& '''+str(GenSpeedmean[9])+r''' & '''+str(GenSpeedmax[9])+r''' & '''+str(GenSpeeddev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(GenSpeedmin[10])+r'''& '''+str(GenSpeedmean[10])+r''' & '''+str(GenSpeedmax[10])+r''' & '''+str(GenSpeeddev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(GenSpeedmin[11])+r'''& '''+str(GenSpeedmean[11])+r''' & '''+str(GenSpeedmax[11])+r''' & '''+str(GenSpeeddev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(GenSpeedmin[12])+r'''& '''+str(GenSpeedmean[12])+r''' & '''+str(GenSpeedmax[12])+r''' & '''+str(GenSpeeddev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(GenSpeedmin[13])+r'''& '''+str(GenSpeedmean[13])+r''' & '''+str(GenSpeedmax[13])+r''' & '''+str(GenSpeeddev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(GenSpeedmin[14])+r'''& '''+str(GenSpeedmean[14])+r''' & '''+str(GenSpeedmax[14])+r''' & '''+str(GenSpeeddev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(GenSpeedmin[15])+r'''& '''+str(GenSpeedmean[15])+r''' & '''+str(GenSpeedmax[15])+r''' & '''+str(GenSpeeddev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(GenSpeedmin[16])+r'''& '''+str(GenSpeedmean[16])+r''' & '''+str(GenSpeedmax[16])+r''' & '''+str(GenSpeeddev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(GenSpeedmin[17])+r'''& '''+str(GenSpeedmean[17])+r''' & '''+str(GenSpeedmax[17])+r''' & '''+str(GenSpeeddev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(GenSpeedmin[18])+r'''& '''+str(GenSpeedmean[18])+r''' & '''+str(GenSpeedmax[18])+r''' & '''+str(GenSpeeddev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(GenSpeedmin[19])+r'''& '''+str(GenSpeedmean[19])+r''' & '''+str(GenSpeedmax[19])+r''' & '''+str(GenSpeeddev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(GenSpeedmin[20])+r'''& '''+str(GenSpeedmean[20])+r''' & '''+str(GenSpeedmax[20])+r''' & '''+str(GenSpeeddev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(GenSpeedmin[21])+r'''& '''+str(GenSpeedmean[21])+r''' & '''+str(GenSpeedmax[21])+r''' & '''+str(GenSpeeddev[21])+r''' \\ \hline
            \end{tabular}
            \egroup
            \end{table}

            \newpage  

            Table \ref{tab:RotorSpeed} shows the rotor speed.

            \begin{table}[H]
            \caption{Rotor Speed}
            \label{tab:RotorSpeed}
            \centering
            \bgroup
            \def\arraystretch{1.5}
            \begin{tabular}{|c|c|c|c|c|c|}
            \hline
            \textbf{Wind speed (m/s)} & \textbf{\# files} & \textbf{Min (RPM)} & \textbf{Mean (RPM} & \textbf{Max (RPM)} & \textbf{Std dev.(RPM)} \\ \hline
            \textbf{3-4} & '''+str(number_of_files[0])+r''' &'''+str(RotSpeedmin[0])+r'''& '''+str(RotSpeedmean[0])+r''' & '''+str(RotSpeedmax[0])+r''' & '''+str(RotSpeeddev[0])+r''' \\ \hline
            \textbf{4-5} & '''+str(number_of_files[1])+r''' &'''+str(RotSpeedmin[1])+r'''& '''+str(RotSpeedmean[1])+r''' & '''+str(RotSpeedmax[1])+r''' & '''+str(RotSpeeddev[1])+r''' \\ \hline
            \textbf{5-6} & '''+str(number_of_files[2])+r''' &'''+str(RotSpeedmin[2])+r'''& '''+str(RotSpeedmean[2])+r''' & '''+str(RotSpeedmax[2])+r''' & '''+str(RotSpeeddev[2])+r''' \\ \hline
            \textbf{6-7} & '''+str(number_of_files[3])+r''' &'''+str(RotSpeedmin[3])+r'''& '''+str(RotSpeedmean[3])+r''' & '''+str(RotSpeedmax[3])+r''' & '''+str(RotSpeeddev[3])+r''' \\ \hline
            \textbf{7-8} & '''+str(number_of_files[4])+r''' &'''+str(RotSpeedmin[4])+r'''& '''+str(RotSpeedmean[4])+r''' & '''+str(RotSpeedmax[4])+r''' & '''+str(RotSpeeddev[4])+r''' \\ \hline
            \textbf{8-9} & '''+str(number_of_files[5])+r''' &'''+str(RotSpeedmin[5])+r'''& '''+str(RotSpeedmean[5])+r''' & '''+str(RotSpeedmax[5])+r''' & '''+str(RotSpeeddev[5])+r''' \\ \hline
            \textbf{9-10} & '''+str(number_of_files[6])+r''' &'''+str(RotSpeedmin[6])+r'''& '''+str(RotSpeedmean[6])+r''' & '''+str(RotSpeedmax[6])+r''' & '''+str(RotSpeeddev[6])+r''' \\ \hline
            \textbf{10-11} & '''+str(number_of_files[7])+r''' &'''+str(RotSpeedmin[7])+r'''& '''+str(RotSpeedmean[7])+r''' & '''+str(RotSpeedmax[7])+r''' & '''+str(RotSpeeddev[7])+r''' \\ \hline
            \textbf{11-12} & '''+str(number_of_files[8])+r''' &'''+str(RotSpeedmin[8])+r'''& '''+str(RotSpeedmean[8])+r''' & '''+str(RotSpeedmax[8])+r''' & '''+str(RotSpeeddev[8])+r''' \\ \hline
            \textbf{12-13} & '''+str(number_of_files[9])+r''' &'''+str(RotSpeedmin[9])+r'''& '''+str(RotSpeedmean[9])+r''' & '''+str(RotSpeedmax[9])+r''' & '''+str(RotSpeeddev[9])+r''' \\ \hline
            \textbf{13-14} & '''+str(number_of_files[10])+r''' &'''+str(RotSpeedmin[10])+r'''& '''+str(RotSpeedmean[10])+r''' & '''+str(RotSpeedmax[10])+r''' & '''+str(RotSpeeddev[10])+r''' \\ \hline
            \textbf{14-15} & '''+str(number_of_files[11])+r''' &'''+str(RotSpeedmin[11])+r'''& '''+str(RotSpeedmean[11])+r''' & '''+str(RotSpeedmax[11])+r''' & '''+str(RotSpeeddev[11])+r''' \\ \hline
            \textbf{15-16} & '''+str(number_of_files[12])+r''' &'''+str(RotSpeedmin[12])+r'''& '''+str(RotSpeedmean[12])+r''' & '''+str(RotSpeedmax[12])+r''' & '''+str(RotSpeeddev[12])+r''' \\ \hline
            \textbf{16-17} & '''+str(number_of_files[13])+r''' &'''+str(RotSpeedmin[13])+r'''& '''+str(RotSpeedmean[13])+r''' & '''+str(RotSpeedmax[13])+r''' & '''+str(RotSpeeddev[13])+r''' \\ \hline
            \textbf{17-18} & '''+str(number_of_files[14])+r''' &'''+str(RotSpeedmin[14])+r'''& '''+str(RotSpeedmean[14])+r''' & '''+str(RotSpeedmax[14])+r''' & '''+str(RotSpeeddev[14])+r''' \\ \hline
            \textbf{18-19} & '''+str(number_of_files[15])+r''' &'''+str(RotSpeedmin[15])+r'''& '''+str(RotSpeedmean[15])+r''' & '''+str(RotSpeedmax[15])+r''' & '''+str(RotSpeeddev[15])+r''' \\ \hline
            \textbf{19-20} & '''+str(number_of_files[16])+r''' &'''+str(RotSpeedmin[16])+r'''& '''+str(RotSpeedmean[16])+r''' & '''+str(RotSpeedmax[16])+r''' & '''+str(RotSpeeddev[16])+r''' \\ \hline
            \textbf{20-21} & '''+str(number_of_files[17])+r''' &'''+str(RotSpeedmin[17])+r'''& '''+str(RotSpeedmean[17])+r''' & '''+str(RotSpeedmax[17])+r''' & '''+str(RotSpeeddev[17])+r''' \\ \hline
            \textbf{21-22} & '''+str(number_of_files[18])+r''' &'''+str(RotSpeedmin[18])+r'''& '''+str(RotSpeedmean[18])+r''' & '''+str(RotSpeedmax[18])+r''' & '''+str(RotSpeeddev[18])+r''' \\ \hline
            \textbf{22-23} & '''+str(number_of_files[19])+r''' &'''+str(RotSpeedmin[19])+r'''& '''+str(RotSpeedmean[19])+r''' & '''+str(RotSpeedmax[19])+r''' & '''+str(RotSpeeddev[19])+r''' \\ \hline
            \textbf{23-24} & '''+str(number_of_files[20])+r''' &'''+str(RotSpeedmin[20])+r'''& '''+str(RotSpeedmean[20])+r''' & '''+str(RotSpeedmax[20])+r''' & '''+str(RotSpeeddev[20])+r''' \\ \hline
            \textbf{24-25} & '''+str(number_of_files[21])+r''' &'''+str(RotSpeedmin[21])+r'''& '''+str(RotSpeedmean[21])+r''' & '''+str(RotSpeedmax[21])+r''' & '''+str(RotSpeeddev[21])+r''' \\ \hline
            \end{tabular}
            \egroup
            \end{table}

            \newpage  
            
            \subsection{Results plots}

            This section shows the plots of data from the tables of previous section. Since there are 18 plots for each wind speed/turbulence intensity case, only two cases will be showed, one for a maximum power
            point tracking (MMPT) region and one for speed control region.

            \newpage  
            
            \subsubsection{Blades roots flapwise bending moments}

            Blade root flapwise bending moments time-series and FFT of the blades in MPPT region are showed in Figures \ref{fig:BladeRootFlapMPPT}-\ref{fig:BladeRootFlapMPPTFFT}.

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+mppt_folder+r'''BladeRootFlapMoments"}.png}
	    \caption[Blade root flapwise bending moment time-series at MPPT region]{Blade root flapwise bending moment time-series at MPPT region}
	    \label{fig:BladeRootFlapMPPT}
            \end{figure}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+mppt_folder+r'''BladeRootFlapMomentsFFT"}.png}
	    \caption[Blade root flapwise bending moment FFT  at MPPT region]{Blade root flapwise bending moment FFT at MPPT region}
	    \label{fig:BladeRootFlapMPPTFFT}
            \end{figure}

            \newpage  
        
            Blade root flapwise bending moments time-series and FFT of the blades in speed control region are showed in Figures \ref{fig:BladeRootFlapSC}-\ref{fig:BladeRootFlapSCFFT}.

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+speed_control_folder+r'''BladeRootFlapMoments"}.png}
	    \caption[Blade root flapwise bending moment time-series at speed control]{Blade root flapwise bending moment time-series at speed control}
	    \label{fig:BladeRootFlapSC}
            \end{figure}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+speed_control_folder+r'''BladeRootFlapMomentsFFT"}.png}
	    \caption[Blade root flapwise bending moment FFT at speed control region]{Blade root flapwise bending moment FFT at speed control region}
	    \label{fig:BladeRootFlapSCFFT}
            \end{figure}

            \newpage  

            \subsubsection{Blades roots edgewise bending moments}

            Blade root edgewise bending moments time-series and FFT of the blades in MPPT region are showed in Figures \ref{fig:BladeRootEdgeMPPT}-\ref{fig:BladeRootEdgeMPPTFFT}.

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+mppt_folder+r'''BladeRootEdgeMoments"}.png}
	    \caption[Blade root edgewise bending moment time-series at MPPT region]{Blade root edgewise bending moment time-series at MPPT region}
	    \label{fig:BladeRootEdgeMPPT}
            \end{figure}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+mppt_folder+r'''BladeRootEdgeMomentsFFT"}.png}
	    \caption[Blade root edgewise bending moment FFT at MPPT region]{Blade root edgewise bending moment FFT at MPPT region}
	    \label{fig:BladeRootEdgeMPPTFFT}
            \end{figure}

            \newpage  
        
            Blade root edgewise bending moments time-series and FFT of the blades in speed control region are showed in Figures \ref{fig:BladeRootEdgeSC}-\ref{fig:BladeRootEdgeSCFFT}.

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+speed_control_folder+r'''BladeRootEdgeMoments"}.png}
	    \caption[Blade root edgewise bending moment time-series at speed control region]{Blade root edgewise bending moment time-series at speed control region}
	    \label{fig:BladeRootEdgeSC}
            \end{figure}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+speed_control_folder+r'''BladeRootEdgeMomentsFFT"}.png}
	    \caption[Blade root edgewise bending moment FFT  at speed control region]{Blade root edgewise bending moment FFT at speed control region}
	    \label{fig:BladeRootEdgeSCFFT}
            \end{figure}

            \newpage  

            \subsubsection{Rotor moments}

            Rotor moments time-series and FFT in MPPT region are showed in Figures \ref{fig:RotorQuantitiesMPPT}-\ref{fig:RotorQuantitiesMPPTFFT}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+mppt_folder+r'''RotorQuantities"}.png}
	    \caption[Rotor moments time-series at MPPT region]{Rotor moments time-series at MPPT region}
	    \label{fig:RotorQuantitiesMPPT}
            \end{figure}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+mppt_folder+r'''RotorQuantitiesFFT"}.png}
	    \caption[Rotor moments FFT at MPPT region]{Rotor moments FFT at MPPT region}
	    \label{fig:RotorQuantitiesMPPTFFT}
            \end{figure}

            \newpage  

            Rotor moments time-series and FFT in SC region are showed in Figures \ref{fig:RotorQuantitiesSC}-\ref{fig:RotorQuantitiesSCFFT}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+speed_control_folder+r'''RotorQuantities"}.png}
	    \caption[Rotor moments time-series at SC region]{Rotor moments time-series at SC region}
	    \label{fig:RotorQuantitiesSC}
            \end{figure}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+speed_control_folder+r'''RotorQuantitiesFFT"}.png}
	    \caption[Rotor moments FFT at SC region]{Rotor moments FFT at SC region}
	    \label{fig:RotorQuantitiesSCFFT}
            \end{figure}

            \newpage  

            \subsubsection{Tower base moments}

            Tower moments time-series and FFT in MPPT region are showed in Figures \ref{fig:TowerMomentsMPPT}-\ref{fig:TowerMomentsMPPTFFT}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+mppt_folder+r'''TowerMoments"}.png}
	    \caption[Tower moments time-series at MPPT region]{Tower moments time-series at MPPT region}
	    \label{fig:TowerMomentsMPPT}
            \end{figure}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+mppt_folder+r'''TowerMomentsFFT"}.png}
	    \caption[Tower moments FFT at MPPT region]{Tower moments FFT at MPPT region}
	    \label{fig:TowerMomentsMPPTFFT}
            \end{figure}

            \newpage  

            Tower moments time-series and FFT in SC region are showed in Figures \ref{fig:TowerMomentsSC}-\ref{fig:TowerMomentsSCFFT}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+speed_control_folder+r'''TowerMoments"}.png}
	    \caption[Tower moments time-series at SC region]{Tower moments time-series at SC region}
	    \label{fig:TowerMomentsSC}
            \end{figure}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+speed_control_folder+r'''TowerMomentsFFT"}.png}
	    \caption[Tower moments FFT at SC region]{Tower moments FFT at MSCPPT region}
	    \label{fig:TowerMomentsSCFFT}
            \end{figure}

            \newpage  

            \subsubsection{Pitch actuation loads}

            Pitch actuation loads time-series and FFT in MPPT region are showed in Figures \ref{fig:pitchactMPPT}-\ref{fig:pitchactMPPTFFT}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+mppt_folder+r'''PitchActuationLoads"}.png}
	    \caption[Pitch actuation loads time-series in MPPT region]{Pitch actuation loads time-series in MPPT region}
	    \label{fig:pitchactMPPT}
            \end{figure}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+mppt_folder+r'''PitchActuationLoadsFFT"}.png}
	    \caption[Pitch actuation loads FFT in MPPT region]{Pitch actuation loads FFT in MPPT region}
	    \label{fig:pitchactMPPTFFT}
            \end{figure}

            \newpage  

            Pitch actuation loads time-series and FFT in SC region are showed in Figures \ref{fig:pitchactSC}-\ref{fig:pitchactSCFFT}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+speed_control_folder+r'''PitchActuationLoads"}.png}
	    \caption[Pitch actuation loads time-series in SC region]{Pitch actuation loads time-series in SC region}
	    \label{fig:pitchactSC}
            \end{figure}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+speed_control_folder+r'''PitchActuationLoadsFFT"}.png}
	    \caption[Pitch actuation loads FFT in SC region]{Pitch actuation loads FFT in SC region}
	    \label{fig:pitchactSCFFT}
            \end{figure}

            \newpage  

            \subsubsection{Tower top accelerations}

            Tower top accelerations time-series and FFT in MPPT region are showed in Figures \ref{fig:TowerTopAccMPPT}-\ref{fig:TowerTopAccMPPTFFT}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+mppt_folder+r'''TowerTopAccelerations"}.png}
	    \caption[Tower top accelerations time-series in MPPT region]{Tower top accelerations time-series in MPPT region}
	    \label{fig:TowerTopAccMPPT}
            \end{figure}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+mppt_folder+r'''TowerTopAccelerationsFFT"}.png}
	    \caption[Tower top accelerations FFT in MPPT region]{Tower top accelerations FFT in MPPT region}
	    \label{fig:TowerTopAccMPPTFFT}
            \end{figure}

            \newpage  

            Tower top accelerations time-series and FFT in SC region are showed in Figures \ref{fig:TowerTopAccSC}-\ref{fig:TowerTopAccSCFFT}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+speed_control_folder+r'''TowerTopAccelerations"}.png}
	    \caption[Tower top accelerations time-series in SC region]{Tower top accelerations time-series in SSC region}
	    \label{fig:TowerTopAccSC}
            \end{figure}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+speed_control_folder+r'''TowerTopAccelerationsFFT"}.png}
	    \caption[Tower top accelerations FFT in SC region]{Tower top accelerations FFT in SC region}
	    \label{fig:TowerTopAccSCFFT}
            \end{figure}

            \newpage  

            \subsubsection{Tower top moments}

            Tower top moments time-series and FFT in MPPT region are showed in Figures \ref{fig:TowertTopMomentsMPPT}-\ref{fig:TowertTopMomentsMPPTFFT}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+mppt_folder+r'''TowerTopMoments"}.png}
	    \caption[Tower top moments time-series in MPPT region]{Tower top moments time-series in MPPT region}
	    \label{fig:TowertTopMomentsMPPT}
            \end{figure}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+mppt_folder+r'''TowerTopMomentsFFT"}.png}
	    \caption[Tower top moments FFT in MPPT region]{Tower top moments FFT in MPPT region}
	    \label{fig:TowertTopMomentsMPPTFFT}
            \end{figure}

            \newpage  

            Tower top moments time-series and FFT in SC region are showed in Figures \ref{fig:TowertTopMomentsSC}-\ref{fig:TowertTopMomentsSCFFT}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+speed_control_folder+r'''TowerTopMoments"}.png}
	    \caption[Tower top moments time-series in SC region]{Tower top moments time-series in SSC region}
	    \label{fig:TowertTopMomentsSC}
            \end{figure}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+speed_control_folder+r'''TowerTopMomentsFFT"}.png}
	    \caption[Tower top moments FFT in SC region]{Tower top moments FFT in SC region}
	    \label{fig:TowertTopMomentsSCFFT}
            \end{figure}

            \newpage  

            \subsubsection{Other quantities}

            Other turbine quantities time-series and FFT in MPPT region are showed in Figures \ref{fig:OtherQuantitiesMPPT}-\ref{fig:OtherQuantitiesMPPTFFT}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+mppt_folder+r'''Quantities"}.png}
	    \caption[Other quantities time-series in MPPT region]{Other quantities time-series in MPPT region}
	    \label{fig:OtherQuantitiesMPPT}
            \end{figure}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+mppt_folder+r'''QuantitiesFFT"}.png}
	    \caption[Other quantities FFT in MPPT region]{Other quantities FFT in MPPT region}
	    \label{fig:OtherQuantitiesMPPTFFT}
            \end{figure}

            \newpage  

            Other turbine quantities time-series and FFT in SC region are showed in Figures \ref{fig:OtherQuantitiesSC}-\ref{fig:OtherQuantitiesSCFFT}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+speed_control_folder+r'''Quantities"}.png}
	    \caption[Other quantities time-series in SC region]{Other quantities time-series in SC region}
	    \label{fig:OtherQuantitiesSC}
            \end{figure}

            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+speed_control_folder+r'''QuantitiesFFT"}.png}
	    \caption[Other quantities FFT in SC region]{Other quantities FFT in SC region}
	    \label{fig:OtherQuantitiesSCFFT}
            \end{figure}

            \newpage  

        
            '''
        content = header + main + footer
        
#######################################################################################################################################################################################################################
        
        tex_file= turbinefast+' Simulink - Customized Report.tex'

        with open(tex_file,'w') as f:
                f.write(content)

        commandLine1 = subprocess.Popen(['pdflatex', tex_file])
        commandLine1.communicate()
        commandLine2=subprocess.Popen(['BibTex',tex_file])
        commandLine2.communicate()
        commandLine3 = subprocess.Popen(['pdflatex', tex_file])
        commandLine3.communicate()
        commandLine4 = subprocess.Popen(['pdflatex', tex_file])
        commandLine4.communicate()

        unlink_file = tex_file[0:len(tex_file)-4]
        pdf_file = unlink_file+'.pdf'

        os.unlink(unlink_file+'.aux')
        os.unlink(unlink_file+'.log')
        os.unlink(unlink_file+'.tex')
        os.unlink(unlink_file+'.toc')
        
        shutil.move(path_fast+pdf_file,sim_path+pdf_file)
