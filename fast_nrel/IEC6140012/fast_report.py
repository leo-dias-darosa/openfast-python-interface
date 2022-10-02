import sys
import os
import subprocess
import shutil
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

        wind_speed =np.arange(3,25,0.5)
        path_modules=path_modules+'/'
        path_fast = path_fast+'/'
        
        fast_input = open(path_fast+turbinefast).read().splitlines()
        turbinefast = turbinefast[0:len(turbinefast)-4]

        sim_path = path_fast+turbinefast+' Power Curve - IEC61400.12 - Fast/'
        
        Simulation = 'Power Curve - IEC61400.12 - Fast'

        simulated_file = sim_path+turbinefast+'-'+str(v)+'ms/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)
        
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

        aero_file = open(sim_path+turbinefast+'-'+str(v)+'ms/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/Aero.dat').read().splitlines()

        air_density_line=aero_file[12].split()
        air_density=air_density_line[0]

####################################################################################################### GET DATA #####################################################################################################
        
        ## Lists
        
        # Min

        Powermin=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        
        Powermean=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        Powermax=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        Powerdev=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        mppt_speeds=[]
        speed_control_speeds=[]
                
        for v in wind_speed:
                Index = int(v)-3
                for turb in range(5,26):
                        if os.path.exists(sim_path+turbinefast+'-'+str(v)+'ms/'+turbinefast+'-'+str(v)+'ms-'+str(turb)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/'+turbinefast+'-'+str(v)+'ms-'+str(turb)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'.out')==False:
                                pass
                        else:
                                read_path = sim_path+turbinefast+'-'+str(v)+'ms/'+turbinefast+'-'+str(v)+'ms-'+str(turb)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/'

                                out_file = read_path+turbinefast+'-'+str(v)+'ms-'+str(turb)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'.out'

                                out_file_noHeaderStr = out_file[0:len(out_file)-4]+"noHeader.out"
                                out_file_csv = out_file[0:len(out_file)-4]+"noHeader.csv"

                                dataIndex =  pd.read_csv(out_file_csv)
                                data_normal_col = pd.read_csv(out_file_csv,header=None)
                        
                        ## Other quantities
                                
                                RotorPowerIndex = dataIndex.columns.get_loc("GenPwr")
                                RotorPowerNormal = data_normal_col.iloc[2:,RotorPowerIndex]
                                RotorPowerNormal = [float(x) for x in RotorPowerNormal]

                                Powermin[Index].append(round(np.min(RotorPowerNormal),3))
                                Powermean[Index].append(round(np.mean(RotorPowerNormal),3))
                                Powermax[Index].append(round(np.max(RotorPowerNormal),3))
                                Powerdev[Index].append(round(np.std(RotorPowerNormal),3))


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

        ## For number of files
        
        number_of_files = []
        for i in range(len(Powermin)):
                number_of_files.append(len(Powermin[i]))
        

        for i in range(len(Powermin)):
                if not Powermin[i]:
                        Powermin[i]='-'
                else:
                        Powermin[i]=round(np.min(Powermin[i]),3)


        for i in range(len(Powermean)):
                if not Powermean[i]:
                        Powermean[i]='-'
                else:
                        Powermean[i]=round(np.mean(Powermean[i]),3)

        for i in range(len(Powermax)):
                if not Powermax[i]:
                        Powermax[i]='-'
                else:
                        Powermax[i]=round(np.max(Powermax[i]),3)


        for i in range(len(Powerdev)):
                if not Powerdev[i]:
                        Powerdev[i]='-'
                else:
                        Powerdev[i]=round(np.std(Powerdev[i]),3)


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
            for the simulation such as wind, aerodynamics and elastodynamics characteristics and FAST modules used. Third section describes the output results of the simulation based on IEC 61400.12 Power Curve.
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
            Table \ref{tab:ElastoSumDOF}.

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

            \section{Simulation results}

            Simulations results were obtained from FAST output files. Those files come in a .txt format, and FAST INTERFACE handle them to get necessary data for plotting in this section. For any purpose,
            .csv files are generated from each of the simulation output .txt, so the user can work already with this format if wanted.

            As mentioned before, the output results are based in the IEC 61400-12 Power curve. The wind speeds considered were from 3-25 m/s, in 0.5 m/s step, with'''+str(t)+r'''% turbulence intensity.
            Power curve and power coefficient plots are showed in the next sections, as well as a table with statistical data.

            \subsection{Statistical data}

            This section shows statistcs binned data of the IEC 61400-12 power output. The standard requests from results the minimum, mean, maximum and standard deviation from each bin. The binned data is
            showed in Table \ref{tab:Poweroutput}.

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
            
            \subsection{Results plots}

            This section shows the plots of power data from the table of previous section. The mean power is considered for the power coefficient and power curve plots and the scatter plot contains the
            others statisthical data, as in Figure \ref{fig:CurveCP}
            
            \begin{figure}[H]
	    \centering
	    \includegraphics[width=0.90\linewidth]{{"'''+sim_path+r'''/'''+turbinefast+r''' - Power curve, PC and Scatter plot"}.png}
	    \caption[Power curve, power coefficient and scatter plot output]{Power curve, power coefficient and scatter plot output}
	    \label{fig:CurveCP}
            \end{figure}

            \newpage  
        
            '''
        content = header + main + footer
        
#######################################################################################################################################################################################################################
        
        tex_file= turbinefast+' - Fast - Power Curve - IEC61400.12 Report.tex'

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
