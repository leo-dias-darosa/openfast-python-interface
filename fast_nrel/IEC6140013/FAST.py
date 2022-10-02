import os
import subprocess
import shutil
import fast_nrel as fst
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft

def simulation(parameters,wind_style=1):

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

        ## Parameters for wind generation and FAST simulation

        parameters_turbsim = [path_turbsim,turbsim,path_fast,path_modules,turbinefast,v,h,t,s,e,n,frequency,simulink]
        
        path_modules=path_modules+'/'
        path_fast = path_fast+'/'
        
        if wind_style==1:
            fst.wind.steady(parameters_turbsim)
        elif wind_style==2:
            fst.wind.uniform_wind_file(parameters_turbsim)
        elif wind_style==3:
            fst.wind.binary_turbsim_full_field_files(parameters_turbsim)              
        elif wind_style==4:
            fst.wind.binary_bladed_style_full_field(parameters_turbsim)

        fast_standard = open(path_fast+turbinefast).read().splitlines()
        turbinefast = turbinefast[0:len(turbinefast)-4]
        if os.path.isdir(path_fast+turbinefast+' Fundamental Load quantities - IEC61400.13 - Fast') == False:
            os.mkdir(path_fast+turbinefast+' Fundamental Load quantities - IEC61400.13 - Fast')
        if os.path.isdir(path_fast+turbinefast+' Fundamental Load quantities - IEC61400.13 - Fast/'+turbinefast+' - '+str(s)+'s of duration bins')==False:
            os.mkdir(path_fast+turbinefast+' Fundamental Load quantities - IEC61400.13 - Fast/'+turbinefast+' - '+str(s)+'s of duration bins')
        if os.path.isdir(path_fast+turbinefast+' Fundamental Load quantities - IEC61400.13 - Fast/'+turbinefast+' - '+str(s)+'s of duration bins/'+turbinefast+'-'+str(v)+'ms')==False:
            os.mkdir(path_fast+turbinefast+' Fundamental Load quantities - IEC61400.13 - Fast/'+turbinefast+' - '+str(s)+'s of duration bins/'+turbinefast+'-'+str(v)+'ms')

        new_path = path_fast+turbinefast+' Fundamental Load quantities - IEC61400.13 - Fast/'+turbinefast+' - '+str(s)+'s of duration bins/'+turbinefast+'-'+str(v)+'ms/'
        str_fast=new_path+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'.fst'
        txtfast=open(str_fast,'w')

        if os.path.isdir(new_path+'/Aerodata')==True:
                shutil.rmtree(new_path+'/Aerodata')
        if os.path.isdir(new_path+'/Airfoils')==True:
                shutil.rmtree(new_path+'/Airfoils')

        shutil.copytree(path_modules+'Aerodata',new_path+'/Aerodata')
        shutil.copytree(path_modules+'Airfoils',new_path+'/Airfoils')

        for line in fast_standard:
                txtfast.write(line+'\n')
        txtfast.close()

        insert_modules = open(str_fast).read().splitlines()           

        ## Get modules

        # Elasto
        Elasto_line = insert_modules[21].split()
        Beam1_line = insert_modules[22].split()
        Beam2_line = insert_modules[23].split()
        Beam3_line = insert_modules[24].split()
        Inflow_line = insert_modules[25].split()
        Aero_line = insert_modules[26].split()
        Servo_line = insert_modules[27].split()
        Hydro_line = insert_modules[28].split()
        Sub_line = insert_modules[29].split()
        Moor_line = insert_modules[30].split()
        Ice_line = insert_modules[31].split()
        
        Elasto = Elasto_line[0]
        Elasto = Elasto[1:len(Elasto)-1]
        Elasto_dyn=''
        for i in Elasto:
                if i == '/':
                        Elasto_dyn = ''
                else:
                        Elasto_dyn = Elasto_dyn+i

        Beam1 = Beam1_line[0]
        Beam1 = Beam1[1:len(Beam1)-1]
        Beam_dyn1=''
        for i in Beam1:
                if i == '/':
                    Beam_dyn1 = ''
                else:
                    Beam_dyn1 = Beam_dyn1+i

        Beam2 = Beam2_line[0]
        Beam2 = Beam2[1:len(Beam2)-1]
        Beam_dyn2=''
        for i in Beam2:
                if i == '/':
                    Beam_dyn2 = ''
                else:
                    Beam_dyn2 = Beam_dyn2+i
                    
        Beam3 = Beam3_line[0]
        Beam3 = Beam3[1:len(Beam3)-1]
        Beam_dyn3=''
        for i in Beam3:
                if i == '/':
                    Beam_dyn3 = ''
                else:
                    Beam_dyn3 = Beam_dyn3+i
                        
        Inflow = Inflow_line[0]
        Inflow = Inflow[1:len(Inflow)-1]
        Inflow_wind=''
        for i in Inflow:
                if i == '/':
                    Inflow_wind = ''
                else:
                    Inflow_wind = Inflow_wind+i

        Aero = Aero_line[0]
        Aero = Aero[1:len(Aero)-1]
        Aero_dyn=''
        for i in Aero:
                if i == '/':
                    Aero_dyn = ''
                else:
                    Aero_dyn = Aero_dyn+i
                    
        Servo = Servo_line[0]
        Servo = Servo[1:len(Servo)-1]           
        Servo_dyn=''
        for i in Servo:
                if i == '/':
                    Servo_dyn = ''
                else:
                    Servo_dyn = Servo_dyn+i
                    
        Hydro = Hydro_line[0]
        Hydro = Hydro[1:len(Hydro)-1]
        Hydro_dyn=''
        for i in Hydro:
                if i == '/':
                    Hydro_dyn = ''
                else:
                    Hydro_dyn = Hydro_dyn+i

        Sub = Sub_line[0]
        Sub = Sub[1:len(Sub)-1]             
        Sub_dyn=''
        for i in Sub:
                if i == '/':
                    Sub_dyn = ''
                else:
                    Sub_dyn = Sub_dyn+i
                        
        Moor = Moor_line[0]
        Moor = Moor[1:len(Moor)-1]
        Moor_dyn=''
        for i in Moor:
                if i == '/':
                    Moor_dyn = ''
                else:
                    Moor_dyn = Moor_dyn+i
                    
        Ice = Ice_line[0]
        Ice = Ice[1:len(Ice)-1]
        Ice_dyn=''
        for i in Ice:
                if i == '/':
                    Ice_dyn = ''
                else:
                    Ice_dyn = Ice_dyn+i
            
        insert_elastocomponents = open(path_modules+Elasto_dyn).read().splitlines()

        Blade1_line = insert_elastocomponents[87].split()
        Blade2_line = insert_elastocomponents[88].split()
        Blade3_line = insert_elastocomponents[89].split()
        Tower_line = insert_elastocomponents[109].split()

        Blade1 = Blade1_line[0]
        Blade2 = Blade2_line[0]
        Blade3 = Blade3_line[0]
        Tower = Tower_line[0]

        Blade1=Blade1[1:len(Blade1)-1]
        Blade2=Blade2[1:len(Blade2)-1]
        Blade3=Blade3[1:len(Blade3)-1]
        Tower=Tower[1:len(Tower)-1]
                        
        insert_aerocomponents = open(path_modules+Aero_dyn).read().splitlines()

        if len(insert_aerocomponents)>40:
                airfoil_number_line=insert_aerocomponents[33].split()
                airfoil_number = int(airfoil_number_line[0])

                Aero_blade1_line = insert_aerocomponents[36+airfoil_number].split()
                Aero_blade2_line = insert_aerocomponents[37+airfoil_number].split()
                Aero_blade3_line = insert_aerocomponents[38+airfoil_number].split()

                Aero_blade1 = Aero_blade1_line[0]
                Aero_blade2 = Aero_blade2_line[0]
                Aero_blade3 = Aero_blade3_line[0]

                Aero_blade1 = Aero_blade1[1:len(Aero_blade1)-1]
                Aero_blade2 = Aero_blade2[1:len(Aero_blade2)-1]
                Aero_blade3 = Aero_blade3[1:len(Aero_blade3)-1]

        ## Create new_modules
                    
        if os.path.exists(path_modules+Elasto_dyn) == True:
                Elasto_standard=open(path_modules+Elasto_dyn).read().splitlines()
                if os.path.exists(new_path+'Elasto.dat')==False:
                        new_elasto = open(new_path+'Elasto.dat','w')
                        for line in Elasto_standard:
                            new_elasto.write(line+'\n')
                        new_elasto.close()
                
        if os.path.exists(path_modules+Beam_dyn1) == True:
                Beam1_standard=open(path_modules+Beam_dyn1).read().splitlines()
                if os.path.exists(new_path+'Beam1.dat')==False:
                        new_beam = open(new_path+'Beam1.dat','w')
                        for line in Beam1_standard:
                            new_beam.write(line+'\n')
                        new_beam.close()

        if os.path.exists(path_modules+Beam_dyn2) == True:
                Beam2_standard=open(path_modules+Beam_dyn2).read().splitlines()
                if os.path.exists(new_path+'Beam2.dat')==False:
                        new_beam = open(new_path+'Beam2.dat','w')
                        for line in Beam2_standard:
                            new_beam.write(line+'\n')
                        new_beam.close()

        if os.path.exists(path_modules+Beam_dyn3) == True:
                Beam3_standard=open(path_modules+Beam_dyn3).read().splitlines()
                if os.path.exists(new_path+'Beam3.dat')==False:
                        new_beam = open(new_path+'Beam3.dat','w')
                        for line in Beam3_standard:
                            new_beam.write(line+'\n')
                        new_beam.close()
                
        if os.path.exists(path_modules+Servo_dyn) == True:
                Servo_standard=open(path_modules+Servo_dyn).read().splitlines()
                if os.path.exists(new_path+'Servo.dat')==False:
                        new_servo = open(new_path+'Servo.dat','w')
                        for line in Servo_standard:
                            new_servo.write(line+'\n')
                        new_servo.close()

        if os.path.exists(path_modules+Aero_dyn) == True:
                Aero_standard=open(path_modules+Aero_dyn).read().splitlines()
                if os.path.exists(new_path+'Aero.dat')==False:
                        new_aero = open(new_path+'Aero.dat','w')
                        for line in Aero_standard:
                            new_aero.write(line+'\n')
                        new_aero.close()
                
        if os.path.exists(path_modules+Inflow_wind)== True:
                Inflow_standard=open(path_modules+Inflow_wind).read().splitlines()
                if os.path.exists(new_path+'Inflow.dat')==False:
                        new_inflow = open(new_path+'Inflow.dat','w')
                        for line in Inflow_standard:
                            new_inflow.write(line+'\n')
                        new_inflow.close()
                   
        if os.path.exists(path_modules+Sub_dyn) == True:
                Sub_standard=open(path_modules+Sub_dyn).read().splitlines()
                if os.path.exists(new_path+'Sub.dat')==False:
                        new_sub = open(new_path+'Sub.dat','w')
                        for line in Sub_standard:
                            new_sub.write(line+'\n')
                        new_sub.close()
                
        if os.path.exists(path_modules+Hydro_dyn) == True:
                Hydro_standard=open(path_modules+Hydro_dyn).read().splitlines()
                if os.path.exists(new_path+'Hydro.dat')==False:
                        new_hydro = open(new_path+'Hydro.dat','w')
                        for line in Hydro_standard:
                            new_hydro.write(line+'\n')
                        new_hydro.close()
                 
        if os.path.exists(path_modules+Moor_dyn) == True:
                Moor_standard=open(path_modules+Moor_dyn).read().splitlines()
                if os.path.exists(new_path+'Moor.dat')==False:
                        new_moor = open(new_path+'Moor.dat','w')
                        for line in Moor_standard:
                            new_moor.write(line+'\n')
                        new_moor.close()
                
        if os.path.exists(path_modules+Ice_dyn) == True:
                Ice_standard=open(path_modules+Ice_dyn).read().splitlines()
                if os.path.exists(new_path+'Ice.dat')==False:
                        new_ice = open(new_path+'Ice.dat','w')
                        for line in Ice_standard:
                            new_ice.write(line+'\n')
                        new_ice.close()
                    

        ## Inflow Wind ##
        
        inflow_line=fast_standard[25].split()
        Inflow = inflow_line[0]
        Inflow=Inflow[1:len(Inflow)-1]
        
        ## Modify inflow wind
    
        wind_inflow= open(path_fast+Inflow).read().splitlines()

        ## Get wind
    
        wind_2_line=wind_inflow[15].split()
        wind_2= wind_2_line[0]
        wind_2= wind_2[1:len(wind_2)-1]

        wind_3_line=wind_inflow[19].split()
        wind_3= wind_3_line[0]
        wind_3= wind_3[1:len(wind_3)-1]

        wind_4_line=wind_inflow[21].split()
        wind_4= wind_4_line[0]
        wind_4= wind_4[1:len(wind_4)-1]
                
        ## Get Wind name only and modify path

        wind_name_2= ''
        for i in wind_2:
                if i =='/':
                    wind_name_2=''
                else:
                    wind_name_2=wind_name_2+i

        wind_name_3= ''
        for i in wind_3:
                if i =='/':
                    wind_name_3=''
                else:
                    wind_name_3=wind_name_3+i

        wind_name_4= ''
        for i in wind_4:
                if i =='/':
                    wind_name_4=''
                else:
                    wind_name_4=wind_name_4+i

        path_wind = wind_2[0:(len(wind_2)-len(wind_name_2))]

        #################### MODIFY EVERY INFLOW PATH #################### 
        wind_inflow= open(new_path+'Inflow.dat').read().splitlines() 
        wind_inflow[15]='"'+path_modules+path_wind+wind_name_2+'"    Filename       - Filename of time series data for uniform wind field.      (-)'
        wind_inflow[19]='"'+path_modules+path_wind+wind_name_3+'"    Filename       - Name of the Full field wind file to use (.bts)'
        wind_inflow[21]= '"'+path_modules+path_wind+wind_name_4+'"    FilenameRoot   - Rootname of the full-field wind file to use (.wnd, .sum)'
        open(new_path+'Inflow.dat','w').write('\n'.join(wind_inflow))  

        ## Elasto_Dyn ##
        inserte = open(new_path+'Elasto.dat').read().splitlines()
        inserte[5]='    %f  DT          - Integration time step (s)'%((1/frequency)/10)
        inserte[87] = '"'+path_modules+Blade1+'"    BldFile(1)  - Name of file containing properties for blade 1 (quoted string)'
        inserte[88]= '"'+path_modules+Blade2+'"     BldFile(2)  - Name of file containing properties for blade 1 (quoted string)'
        inserte[89]= '"'+path_modules+Blade3+'"     BldFile(3)  - Name of file containing properties for blade 1 (quoted string)'
        inserte[109]='"'+path_modules+Tower+'"    TwrFile     - Name of file containing tower properties (quoted string)'
        inserte[119]='          1   NBlGages    - Number of blade nodes that have strain gages for output [0 to 9] (-)'
        inserte[120]='         5   BldGagNd    - List of blade nodes that have strain gages [1 to BldNodes] (-) [unused if NBlGages=0]'
        open(new_path+'Elasto.dat','w').write('\n'.join(inserte))

        f = open(new_path+'Elasto.dat','r')
        lines = f.readlines()
        f.close()
        size = len(lines)
        f = open(new_path+'Elasto.dat',"w")
        a =0
        for line in lines:
                if a <(size-2):
                    f.write(line)
                    a=a+1
        f.close()

        with open(new_path+'Elasto.dat', 'a') as file:
                if any('"RootMyb1"' in l for l in lines)==False:
                    file.write('"RootMyb1"\n')                      ## Blade root flapwise bending moment (1)
                if any('"RootMyb2"' in l for l in lines)==False:
                    file.write('"RootMyb2"\n')                      ## Blade root flapwise bending moment (2)
                if any('"RootMyb3"' in l for l in lines)==False:
                    file.write('"RootMyb3"\n')                      ## Blade root flapwise bending moment (3)
                if any('"RootMxb1"' in l for l in lines)==False:
                    file.write('"RootMxb1"\n')                      ## Blade root edgewise bending moment (1)
                if any('"RootMxb2"' in l for l in lines)==False:
                    file.write('"RootMxb2"\n')                      ## Blade root edgewise bending moment (2)
                if any('"RootMxb3"' in l for l in lines)==False:
                    file.write('"RootMxb3"\n')                      ## Blade root edgewise bending moment (3)
                if any('"LSSTipMys"' in l for l in lines)==False:
                    file.write('"LSSTipMys"\n')                     ## Rotor Tilt
                if any('"LssTipMzs"' in l for l in lines)==False:
                    file.write('"LssTipMzs"\n')                     ## Rotor Yaw
                if any('"LSShftMxa"' in l for l in lines)==False:
                    file.write('"LSShftMxa"\n')                     ## Rotor Torque
                if any('"TwrBsMyt"' in l for l in lines)==False:
                    file.write('"TwrBsMyt"\n')                     ## Tower base normal moment
                if any('"TwrBsMxt"' in l for l in lines)==False:
                    file.write('"TwrBsMxt"\n')                     ## Tower base lateral moment
                if any('"RootMzc1"' in l for l in lines)==False:
                    file.write('"RootMzc1"\n')                      ## Pitch Actuation Loads (1)
                if any('"RootMzc2"' in l for l in lines)==False:
                    file.write('"RootMzc2"\n')                      ## Pitch Actuation Loads (2)
                if any('"RootMzc3"' in l for l in lines)==False:
                    file.write('"RootMzc3"\n')                      ## Pitch Actuation Loads (3)
                if any('"Spn1MLzb1"' in l for l in lines)==False:
                    file.write('"Spn1MLzb1"\n')                     ## Blade pitching moment at span location (1)
                if any('"Spn1MLzb2"' in l for l in lines)==False:
                    file.write('"Spn1MLzb2"\n')                     ## Blade pitching moment at span location (2)
                if any('"Spn1MLzb3"' in l for l in lines)==False:
                    file.write('"Spn1MLzb3"\n')                     ## Blade pitching moment at span location (3)
                if any('"YawBrTAxp"' in l for l in lines)==False:
                    file.write('"YawBrTAxp"\n')                     ## Tower-top acceleration normal
                if any('"YawBrTAyp"' in l for l in lines)==False:
                    file.write('"YawBrTAyp"\n')                     ## Tower-top acceleration lateral
                if any('"TwHt1MLyt"' in l for l in lines)==False:
                    file.write('"TwHt1MLyt"\n')                     ## Tower normal moment at span location 
                if any('"TwHt1MLxt"' in l for l in lines)==False:
                    file.write('"TwHt1MLxt"\n')                     ## Tower lateral moment at span location 
                if any('"YawBrMyp"' in l for l in lines)==False:
                    file.write('"YawBrMyp"\n')                      ## Tower top normal moment 
                if any('"YawBrMxp"' in l for l in lines)==False:
                    file.write('"YawBrMxp"\n')                      ## Tower top lateral moment
                if any('"TwrBsMzt"' in l for l in lines)==False:
                    file.write('"TwrBsMzt"\n')                      ## Tower Torque
                if any('"RotPwr"' in l for l in lines)==False:
                    file.write('"RotPwr"\n')                        ## Generator Power
                if any('"GenSpeed"' in l for l in lines)==False:
                    file.write('"GenSpeed"\n')                      ## Generator Speed
                if any('"RotSpeed"' in l for l in lines)==False:
                    file.write('"RotSpeed"\n')                     ## Rotor Speed
                if any('"Azimuth"' in l for l in lines)==False:
                    file.write('"Azimuth"\n')                      ## Azimuth Angle 
                if any('"BldPitch1"' in l for l in lines)==False:
                    file.write('"BldPitch1"\n')                     ## Blade pitch angle (1)
                if any('"BldPitch2"' in l for l in lines)==False:
                    file.write('"BldPitch2"\n')                     ## Blade pitch angle (2)
                if any('"BldPitch3"' in l for l in lines)==False:
                    file.write('"BldPitch3"\n')                     ## Blade pitch angle (3)
                file.write('END of input file (the word "END" must appear in the first 3 columns of this last OutList line)\n')
                file.write('---------------------------------------------------------------------------------------')
                    
        #Servo_Dyn
        insertdt = open(new_path+'Servo.dat').read().splitlines()
        insertdt[4]='   %f   DT           - Communication interval for controllers (s) (or "default")'%((1/frequency)/10)
        open(new_path+'Servo.dat','w').write('\n'.join(insertdt))

        f = open(new_path+'Servo.dat','r')
        lines = f.readlines()
        f.close()
        size = len(lines)
        f = open(new_path+'Servo.dat',"w")
        a =0
        for line in lines:
                if a <(size-2):
                    f.write(line)
                    a=a+1
        f.close()

        with open(new_path+'Servo.dat', 'a') as file:
                if any('"GenTq"' in l for l in lines)==False:
                    file.write('"GenTq"\n')                      ## Generator torque
                if any('"GenPwr"' in l for l in lines)==False:
                    file.write('"GenPwr"\n')                      ## Generator Power            
                file.write('END of input file (the word "END" must appear in the first 3 columns of this last OutList line)\n')
                file.write('---------------------------------------------------------------------------------------')
            
        ### .fst ##                      
        insertmod=open(str_fast).read().splitlines()
        insertmod[5]='        %i   TMax            - Total run time (s)'%(s)
        insertmod[6]='   %f   DT              - Recommended module time step (s)'%((1/frequency)/10)
        insertmod[21]='"'+new_path+'Elasto.dat"    EDFile          - Name of file containing ElastoDyn input parameters (quoted string)'
        insertmod[22]='"'+new_path+'Beam1.dat"    BDBldFile(1)    - Name of file containing BeamDyn input parameters for blade 1 (quoted string)'
        insertmod[23]='"'+new_path+'Beam2.dat"    BDBldFile(2)    - Name of file containing BeamDyn input parameters for blade 2 (quoted string)'
        insertmod[24]='"'+new_path+'Beam3.dat"    BDBldFile(3)    - Name of file containing BeamDyn input parameters for blade 3 (quoted string)'
        insertmod[25]='"'+new_path+'Inflow.dat"    InflowFile      - Name of file containing inflow wind input parameters (quoted string)'
        insertmod[26]='"'+new_path+'Aero.dat"    AeroFile        - Name of file containing aerodynamic input parameters (quoted string)'
        insertmod[27]='"'+new_path+'Servo.dat"    ServoFile       - Name of file containing control and electrical-drive input parameters (quoted string)'
        insertmod[28]='"'+new_path+'Hydro.dat"    HydroFile       - Name of file containing hydrodynamic input parameters (quoted string)'
        insertmod[29]='"'+new_path+'Sub.dat"     SubFile         - Name of file containing sub-structural input parameters (quoted string)'
        insertmod[30]='"'+new_path+'Moor.dat"      MooringFile     - Name of file containing mooring system input parameters (quoted string)'
        insertmod[31]='"'+new_path+'Ice.dat"      IceFile         - Name of file containing ice input parameters (quoted string)'
        insertmod[36]='   %f    DT_Out          - Time step for tabular output (s) (or "default")'%(1/frequency)
        insertmod[37]='        30   TStart          - Time to begin tabular output (s)'
        open(str_fast,'w').write('\n'.join(insertmod))
             
        ## Aero_Dyn
        if len(insert_aerocomponents) > 40:
                insert_new_aero=open(new_path+'Aero.dat').read().splitlines()
                insert_new_aero[14]='   %f   DTAero       - Time interval for aerodynamic calculations (sec)'%((1/frequency)/10)
                for i in range(len(insert_aerocomponents)):       
                        aerodyn_line =insert_new_aero[i].split()
                        if aerodyn_line[0]=='"'+Aero_blade1+'"':
                                insert_new_aero[i]='"'+path_modules+Aero_blade1+'"    ADBlFile(1)       - Name of file containing distributed aerodynamic properties for Blade #1 (-)'
                        elif aerodyn_line[0]=='"'+Aero_blade2+'"':
                                insert_new_aero[i]='"'+path_modules+Aero_blade2+'"    ADBlFile(2)        - Name of file containing distributed aerodynamic properties for Blade #2 (-)'
                        elif aerodyn_line[0]=='"'+Aero_blade3+'"':
                                insert_new_aero[i]='"'+path_modules+Aero_blade3+'"    ADBlFile(3)        - Name of file containing distributed aerodynamic properties for Blade #3(-)'

                
                open(new_path+'Aero.dat','w').write('\n'.join(insert_new_aero))

                f = open(new_path+'Aero.dat','r')
                lines = f.readlines()
                f.close()
                size = len(lines)
                f = open(new_path+'Aero.dat',"w")
                a =0
                for line in lines:
                        if a <(size-2):
                            f.write(line)
                            a=a+1
                f.close()

                with open(new_path+'Aero.dat', 'a') as file:
                        if any('"RtSkew"' in l for l in lines)==False:
                            file.write('"RtSkew"\n')                      ## Rotor Skew
                        if any('"RtAeroCp"' in l for l in lines)==False:
                            file.write('"RtAeroCp"\n')                      ## Aerodynamic CP 
                        if any('"RtAeroCt"' in l for l in lines)==False:
                            file.write('"RtAeroCt"\n')                      ## Aerodynamic CT  
                        file.write('END of input file (the word "END" must appear in the first 3 columns of this last OutList line)\n')
                        file.write('---------------------------------------------------------------------------------------')
                
        else:
                insert_aerocomponents = open(new_path+'Aero.dat').read().splitlines()
                insert_aerocomponents[14]='   %f   DTAero       - Time interval for aerodynamic calculations (sec)'%((1/frequency)/10)
                open(new_path+'Aero.dat','w').write('\n'.join(insert_aerocomponents))

        if os.path.exists(new_path+'/pitch.ipt')==False:
                pitch = open(path_fast+'pitch.ipt').read().splitlines()
                pitcht = open(new_path+'/pitch.ipt','w')
                for line in pitch:
                        pitcht.write(line+'\n')
                pitcht.close()
                   
        # Run Fast
        subprocess.run([path_fast+'fast_x64d', str_fast])

def data(parameters):

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
        from_to=parameters[10]
        frequency = parameters[11]
        simulink = parameters[12]

        path_modules=path_modules+'/'
        path_fast = path_fast+'/'

        fast_input = open(path_fast+turbinefast).read().splitlines()
        turbinefast = turbinefast[0:len(turbinefast)-4]

        wind_speed = np.arange(3.0,25.5,0.5)
        turbulence_intensity=np.arange(1.0,31.0,1.0)
        n_1=from_to[0]
        n_2=from_to[1]
        
        for v in wind_speed:
                for t in turbulence_intensity:
                        for n in range(n_1,n_2+1):
                                if os.path.isdir(path_fast+turbinefast+' Fundamental Load quantities - IEC61400.13 - Fast/'+turbinefast+' - '+str(s)+'s of duration bins/'+turbinefast+'-'+str(v)+'ms')==False:
                                        print('You need all the simulations from IEC6140013.simulations for plotting!')
                                        
                                sim_path = path_fast+turbinefast+' Fundamental Load quantities - IEC61400.13 - Fast/'+turbinefast+' - '+str(s)+'s of duration bins/'+turbinefast+'-'+str(v)+'ms/'

                                out_file = sim_path+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'.out'

                                out_file_noHeaderStr = out_file[0:len(out_file)-4]+"noHeader.out"
                                out_file_csv = out_file[0:len(out_file)-4]+"noHeader.csv"
                                
                                output_data= sim_path+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+' Data/'
                                
                                if os.path.exists(out_file_csv+'.csv')==False:
                                        out_header = open(out_file).read().splitlines()
                                        out_noHeader = open(out_file_noHeaderStr,'w')

                                        i = 0
                                        for linha in out_header:
                                                if i >5:
                                                        out_noHeader.write(linha+'\n')
                                                else:
                                                        i=i+1
                                        out_noHeader.close()

                                        df = pd.read_fwf(out_file_noHeaderStr)
                                        df.to_csv(out_file_csv)
                                        
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
        from_to=parameters[10]
        frequency = parameters[11]
        simulink = parameters[12]

        path_modules=path_modules+'/'
        path_fast = path_fast+'/'

        fast_input = open(path_fast+turbinefast).read().splitlines()
        turbinefast = turbinefast[0:len(turbinefast)-4]

        wind_speed = np.arange(3.0,25.5,0.5)
        turbulence_intensity=np.arange(1.0,31.0,1.0)
        n_1=from_to[0]
        n_2=from_to[1]
        
        for v in wind_speed:
                for t in turbulence_intensity:
                        for n in range(n_1,n_2+1):
                                if os.path.isdir(path_fast+turbinefast+' Fundamental Load quantities - IEC61400.13 - Fast/'+turbinefast+' - '+str(s)+'s of duration bins/'+turbinefast+'-'+str(v)+'ms')==False:
                                        print('You need all the simulations from IEC6140013.simulations for plotting!')
                                        
                                sim_path = path_fast+turbinefast+' Fundamental Load quantities - IEC61400.13 - Fast/'+turbinefast+' - '+str(s)+'s of duration bins/'+turbinefast+'-'+str(v)+'ms/'

                                out_file = sim_path+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'.out'

                                out_file_noHeaderStr = out_file[0:len(out_file)-4]+"noHeader.out"
                                out_file_csv = out_file[0:len(out_file)-4]+"noHeader.csv"
                                
                                output_data= sim_path+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+' Data/'
                                
                                if os.path.exists(out_file_csv+'.csv')==False:
                                        out_header = open(out_file).read().splitlines()
                                        out_noHeader = open(out_file_noHeaderStr,'w')

                                        i = 0
                                        for linha in out_header:
                                                if i >5:
                                                        out_noHeader.write(linha+'\n')
                                                else:
                                                        i=i+1
                                        out_noHeader.close()

                                        df = pd.read_fwf(out_file_noHeaderStr)
                                        df.to_csv(out_file_csv)
                                        
                                ## Get data

                                dataIndex =  pd.read_csv(out_file_csv)
                                data_normal_col = pd.read_csv(out_file_csv,header=None)

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
                                xmin =0.1
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

                                BladeRootFlapWiseM2Index = dataIndex.columns.get_loc("RootMxb2")
                                BladeRootFlapWiseM2Normal = data_normal_col.iloc[2:,BladeRootFlapWiseM2Index]
                                BladeRootFlapWiseM2Normal = [float(x) for x in BladeRootFlapWiseM2Normal]

                                BladeRootFlapWiseM3Index = dataIndex.columns.get_loc("RootMxb3")
                                BladeRootFlapWiseM3Normal = data_normal_col.iloc[2:,BladeRootFlapWiseM3Index]
                                BladeRootFlapWiseM3Normal = [float(x) for x in BladeRootFlapWiseM3Normal]

                                ## Time Series

                                plt.figure()
                                figure = plt.gcf()
                                figure.set_size_inches(inches_x_time_series,inches_y_time_series)
                                plt.subplot(3,1,1)
                                plt.plot(Time,BladeRootFlapWiseM1Normal)
                                plt.title('Blade Root Flapwise Moments\nBlade 1',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                plt.tight_layout()

                                plt.subplot(3,1,2)
                                plt.plot(Time,BladeRootFlapWiseM2Normal)
                                plt.title('Blade 2',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                plt.tight_layout()

                                plt.subplot(3,1,3)
                                plt.plot(Time,BladeRootFlapWiseM3Normal)
                                plt.title('Blade 3',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.xlabel('Time(s)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity',fontsize=font_size)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
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

                                plt.plot(Freq_mirror[0:cut],BladeRootFlapWiseM1NormalFFT[0:cut])
                                plt.title('Blade Root Flapwise Moments FFT\nBlade 1',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax= max(BladeRootFlapWiseM1NormalFFT[y0:yf])
                                axes = plt.gca()
                                axes.set_xlim([xmin,xmax])
                                axes.set_ylim([ymin,ymax])
                                plt.tight_layout()

                                plt.subplot(3,1,2)
                                BladeRootFlapWiseM2NormalFFT = fft(BladeRootFlapWiseM2Normal,N)
                                BladeRootFlapWiseM2NormalFFT=np.abs(BladeRootFlapWiseM2NormalFFT)
                                BladeRootFlapWiseM2NormalFFT=BladeRootFlapWiseM2NormalFFT/(N/2)

                                plt.plot(Freq_mirror[0:cut],BladeRootFlapWiseM2NormalFFT[0:cut])
                                plt.title('Blade 2',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax = max(BladeRootFlapWiseM2NormalFFT[y0:yf])
                                axes = plt.gca()
                                axes.set_xlim([xmin,xmax])
                                axes.set_ylim([ymin,ymax])
                                plt.tight_layout()

                                plt.subplot(3,1,3)
                                BladeRootFlapWiseM3NormalFFT = fft(BladeRootFlapWiseM3Normal,N)
                                BladeRootFlapWiseM3NormalFFT=np.abs(BladeRootFlapWiseM3NormalFFT)
                                BladeRootFlapWiseM3NormalFFT=BladeRootFlapWiseM3NormalFFT/(N/2)
                                plt.plot(Freq_mirror[0:cut],BladeRootFlapWiseM3NormalFFT[0:cut])
                                plt.title('Blade 3',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.xlabel('Frequency(Hz)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity',fontsize=font_size)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax = max(BladeRootFlapWiseM3NormalFFT[y0:yf])
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

                                BladeRootEdgeWiseM2Index = dataIndex.columns.get_loc("RootMyb2")
                                BladeRootEdgeWiseM2Normal = data_normal_col.iloc[2:,BladeRootEdgeWiseM2Index]
                                BladeRootEdgeWiseM2Normal = [float(x) for x in BladeRootEdgeWiseM2Normal]

                                BladeRootEdgeWiseM3Index = dataIndex.columns.get_loc("RootMyb3")
                                BladeRootEdgeWiseM3Normal = data_normal_col.iloc[2:,BladeRootEdgeWiseM3Index]
                                BladeRootEdgeWiseM3Normal = [float(x) for x in BladeRootEdgeWiseM3Normal]

                                ## Time Series

                                plt.figure()
                                figure = plt.gcf()
                                figure.set_size_inches(inches_x_time_series,inches_y_time_series)
                                plt.subplot(3,1,1)
                                plt.plot(Time,BladeRootEdgeWiseM1Normal)
                                plt.title('Blade Root Edgewise Moments\nBlade 1',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                plt.tight_layout()

                                plt.subplot(3,1,2)
                                plt.plot(Time,BladeRootEdgeWiseM2Normal)
                                plt.title('Blade 2',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                plt.tight_layout()

                                plt.subplot(3,1,3)
                                plt.plot(Time,BladeRootEdgeWiseM3Normal)
                                plt.title('Blade 3',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.xlabel('Time(s)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity',fontsize=font_size)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
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

                                plt.plot(Freq_mirror[0:cut],BladeRootEdgeWiseM1NormalFFT[0:cut])
                                plt.title('Blade Root Edgewise Moments FFT\nBlade 1',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax= max(BladeRootEdgeWiseM1NormalFFT[y0:yf])
                                axes = plt.gca()
                                axes.set_xlim([xmin,xmax])
                                axes.set_ylim([ymin,ymax])
                                plt.tight_layout()

                                plt.subplot(3,1,2)
                                BladeRootEdgeWiseM2NormalFFT = fft(BladeRootEdgeWiseM2Normal,N)
                                BladeRootEdgeWiseM2NormalFFT=np.abs(BladeRootEdgeWiseM2NormalFFT)
                                BladeRootEdgeWiseM2NormalFFT=BladeRootEdgeWiseM2NormalFFT/(N/2)

                                plt.plot(Freq_mirror[0:cut],BladeRootEdgeWiseM2NormalFFT[0:cut])
                                plt.title('Blade 2',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax = max(BladeRootEdgeWiseM2NormalFFT[y0:yf])
                                axes = plt.gca()
                                axes.set_xlim([xmin,xmax])
                                axes.set_ylim([ymin,ymax])
                                plt.tight_layout()

                                plt.subplot(3,1,3)
                                BladeRootEdgeWiseM3NormalFFT = fft(BladeRootEdgeWiseM3Normal,N)
                                BladeRootEdgeWiseM3NormalFFT=np.abs(BladeRootEdgeWiseM3NormalFFT)
                                BladeRootEdgeWiseM3NormalFFT=BladeRootEdgeWiseM3NormalFFT/(N/2)

                                plt.plot(Freq_mirror[0:cut],BladeRootEdgeWiseM3NormalFFT[0:cut])
                                plt.title('Blade 3',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.xlabel('Frequency (Hz)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity',fontsize=font_size)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax = max(BladeRootEdgeWiseM3NormalFFT[y0:yf])
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

                                RotorYawMomentIndex = dataIndex.columns.get_loc("YawBrMzn")
                                RotorYawMomentNormal = data_normal_col.iloc[2:,RotorYawMomentIndex]
                                RotorYawMomentNormal = [float(x) for x in RotorYawMomentNormal]

                                RotorTorqueIndex = dataIndex.columns.get_loc("LSShftMxa")
                                RotorTorqueNormal = data_normal_col.iloc[2:,RotorTorqueIndex]
                                RotorTorqueNormal = [float(x) for x in RotorTorqueNormal]

                                ## Time Series

                                plt.figure()
                                figure = plt.gcf()
                                figure.set_size_inches(inches_x_time_series,inches_y_time_series)
                                plt.subplot(3,1,1)
                                plt.plot(Time,RotorTiltMomentNormal)
                                plt.title('Rotor Quantities\nTilt Moment',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                plt.tight_layout()

                                plt.subplot(3,1,2)
                                plt.plot(Time,RotorYawMomentNormal)
                                plt.title('Yaw Moment',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                plt.tight_layout()

                                plt.subplot(3,1,3)
                                plt.plot(Time,RotorTorqueNormal)
                                plt.title('Rotor Torque',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.xlabel('Time(s)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity',fontsize=font_size)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
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

                                plt.plot(Freq_mirror[0:cut],RotorTiltMomentNormalFFT[0:cut])
                                plt.title('Rotor Quantities FFT\nTilt Moment',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax=max(RotorTiltMomentNormalFFT[y0:yf])
                                axes = plt.gca()
                                axes.set_xlim([xmin,xmax])
                                axes.set_ylim([ymin,ymax])
                                plt.tight_layout()

                                plt.subplot(3,1,2)
                                RotorYawMomentNormalFFT = fft(RotorYawMomentNormal)
                                RotorYawMomentNormalFFT=np.abs(RotorYawMomentNormalFFT)
                                RotorYawMomentNormalFFT=RotorYawMomentNormalFFT/(N/2)

                                plt.plot(Freq_mirror[0:cut],RotorYawMomentNormalFFT[0:cut])
                                plt.title('Yaw Moment',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax=max(RotorYawMomentNormalFFT[y0:yf])
                                axes = plt.gca()
                                axes.set_xlim([xmin,xmax])
                                axes.set_ylim([ymin,ymax])
                                plt.tight_layout()

                                plt.subplot(3,1,3)
                                RotorTorqueNormalFFT = fft(RotorTorqueNormal)
                                RotorTorqueNormalFFT=np.abs(RotorTorqueNormalFFT)
                                RotorTorqueNormalFFT=RotorTorqueNormalFFT/(N/2)

                                plt.plot(Freq_mirror[0:cut],RotorTorqueNormalFFT[0:cut])
                                plt.title('Rotor torque',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.xlabel('Frequency (Hz)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity',fontsize=font_size)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax=max(RotorTorqueNormalFFT[y0:yf])
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


                                TowerBaseLateralIndex = dataIndex.columns.get_loc("TwrBsMxt")
                                TowerBaseLateralNormal = data_normal_col.iloc[2:,TowerBaseLateralIndex]
                                TowerBaseLateralNormal = [float(x) for x in TowerBaseLateralNormal]

                                TowerTorqueIndex = dataIndex.columns.get_loc("TwrBsMxt")
                                TowerTorqueNormal = data_normal_col.iloc[2:,TowerTorqueIndex]
                                TowerTorqueNormal = [float(x) for x in TowerTorqueNormal]

                                ## Time Series

                                plt.figure()
                                figure = plt.gcf()
                                figure.set_size_inches(inches_x_time_series,inches_y_time_series)
                                plt.subplot(3,1,1)
                                plt.title('Tower Moments\nBase Normal')
                                plt.plot(Time,TowerBaseNormalNormal)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                plt.tight_layout()

                                plt.subplot(3,1,2)
                                plt.plot(Time,TowerBaseLateralNormal)
                                plt.title('Base Lateral',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                plt.tight_layout()

                                plt.subplot(3,1,3)
                                plt.plot(Time,TowerTorqueNormal)
                                plt.title('Torque',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.xlabel('Time(s)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity',fontsize=font_size)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
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

                                plt.plot(Freq_mirror[0:cut],TowerBaseNormalNormalFFT[0:cut])
                                plt.title('Tower base moments FFT\nNormal Moment',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax= max(TowerBaseNormalNormalFFT[y0:yf])
                                axes = plt.gca()
                                axes.set_xlim([xmin,xmax])
                                axes.set_ylim([ymin,ymax])
                                plt.tight_layout()

                                plt.subplot(3,1,2)
                                TowerBaseLateralNormalFFT = fft(TowerBaseLateralNormal)
                                TowerBaseLateralNormalFFT=np.abs(TowerBaseLateralNormalFFT)
                                TowerBaseLateralNormalFFT=TowerBaseLateralNormalFFT/(N/2)

                                plt.plot(Freq_mirror[0:cut],TowerBaseLateralNormalFFT[0:cut])
                                plt.title('Lateral Moment',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax= max(TowerBaseLateralNormalFFT[y0:yf])
                                axes = plt.gca()
                                axes.set_xlim([xmin,xmax])
                                axes.set_ylim([ymin,ymax])
                                plt.tight_layout()

                                plt.subplot(3,1,3)
                                TowerTorqueNormalFFT = fft(TowerTorqueNormal)
                                TowerTorqueNormalFFT=np.abs(TowerTorqueNormalFFT)
                                TowerTorqueNormalFFT=TowerTorqueNormalFFT/(N/2)

                                plt.plot(Freq_mirror[0:cut],TowerTorqueNormalFFT[0:cut])
                                plt.title('Tower torque',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.xlabel('Frequency (Hz)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity',fontsize=font_size)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax= max(TowerTorqueNormalFFT[y0:yf])
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

                                PitchActuationoLoad2Index = dataIndex.columns.get_loc("RootMzc2")
                                PitchActuationoLoad2Normal = data_normal_col.iloc[2:,PitchActuationoLoad2Index]
                                PitchActuationoLoad2Normal = [float(x) for x in PitchActuationoLoad2Normal]

                                PitchActuationoLoad3Index = dataIndex.columns.get_loc("RootMzc3")
                                PitchActuationoLoad3Normal = data_normal_col.iloc[2:,PitchActuationoLoad3Index]
                                PitchActuationoLoad3Normal = [float(x) for x in PitchActuationoLoad3Normal]

                                ## Time Series

                                plt.figure()
                                figure = plt.gcf()
                                figure.set_size_inches(inches_x_time_series,inches_y_time_series)
                                plt.subplot(3,1,1)
                                plt.plot(Time,PitchActuationoLoad1Normal)
                                plt.title('Pitch actuation loads\nBlade 1',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                plt.tight_layout()

                                plt.subplot(3,1,2)
                                plt.plot(Time,PitchActuationoLoad2Normal)
                                plt.title('Blade 2',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                plt.tight_layout()

                                plt.subplot(3,1,3)
                                plt.plot(Time,PitchActuationoLoad3Normal)
                                plt.title(' Blade 3',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.xlabel('Time(s)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity',fontsize=font_size)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
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
                                plt.plot(Freq_mirror[0:cut],PitchActuationoLoad1NormalFFT[0:cut])
                                plt.title('Pitch actuation loads FFT\nBlade 1',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax= max(PitchActuationoLoad1NormalFFT[y0:yf])
                                axes = plt.gca()
                                axes.set_xlim([xmin,xmax])
                                axes.set_ylim([ymin,ymax])
                                plt.tight_layout()

                                plt.subplot(3,1,2)
                                PitchActuationoLoad2NormalFFT = fft(PitchActuationoLoad2Normal)
                                PitchActuationoLoad2NormalFFT=np.abs(PitchActuationoLoad2NormalFFT)
                                PitchActuationoLoad2NormalFFT=PitchActuationoLoad2NormalFFT/(N/2)
                                plt.plot(Freq_mirror[0:cut],PitchActuationoLoad2NormalFFT[0:cut])
                                plt.title('Blade 2',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax= max(PitchActuationoLoad2NormalFFT[y0:yf])
                                axes = plt.gca()
                                axes.set_xlim([xmin,xmax])
                                axes.set_ylim([ymin,ymax])
                                plt.tight_layout()

                                plt.subplot(3,1,3)
                                PitchActuationoLoad3NormalFFT = fft(PitchActuationoLoad3Normal)
                                PitchActuationoLoad3NormalFFT=np.abs(PitchActuationoLoad3NormalFFT)
                                PitchActuationoLoad3NormalFFT=PitchActuationoLoad3NormalFFT/(N/2)
                                plt.plot(Freq_mirror[0:cut],PitchActuationoLoad3NormalFFT[0:cut])
                                plt.title('Blade 3',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.box(on=None)
                                plt.grid(True)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                ymax= max(PitchActuationoLoad3NormalFFT[y0:yf])
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

                                TowerTopAccelerationLaterallIndex = dataIndex.columns.get_loc("YawBrTAyp")
                                TowerTopAccelerationLateralNormal = data_normal_col.iloc[2:,TowerTopAccelerationLaterallIndex]
                                TowerTopAccelerationLateralNormal = [float(x) for x in TowerTopAccelerationLateralNormal]

                                ## Time Series

                                plt.figure()
                                figure = plt.gcf()
                                figure.set_size_inches(inches_x_time_series,inches_y_time_series)
                                plt.subplot(2,1,1)
                                plt.plot(Time,TowerTopAccelerationNormalNormal)
                                plt.title('Tower Top Accelerations\nNormal direction',fontsize=font_size)
                                plt.ylabel('m/s²',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                plt.tight_layout()

                                plt.subplot(2,1,2)
                                plt.plot(Time,TowerTopAccelerationLateralNormal)
                                plt.title('Lateral direction',fontsize=font_size)
                                plt.ylabel('m/s²',fontsize=font_size)
                                plt.xlabel('Time(s)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity',fontsize=font_size)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
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

                                plt.plot(Freq_mirror[0:cut],TowerTopAccelerationNormalNormalFFT[0:cut])
                                plt.title('Tower top accelerations FFT\nNormal direction',fontsize=font_size)
                                plt.ylabel('m/s²',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax= max(TowerTopAccelerationNormalNormalFFT[y0:yf])
                                axes = plt.gca()
                                axes.set_xlim([xmin,xmax])
                                axes.set_ylim([ymin,ymax])
                                plt.tight_layout()

                                plt.subplot(2,1,2)
                                TowerTopAccelerationLateralNormalFFT = fft(TowerTopAccelerationLateralNormal)
                                TowerTopAccelerationLateralNormalFFT=np.abs(TowerTopAccelerationLateralNormalFFT)
                                TowerTopAccelerationLateralNormalFFT=TowerTopAccelerationLateralNormalFFT/(N/2)

                                plt.plot(Freq_mirror[0:cut],TowerTopAccelerationLateralNormalFFT[0:cut])
                                plt.title('Lateral direction',fontsize=font_size)
                                plt.ylabel('m/s²',fontsize=font_size)
                                plt.xlabel('Frequency (Hz)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity',fontsize=font_size)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None) 
                                plt.grid(True)  
                                ymax= max(TowerTopAccelerationLateralNormalFFT[y0:yf])
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
                                
                                TowerMidLateralIndex = dataIndex.columns.get_loc("TwHt1MLxt")
                                TowerMidLateralNormal = data_normal_col.iloc[2:,TowerMidLateralIndex]
                                TowerMidLateralNormal = [float(x) for x in TowerMidLateralNormal]


                                ## Time Series

                                plt.figure()
                                figure = plt.gcf()
                                figure.set_size_inches(inches_x_time_series,inches_y_time_series)
                                plt.subplot(2,1,1)
                                plt.plot(Time,TowerMidNormalNormal)
                                plt.title('Tower mid Moments\nNormal',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                plt.tight_layout()

                                plt.subplot(2,1,2)
                                plt.plot(Time,TowerMidLateralNormal)
                                plt.title('Lateral',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.xlabel('Time (s)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity',fontsize=font_size)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
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

                                plt.plot(Freq_mirror[0:cut],TowerMidNormalNormalFFT[0:cut])
                                plt.title('Tower mid moments FFT\nNormal',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax= max(TowerMidNormalNormalFFT[y0:yf])
                                axes = plt.gca()
                                axes.set_xlim([xmin,xmax])
                                axes.set_ylim([ymin,ymax])
                                plt.tight_layout()

                                plt.subplot(2,1,2)
                                TowerMidLateralNormalFFT = fft(TowerMidLateralNormal)
                                TowerMidLateralNormalFFT=np.abs(TowerMidLateralNormalFFT)
                                TowerMidLateralNormalFFT=TowerMidLateralNormalFFT/(N/2)

                                plt.plot(Freq_mirror[0:cut],TowerMidLateralNormalFFT[0:cut])
                                plt.title('Lateral',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.xlabel('Frequency (Hz)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity',fontsize=font_size)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax= max(TowerMidLateralNormalFFT[y0:yf])
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

                                TowerTopLateralIndex = dataIndex.columns.get_loc("YawBrMxp")
                                TowerTopLateralNormal = data_normal_col.iloc[2:,TowerTopLateralIndex]
                                TowerTopLateralNormal = [float(x) for x in TowerTopLateralNormal]

                                ## Time Series

                                plt.figure()
                                figure = plt.gcf()
                                figure.set_size_inches(inches_x_time_series,inches_y_time_series)
                                plt.subplot(2,1,1)
                                plt.plot(Time,TowerTopNormalNormal)
                                plt.title('Tower top Moments\nNormal',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                plt.tight_layout()

                                plt.subplot(2,1,2)
                                plt.plot(Time,TowerTopLateralNormal)
                                plt.title('Lateral',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.xlabel('Time (s)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity',fontsize=font_size)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
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

                                plt.plot(Freq_mirror[0:cut],TowerTopMomentNormalNormalFFT[0:cut])
                                plt.title('Tower top Moments FFT\nNormal',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax= max(TowerTopMomentNormalNormalFFT[y0:yf])
                                axes = plt.gca()
                                axes.set_xlim([xmin,xmax])
                                axes.set_ylim([ymin,ymax])
                                plt.tight_layout()

                                plt.subplot(2,1,2)
                                TowerTopLateralNormalFFT = fft(TowerTopLateralNormal)
                                TowerTopLateralNormalFFT=np.abs(TowerTopLateralNormalFFT)
                                TowerTopLateralNormalFFT=TowerTopLateralNormalFFT/(N/2)

                                plt.plot(Freq_mirror[0:cut],TowerTopLateralNormalFFT[0:cut])
                                plt.title('Lateral',fontsize=font_size)
                                plt.ylabel('kN.m',fontsize=font_size)
                                plt.xlabel('Frequency (Hz)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity',fontsize=font_size)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax= max(TowerTopLateralNormalFFT[y0:yf])
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

                                GeneratorSpeedIndex = dataIndex.columns.get_loc("GenSpeed")
                                GeneratorSpeedNormal = data_normal_col.iloc[2:,GeneratorSpeedIndex]
                                GeneratorSpeedNormal = [float(x) for x in GeneratorSpeedNormal]

                                RotorSpeedIndex = dataIndex.columns.get_loc("RotSpeed")
                                RotorSpeedNormal = data_normal_col.iloc[2:,RotorSpeedIndex]
                                RotorSpeedNormal = [float(x) for x in RotorSpeedNormal]

                                AzimuthAngleIndex = dataIndex.columns.get_loc("Azimuth")
                                AzimuthAngleNormal = data_normal_col.iloc[2:,AzimuthAngleIndex]
                                AzimuthAngleNormal = [float(x) for x in AzimuthAngleNormal]

                                ## Time Series

                                plt.figure()
                                figure = plt.gcf()
                                figure.set_size_inches(inches_x_time_series,inches_y_time_series)   
                                plt.subplot(4,1,1)
                                plt.plot(Time,RotorPowerNormal)
                                plt.title('General quantities\nPower',fontsize=font_size)
                                plt.ylabel('MW',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                plt.tight_layout()

                                plt.subplot(4,1,2)
                                plt.plot(Time,GeneratorSpeedNormal)
                                plt.title('Generator Speed',fontsize=font_size)
                                plt.ylabel('RPM',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                plt.tight_layout()

                                plt.subplot(4,1,3)
                                plt.plot(Time,RotorSpeedNormal)
                                plt.title('Rotor Speed',fontsize=font_size)
                                plt.ylabel('RPM',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                plt.tight_layout()

                                plt.subplot(4,1,4)
                                plt.plot(Time,AzimuthAngleNormal)
                                plt.title('Rotor Azimuth Angle',fontsize=font_size)
                                plt.ylabel('Degrees',fontsize=font_size)
                                plt.xlabel('Time (s)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity',fontsize=font_size)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
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

                                plt.plot(Freq_mirror[0:cut],RotorPowerNormalFFT[0:cut])
                                plt.title('General quantities FFT\nPower',fontsize=font_size)
                                plt.ylabel('kW',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax= max(RotorPowerNormalFFT[y0:yf])
                                axes = plt.gca()
                                axes.set_xlim([xmin,xmax])
                                axes.set_ylim([ymin,ymax])
                                plt.tight_layout()

                                plt.subplot(3,1,2)
                                GeneratorSpeedNormalFFT = fft(GeneratorSpeedNormal)
                                GeneratorSpeedNormalFFT=np.abs(GeneratorSpeedNormalFFT)
                                GeneratorSpeedNormalFFT=GeneratorSpeedNormalFFT/(N/2)

                                plt.plot(Freq_mirror[0:cut],GeneratorSpeedNormalFFT[0:cut])
                                plt.title('Generator Speed',fontsize=font_size)
                                plt.ylabel('RPM',fontsize=font_size)
                                plt.tick_params(axis='x',labelbottom=False)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax= max(GeneratorSpeedNormalFFT[y0:yf])
                                axes = plt.gca()
                                axes.set_xlim([xmin,xmax])
                                axes.set_ylim([ymin,ymax])
                                plt.tight_layout()

                                plt.subplot(3,1,3)
                                RotorSpeedNormalFFT = fft(RotorSpeedNormal)
                                RotorSpeedNormalFFT=np.abs(RotorSpeedNormalFFT)
                                RotorSpeedNormalFFT=RotorSpeedNormalFFT/(N/2)

                                plt.plot(Freq_mirror[0:cut],RotorSpeedNormalFFT[0:cut])
                                plt.title('Rotor Speed',fontsize=font_size)
                                plt.ylabel('RPM',fontsize=font_size)
                                plt.tick_params(axis='y',labelsize = tick_size)
                                plt.xlabel('Frequency (Hz)\n\nWind Speed of '+str(v)+'m/s with '+str(t)+'% turbulence intensity',fontsize=font_size)
                                plt.box(on=None)
                                plt.grid(True)
                                ymax= max(RotorSpeedNormalFFT[y0:yf])
                                axes = plt.gca()
                                axes.set_xlim([xmin,xmax])
                                axes.set_ylim([ymin,ymax])
                                plt.tight_layout()

                                plt.savefig(output_data+'/QuantitiesFFT.png',dpi = 200)
