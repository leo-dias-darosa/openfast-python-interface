import os
import subprocess
import shutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import fast_nrel as fst

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
    
    if os.path.isdir(path_fast+turbinefast+' Power Curve - IEC61400.12 - Fast') == False:
        os.mkdir(path_fast+turbinefast+' Power Curve - IEC61400.12 - Fast')
    if os.path.isdir(path_fast+turbinefast+' Power Curve - IEC61400.12 - Fast/'+turbinefast+' - '+str(s)+'s of duration bins')==False:
        os.mkdir(path_fast+turbinefast+' Power Curve - IEC61400.12 - Fast/'+turbinefast+' - '+str(s)+'s of duration bins')

    new_path = path_fast+turbinefast+' Power Curve - IEC61400.12 - Fast/'+turbinefast+' - '+str(s)+'s of duration bins/'
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

    ## Generating array of wind accordingly to IEC61400-12
    wind_speed = np.arange(3.0,25.5,0.5)

    ## Parameters for wind generation and FAST simulation

    path_fast = parameters[2]
    path_modules = parameters[3]
    turbinefast=parameters[4]
    h = parameters[6]
    turb = parameters[7]
    s = parameters[8]
    from_to=parameters[10]

    path_modules=path_modules+'/'
    path_fast = path_fast+'/'

    n_1=from_to[0]
    n_2=from_to[1]
    
    ## Parameters for plotting Power Curve, Power coefficient and Scattered Plot
    for v in wind_speed:
        for t in turb:
            for n in range(n_1,n_2):
                sim_path = path_fast+turbinefast+' Power Curve - IEC61400.12 - Fast/'+turbinefast+' - '+str(s)+'s of duration bins/'
                out_file = sim_path+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'.out'
                out_file_noHeaderStr = out_file[0:len(out_file)-4]+"noHeader.out"

                if os.path.exists(out_file_noHeaderStr+'.csv')==False:

                    sim_path = path_fast+turbinefast+' Power Curve - IEC61400.12 - Fast/'+turbinefast+' - '+str(s)+'s of duration bins/'
                            
                    out_file_csv = out_file[0:len(out_file)-4]+"noHeader.csv"
                            
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

    ## Generating array of wind accordingly to IEC61400-12
    wind_speed = np.arange(3.0,25.5,0.5)

    ## Parameters for wind generation and FAST simulation

    path_fast = parameters[2]
    path_modules = parameters[3]
    turbinefast=parameters[4]
    h = parameters[6]
    turb = parameters[7]
    s = parameters[8]
    from_to=parameters[10]

    path_modules=path_modules+'/'
    path_fast = path_fast+'/'

    n_1=from_to[0]
    n_2=from_to[1]
    ## Getting elasto_dyn module file for turbine radius
    fast_input = open(path_fast+turbinefast).read().splitlines()
    turbinefast = turbinefast[0:len(turbinefast)-4]
    Elasto_line = fast_input[21].split()
    Elasto = Elasto_line[0]
    Elasto_dyn = ''
    for i in Elasto:
        if i == '/':
            Elasto_dyn = ''
        else:
            Elasto_dyn = Elasto_dyn+i
    Elasto_dyn = path_modules+Elasto_dyn[0:-1]

    ## Get turbine radius
    get_radius = open(Elasto_dyn).read().splitlines()
    radius_line = get_radius[46].split()
    radius = radius_line[0]
    ## Rotor swept area
    A = 3.1415*int(radius)**2
    
    ## Parameters for plotting Power Curve, Power coefficient and Scattered Plot
    power_mean_list=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    power_mean_final=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    power_max_list=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    power_min_list=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    power_deviation_list=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    cp_list =[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    Rated_speed_power_mean= []
    power_max_global = 0
    n_list=0

    for v in wind_speed:
        for t in turb:
            for n in range(n_1,n_2):
                sim_path = path_fast+turbinefast+' Power Curve - IEC61400.12 - Fast/'+turbinefast+' - '+str(s)+'s of duration bins/'
                out_file = sim_path+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'.out'
                out_file_noHeaderStr = out_file[0:len(out_file)-4]+"noHeader.out"

                if os.path.exists(out_file_noHeaderStr+'.csv')==False:

                    sim_path = path_fast+turbinefast+' Power Curve - IEC61400.12 - Fast/'+turbinefast+' - '+str(s)+'s of duration bins/'
                            
                    out_file_csv = out_file[0:len(out_file)-4]+"noHeader.csv"
                            
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

                ## Get values

                out_file_csv = out_file[0:len(out_file)-4]+"noHeader.csv"
                
                dataBinIndex =  pd.read_csv(out_file_csv)
                dataBin = pd.read_csv(out_file_csv,header=None)

                power_index = dataBinIndex.columns.get_loc("GenPwr")
                power=dataBin.iloc[2:,power_index]
                power = [float(x) for x in power]

                Blade1PitchAngleIndex = dataBinIndex.columns.get_loc("BldPitch1")
                Blade1PitchAngle = dataBin.iloc[2:,Blade1PitchAngleIndex]
                Blade1PitchAngle = [float(x) for x in Blade1PitchAngle]

                Blade2PitchAngleIndex = dataBinIndex.columns.get_loc("BldPitch2")
                Blade2PitchAngle = dataBin.iloc[2:,Blade2PitchAngleIndex]
                Blade2PitchAngle = [float(x) for x in Blade2PitchAngle]

                Blade3PitchAngleIndex = dataBinIndex.columns.get_loc("BldPitch3")
                Blade3PitchAngle = dataBin.iloc[2:,Blade3PitchAngleIndex]
                Blade3PitchAngle = [float(x) for x in Blade3PitchAngle]

                ## Getting Power

                power_mean = np.mean(power)
                power_max=np.max(power)
                power_min=np.min(power)
                power_deviation = np.std(power)

                power_mean_list[n_list].append(power_mean)
                power_mean_final[n_list].append(power_mean)
                power_max_list[n_list].append(power_max)
                power_min_list[n_list].append(power_min)
                power_deviation_list[n_list].append(round((power_deviation),2))

                if (np.mean(Blade1PitchAngle) or np.mean(Blade2PitchAngle) or np.mean(Blade3PitchAngle))>5 and ((np.mean(Blade1PitchAngle) or np.mean(Blade2PitchAngle) or np.mean(Blade3PitchAngle))<80):
                    Rated_speed_power_mean.append(power_mean)
                    if power_max > power_max_global:
                        power_max_global = power_max

                ## Getting CP

                Power_available = (0.5*1.225*A*(v**3))
                Cp = power_mean*1000/Power_available
                cp_list[n_list].append(Cp)
        n_list = n_list+1
                
        for i in range(len(power_mean_final)):
            power_mean_final[i]=np.mean(power_mean_final[i])
                       
        for i in range(len(cp_list)):
            cp_list[i]=np.mean(cp_list[i])

        turbulences_string=''
        for i in turb:
            if i==turb[-1] and len(turb)>1:
                turbulences_string = turbulences_string+'and '+str(i)
            elif len(turb==1):
                turbulences_string = turbulences_string+str(i)
            else:
                turbulences_string = turbulences_string+str(i)+', '
                       
        font_size = 20
        legend_size = 18
        tick_size = 16
        plot_line = 0.75
        fig, ax1= plt.subplots(sharex=True,frameon=False)
        fig.set_size_inches(14,8)
        power_mean_part = np.mean(Rated_speed_power_mean)/5
        power_max_part = power_max_global/5
        
        ax1.plot(wind_speed, power_mean_final, label='Power',linewidth=plot_line)
        ax1.set_title('Power Curve and CP',fontsize=font_size)
        ax1.set_xlabel('Wind speed (m/s)\n'+turbinefast+', turbulence intensity '+str(turb),fontsize=font_size)
        ax1.set_ylabel('Power (kW)',fontsize=font_size)
        ax1.set_xlim(0,25)
        ax1.set_ylim(bottom=0)
        ax1.legend(fontsize=legend_size,frameon=False,loc='center right')
        ax1.set_yticks(np.arange(0,6*power_mean_part,power_mean_part))
        ax1.tick_params(labelsize=tick_size)        
        ax1.set_frame_on(False)

        ax2 = ax1.twinx()
        ax2.plot(wind_speed,cp_list,'r',label = 'CP',linewidth=plot_line)
        ax2.set_xlabel('Wind speed (m/s)\n'+turbinefast+', turbulence intensity '+turbulences_string, fontsize=font_size)
        ax2.set_ylabel('CP',fontsize=font_size)
        ax2.set_xlim(3,25)
        ax2.set_ylim(0,0.55)
        ax2.legend(fontsize=legend_size,frameon=False,loc='center left')
        ax2.set_xticks(np.arange(5,26,5))
        ax2.set_yticks(np.arange(0,0.55,0.1))
        ax2.tick_params(labelsize=tick_size)        
        ax2.set_frame_on(True)
        fig.tight_layout()
        fig.savefig(sim_path+' Power Curve and CP.png',dpi = 200)
        plt.close('all')

        ##Plot Scatter Power ##########################################################################

        fig, ax3= plt.subplots()
        fig.set_size_inches(14,8)
        
        first_plot_mean = power_mean_list[0]
        first_plot_min = power_min_list[0]
        first_plot_max = power_max_list[0]
        first_plot_dev = power_deviation_list[0]
        dot_size = 12
        ax3.scatter(wind_speed[0],first_plot_mean[0],s=dot_size, c = 'grey',label = 'Mean')
        ax3.scatter(wind_speed[0],first_plot_min[0],s=dot_size, c = 'r',label = 'Min')       
        ax3.scatter(wind_speed[0],first_plot_max[0],s=dot_size, c = 'g',label = 'Max')    
        ax3.scatter(wind_speed[0],first_plot_dev[0],s=dot_size, c = 'b',label = 'Deviation')

        for l in range(1,len(power_mean_list)):
            index_plot_mean= power_mean_list[l]
            index_plot_min= power_min_list[l]
            index_plot_max= power_max_list[l]
            index_plot_dev= power_deviation_list[l]
            for i in range(1,len(index_plot_mean)):
                    ax3.scatter(wind_speed[l],index_plot_mean[i],s=dot_size, c = 'grey')
                    ax3.scatter(wind_speed[l],index_plot_min[i],s=dot_size, c = 'r')       
                    ax3.scatter(wind_speed[l],index_plot_max[i],s=dot_size, c = 'g')    
                    ax3.scatter(wind_speed[l],index_plot_dev[i],s=dot_size, c = 'b')

        ax3.set_title('Statistics',fontsize=font_size)
        ax3.set_xlabel('Wind speed (m/s)\n'+turbinefast+', turbulence intensity '+turbulences_string, fontsize=font_size)
        ax3.set_ylabel('Power (kW)',fontsize=font_size)
        ax3.set_xlim(3,25.1)
        ax3.set_ylim(-10,power_max_global+10)
        ax3.legend(fontsize=legend_size,frameon=False,loc = 'center right')
        ax3.set_xticks(np.arange(5,26,5))
        ax3.set_yticks(np.arange(0,6*power_max_part,power_max_part))
        ax3.tick_params(labelsize=tick_size)
        ax3.set_frame_on(True)        
        fig.tight_layout()
        fig.savefig(sim_path+' Scatter plot.png',dpi = 200)
        plt.close('all')