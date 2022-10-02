    # -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 14:57:27 2018

@author: Leonardo
"""

import subprocess
import os
import shutil
import matlab.engine

def collective(parameters):
    
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
    simulink_collective = parameters[11]
    n = parameters[13]
    
    fast_standard = open(path_fast+turbinefast).read().splitlines()
    turbinefast = turbinefast[0:len(turbinefast)-4]

    if os.path.isdir(path_fast+turbinefast+' Customized - Collective Pitch Controller') == False:
            os.mkdir(path_fast+turbinefast+' Customized - Collective Pitch Controller')
    if os.path.isdir(path_fast+turbinefast+' Customized - Collective Pitch Controller/Blade Mass Fault') == False:
            os.mkdir(path_fast+turbinefast+' Customized - Collective Pitch Controller/Blade Mass Fault')
    if os.path.isdir(path_fast+turbinefast+' Customized - Collective Pitch Controller/Blade Mass Fault/'+turbinefast+'-'+str(v)+'ms') == False:
            os.mkdir(path_fast+turbinefast+' Customized - Collective Pitch Controller/Blade Mass Fault/'+turbinefast+'-'+str(v)+'ms')
    if os.path.isdir(path_fast+turbinefast+' Customized - Collective Pitch Controller/Blade Mass Fault/'+turbinefast+'-'+str(v)+'ms/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'-'+str(e)+'BladeMassFault') == False:
            os.mkdir(path_fast+turbinefast+' Customized - Collective Pitch Controller/Blade Mass Fault/'+turbinefast+'-'+str(v)+'ms/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'-'+str(e)+'BladeMassFault')

    new_path = path_fast+turbinefast+' Customized - Collective Pitch Controller/Blade Mass Fault/'+turbinefast+'-'+str(v)+'ms/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'-'+str(e)+'BladeMassFault/'
              
    str_fast=new_path+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'-'+str(e)+'BladeMassFault.fst'
    txtfast=open(str_fast,'w')

    if os.path.isdir(new_path+'/Aerodata')==True:
        shutil.rmtree(new_path+'/Aerodata')
    if os.path.isdir(new_path+'/Airfoils')==True:
        shutil.rmtree(new_path+'/Airfoils')

    shutil.copytree(path_modules+'Aerodata',new_path+'/Aerodata')
    shutil.copytree(path_modules+'Airfoils',new_path+'/Airfoils')
        
    for linha in fast_standard:
        txtfast.write(linha+'\n')
    txtfast.close()
    
    insert_modules = open(str_fast).read().splitlines()           
    Elasto=''
    Inflow =''
    Aero=''
    Servo=''
    Hidro = ''
    Sub = ''
    Moor = ''
    Ice = ''
    Beam = ''
    Blade = ''
    Tower = ''
    Aero_blade = ''


    ## Get modules
    
    a = 0
    for i in insert_modules[21]:
        if a <2:
            if i == '"':
                a = a+1
            else:
                Elasto = Elasto + str(i)

    Elasto_dyn=''
    for i in Elasto:
        if i == '/':
            Elasto_dyn = ''
        else:
            Elasto_dyn = Elasto_dyn+i
    
    a = 0
    for i in insert_modules[25]:
        if a<2:
            if i =='"':
                a = a+1
            else:
                Inflow = Inflow + str(i)

    Inflow_wind=''
    for i in Inflow:
        if i == '/':
            Inflow_wind = ''
        else:
            Inflow_wind = Inflow_wind+i

    a=0
    for i in insert_modules[26]:
        if a<2:
            if i =='"':
                a = a+1
            else:
                Aero = Aero + str(i)

    Aero_dyn=''
    for i in Aero:
        if i == '/':
            Aero_dyn = ''
        else:
            Aero_dyn = Aero_dyn+i
    
    a=0
    for i in insert_modules[27]:
        if a<2:
            if i=='"':
                a = a+1
            else:
                Servo = Servo + str(i)

    Servo_dyn=''
    for i in Servo:
        if i == '/':
            Servo_dyn = ''
        else:
            Servo_dyn = Servo_dyn+i
    
    insert_elastocomponents = open(path_modules+Elasto_dyn).read().splitlines()
    a=0
    for i in insert_elastocomponents[87]:
        if a<2:
            if i=='"':
                a=a+1
            else:
                Blade = Blade + str(i)
                
    a = 0
    for i in insert_elastocomponents[109]:
        if a<2:
            if i=='"':
                a=a+1
            else:
                Tower= Tower + str(i)
                
    insert_aerocomponents = open(path_modules+Aero_dyn).read().splitlines()
    
    if len(insert_aerocomponents)>40:
        a = 0
        for i in insert_aerocomponents[40]:
            if a<2:
                if i=='"':
                    a=a+1
                else:
                    Aero_blade = Aero_blade + str(i)
    
    else:
        pass
    
    a = 0
    for i in insert_modules[22]:
        if a <2:
            if i == '"':
                a = a+1
            else:
                Beam = Beam + str(i)

    Beam_dyn=''
    for i in Beam:
        if i == '/':
            Beam_dyn = ''
        else:
            Beam_dyn = Beam_dyn+i
    
    a = 0
    for i in insert_modules[28]:
        if a <2:
            if i == '"':
                a = a+1
            else:
                Hidro = Hidro + str(i)

    Hidro_dyn=''
    for i in Hidro:
        if i == '/':
            Hidro_dyn = ''
        else:
            Hidro_dyn = Hidro_dyn+i

    a = 0
    for i in insert_modules[29]:
        if a <2:
            if i == '"':
                a = a+1
            else:
                Sub = Sub + str(i)
                
    Sub_dyn=''
    for i in Sub:
        if i == '/':
            Sub_dyn = ''
        else:
            Sub_dyn = Sub_dyn+i
                
    a = 0
    for i in insert_modules[30]:
        if a <2:
            if i == '"':
                a = a+1
            else:
                Moor = Moor + str(i)

    Moor_dyn=''
    for i in Moor:
        if i == '/':
            Moor_dyn = ''
        else:
            Moor_dyn = Moor_dyn+i
            
    a = 0
    for i in insert_modules[31]:
        if a <2:
            if i == '"':
                a = a+1
            else:
                Ice = Ice + str(i)

    Ice_dyn=''
    for i in Ice:
        if i == '/':
            Ice_dyn = ''
        else:
            Ice_dyn = Ice_dyn+i

    ## Create new_modules
            
    if os.path.exists(path_modules+Elasto_dyn) == True:
        Elasto_standard=open(path_modules+Elasto_dyn).read().splitlines()
        new_elasto = open(new_path+'Elasto.dat','w')
        for linha in Elasto_standard:
            new_elasto.write(linha+'\n')
        new_elasto.close()
        
    if os.path.exists(path_modules+Servo_dyn) == True:
        Servo_standard=open(path_modules+Servo_dyn).read().splitlines()
        new_servo = open(new_path+'Servo.dat','w')
        for linha in Servo_standard:
            new_servo.write(linha+'\n')
        new_servo.close()

    if os.path.exists(path_modules+Aero_dyn) == True:
        Aero_standard=open(path_modules+Aero_dyn).read().splitlines()
        new_aero = open(new_path+'Aero.dat','w')
        for linha in Aero_standard:
            new_aero.write(linha+'\n')
        new_aero.close()
        
    if os.path.exists(path_modules+Inflow_wind)== True:
        Inflow_standard=open(path_modules+Inflow_wind).read().splitlines()
        new_inflow = open(new_path+'Inflow.dat','w')
        for linha in Inflow_standard:
            new_inflow.write(linha+'\n')
        new_inflow.close()
           
    if os.path.exists(path_modules+Sub_dyn) == True:
        Sub_standard=open(path_modules+Sub_dyn).read().splitlines()
        new_sub = open(new_path+'Sub.dat','w')
        for linha in Sub_standard:
            new_sub.write(linha+'\n')
        new_sub.close()
        
    if os.path.exists(path_modules+Hidro_dyn) == True:
        Hidro_standard=open(path_modules+Hidro_dyn).read().splitlines()
        new_hidro = open(new_path+'Hidro.dat','w')
        for linha in Hidro_standard:
            new_hidro.write(linha+'\n')
        new_hidro.close()
 
    if os.path.exists(path_modules+Moor_dyn) == True:
        Moor_standard=open(path_modules+Moor_dyn).read().splitlines()
        new_moor = open(new_path+'Moor.dat','w')
        for linha in Moor_standard:
            new_moor.write(linha+'\n')
        new_moor.close()
        
    if os.path.exists(path_modules+Ice_dyn) == True:
        Ice_standard=open(path_modules+Ice_dyn).read().splitlines()
        new_ice = open(new_path+'Ice.dat','w')
        for linha in Ice_standard:
            new_ice.write(linha+'\n')
        new_ice.close()
    
    if os.path.exists(path_modules+Beam_dyn) == True:
        Beam_standard=open(path_modules+Beam_dyn).read().splitlines()
        new_beam = open(new_path+'Beam.dat','w')
        for linha in Beam_standard:
            new_beam.write(linha+'\n')
        new_beam.close()

    ## Inflow Wind ##
    fast_input = open(path_fast+turbinefast+'.fst').read().splitlines()
    wind_file=str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(n)+'.inp'

    ## Get wind

    wind_inflow= open(new_path+'Inflow.dat').read().splitlines()
    a=0
    wind =''
    for i in wind_inflow[21]:
        if a<2:
            if i != '"':
                wind = wind+i
            else:
                a= a+1
                
    ## Get Wind name only

    wind2 = ''
    for i in wind:
        if i =='/':
            wind2=''
        else:
            wind2=wind2+i

    ## Modify path
    a=0
    for i in wind:
        if i == '/':
            a = 0
        else:
            a = a+1
    path_wind = wind[0:(len(wind)-a)]

    wind_inflow= open(new_path+'Inflow.dat').read().splitlines()
    wind_inflow[4]='          4   WindType       - switch for wind file type (1=steady; 2=uniform; 3=binary TurbSim FF; 4=binary Bladed-style FF; 5=HAWC format; 6=User defined)'
    wind_inflow[21]= '"'+path_modules+path_wind+wind_file[0:len(wind_file)-4]+'"    FilenameRoot   - Rootname of the full-field wind file to use (.wnd, .sum)'
    open(new_path+'Inflow.dat','w').write('\n'.join(wind_inflow))  

    Blade_fault = Blade[0:len(Blade)-4]
    Blade_fault = Blade_fault+str(e)+'m.dat'
    ## Elasto_Dyn ##
    inserte = open(new_path+'Elasto.dat').read().splitlines()
    inserte[5]='    %f  DT          - Integration time step (s)'%((1/frequency)/10)
    inserte[87] = '"'+path_modules+Blade_fault+'"    BldFile(1)  - Name of file containing properties for blade 1 (quoted string)'
    inserte[88]= '"'+path_modules+Blade+'"     BldFile(2)  - Name of file containing properties for blade 1 (quoted string)'
    inserte[89]= '"'+path_modules+Blade+'"     BldFile(3)  - Name of file containing properties for blade 1 (quoted string)'
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
        if any("RootMyb1" in l for l in lines)==False:
            file.write('"RootMyb1"\n')                      ## Blade root flapwise bending moment (1)
        if any("RootMyb2" in l for l in lines)==False:
            file.write('"RootMyb2"\n')                      ## Blade root flapwise bending moment (2)
        if any("RootMyb3" in l for l in lines)==False:
            file.write('"RootMyb3"\n')                      ## Blade root flapwise bending moment (3)
        if any("RootMxb1" in l for l in lines)==False:
            file.write('"RootMxb1"\n')                      ## Blade root edgewise bending moment (1)
        if any("RootMxb2" in l for l in lines)==False:
            file.write('"RootMxb2"\n')                      ## Blade root edgewise bending moment (2)
        if any("RootMxb3" in l for l in lines)==False:
            file.write('"RootMxb3"\n')                      ## Blade root edgewise bending moment (3)
        if any("LSSTipMys" in l for l in lines)==False:
            file.write('"LSSTipMys"\n')                     ## Rotor Tilt
        if any("LssTipMzs" in l for l in lines)==False:
            file.write('"LssTipMzs"\n')                     ## Rotor Yaw
        if any("LSShftMxa" in l for l in lines)==False:
            file.write('"LSShftMxa"\n')                     ## Rotor Torque
        if any("TwrBsMyt" in l for l in lines)==False:
            file.write('"TwrBsMyt"\n')                     ## Tower base normal moment
        if any("TwrBsMxt" in l for l in lines)==False:
            file.write('"TwrBsMxt"\n')                     ## Tower base lateral moment
        if any("RootMzc1" in l for l in lines)==False:
            file.write('"RootMzc1"\n')                      ## Pitch Actuation Loads (1)
        if any("RootMzc2" in l for l in lines)==False:
            file.write('"RootMzc2"\n')                      ## Pitch Actuation Loads (2)
        if any("RootMzc3" in l for l in lines)==False:
            file.write('"RootMzc3"\n')                      ## Pitch Actuation Loads (3)
        if any("Spn1MLzb1" in l for l in lines)==False:
            file.write('"Spn1MLzb1"\n')                     ## Blade pitching moment at span location (1)
        if any("Spn1MLzb2" in l for l in lines)==False:
            file.write('"Spn1MLzb2"\n')                     ## Blade pitching moment at span location (2)
        if any("Spn1MLzb3" in l for l in lines)==False:
            file.write('"Spn1MLzb3"\n')                     ## Blade pitching moment at span location (3)
        if any("YawBrTAxp" in l for l in lines)==False:
            file.write('"YawBrTAxp"\n')                     ## Tower-top acceleration normal
        if any("YawBrTAyp" in l for l in lines)==False:
            file.write('"YawBrTAyp"\n')                     ## Tower-top acceleration lateral
        if any("TwHt1MLyt" in l for l in lines)==False:
            file.write('"TwHt1MLyt"\n')                     ## Tower normal moment at span location 
        if any("TwHt1MLxt" in l for l in lines)==False:
            file.write('"TwHt1MLxt"\n')                     ## Tower lateral moment at span location 
        if any("YawBrMyp" in l for l in lines)==False:
            file.write('"YawBrMyp"\n')                      ## Tower top normal moment 
        if any("YawBrMxp" in l for l in lines)==False:
            file.write('"YawBrMxp"\n')                      ## Tower top lateral moment
        if any("TwrBsMzt" in l for l in lines)==False:
            file.write('"TwrBsMzt"\n')                      ## Tower Torque
        if any("RotPwr" in l for l in lines)==False:
            file.write('"RotPwr"\n')                        ## Generator Power
        if any("GenSpeed" in l for l in lines)==False:
            file.write('"GenSpeed"\n')                      ## Generator Speed
        if any("RotSpeed " in l for l in lines)==False:
            file.write('"RotSpeed "\n')                     ## Rotor Speed
        if any("Azimuth " in l for l in lines)==False:
            file.write('"Azimuth "\n')                      ## Azimuth Angle 
        if any("PtchPMzc1" in l for l in lines)==False:
            file.write('"PtchPMzc1"\n')                     ## Blade pitch angle (1)
        if any("PtchPMzc2" in l for l in lines)==False:
            file.write('"PtchPMzc2"\n')                     ## Blade pitch angle (2)
        if any("PtchPMzc3" in l for l in lines)==False:
            file.write('"PtchPMzc3"\n')                     ## Blade pitch angle (3)
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
        if any("GenTq" in l for l in lines)==False:
            file.write('"GenTq"\n')                      ## Generator torque
        if any("GenPwr" in l for l in lines)==False:
            file.write('"GenPwr"\n')                      ## Generator Power            
        file.write('END of input file (the word "END" must appear in the first 3 columns of this last OutList line)\n')
        file.write('---------------------------------------------------------------------------------------')
    
    ## .fst ##                      
    insertmod=open(str_fast).read().splitlines()
    insertmod[21]='"'+new_path+'Elasto.dat"    EDFile          - Name of file containing ElastoDyn input parameters (quoted string)'
    insertmod[22]='"'+new_path+'Beam.dat"    BDBldFile(1)    - Name of file containing BeamDyn input parameters for blade 1 (quoted string)'
    insertmod[23]='"'+new_path+'Beam.dat"    BDBldFile(2)    - Name of file containing BeamDyn input parameters for blade 2 (quoted string)'
    insertmod[24]='"'+new_path+'Beam.dat"    BDBldFile(3)    - Name of file containing BeamDyn input parameters for blade 3 (quoted string)'
    insertmod[25]='"'+new_path+'Inflow.dat"    InflowFile      - Name of file containing inflow wind input parameters (quoted string)'
    insertmod[26]='"'+new_path+'Aero.dat"    AeroFile        - Name of file containing aerodynamic input parameters (quoted string)'
    insertmod[27]='"'+new_path+'Servo.dat"    ServoFile       - Name of file containing control and electrical-drive input parameters (quoted string)'
    insertmod[28]='"'+new_path+'Hidro.dat"    HydroFile       - Name of file containing hydrodynamic input parameters (quoted string)'
    insertmod[29]='"'+new_path+'Sub.dat"     SubFile         - Name of file containing sub-structural input parameters (quoted string)'
    insertmod[30]='"'+new_path+'Moor.dat"      MooringFile     - Name of file containing mooring system input parameters (quoted string)'
    insertmod[31]='"'+new_path+'Ice.dat"      IceFile         - Name of file containing ice input parameters (quoted string)'
    insertmod[36]='   %f    DT_Out          - Time step for tabular output (s) (or "default")'%(1/frequency)
    insertmod[5]='        %i   TMax            - Total run time (s)'%(s)
    insertmod[6]='   %f   DT              - Recommended module time step (s)'%((1/frequency)/10)
    open(str_fast,'w').write('\n'.join(insertmod))
     
    ## Aero_Dyn
    if len(insert_aerocomponents) > 40:
        insert_aerocomponents[6]='          1   AFAeroMod          - Type of blade airfoil aerodynamics model (switch) {1=steady model, 2=Beddoes-Leishman unsteady model}'
        insert_aerocomponents[16]='          1   SkewMod            - Type of skewed-wake correction model (switch) {1=uncoupled, 2=Pitt/Peters, 3=coupled} [used only when WakeMod=1]'
        insert_aerocomponents[40]='"'+path_modules+Aero_blade+'"    ADBlFile(1)        - Name of file containing distributed aerodynamic properties for Blade #1 (-))'
        insert_aerocomponents[41]='"'+path_modules+Aero_blade+'"    ADBlFile(2)        - Name of file containing distributed aerodynamic properties for Blade #2 (-))'
        insert_aerocomponents[42]='"'+path_modules+Aero_blade+'"    ADBlFile(3)        - Name of file containing distributed aerodynamic properties for Blade #3 (-))'
        
        open(new_path+'Aero.dat','w').write('\n'.join(insert_aerocomponents))
        insert_aerocomponents = open(new_path+'Aero.dat').read().splitlines()
        insert_aerocomponents[14]='   %f   DTAero       - Time interval for aerodynamic calculations (sec)'%((1/frequency)/10)
        open(new_path+'Aero.dat','w').write('\n'.join(insert_aerocomponents))
        
    else:
        insert_aerocomponents = open(new_path+'Aero.dat').read().splitlines()
        insert_aerocomponents[14]='   %f   DTAero       - Time interval for aerodynamic calculations (sec)'%((1/frequency)/10)
        open(new_path+'Aero.dat','w').write('\n'.join(insert_aerocomponents))
    
    pitch = open(path_fast+'pitch.ipt').read().splitlines()
    pitcht = open(new_path+'/pitch.ipt','w')
                
    for linha in pitch:
        pitcht.write(linha+'\n')
    pitcht.close()
    
    # Run Fast
    
    eng = matlab.engine.start_matlab()
    eng.workspace['path_from_python'] = path_fast
    eng.workspace['turbine_from_python'] = str_fast
    eng.workspace['simulink_from_python'] = simulink_collective
    eng.workspace['Time_from_python'] = str(s)
    eng.fast_nrel(nargout=0)

############################################################################################################################################################################################
############################################################################################################################################################################################

def IPC(parameters,IEC6140013=False):
    
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
    simulink_IPC = parameters[12]
    n = parameters[13]
    
    fast_standard = open(path_fast+turbinefast).read().splitlines()
    turbinefast = turbinefast[0:len(turbinefast)-4]

    if os.path.isdir(path_fast+turbinefast+' Customized - Collective Pitch Controller - Blade mass imbalance') == False:
            os.mkdir(path_fast+turbinefast+' Customized - Collective Pitch Controller - Blade mass imbalance')
    if os.path.isdir(path_fast+turbinefast+' Customized - Collective Pitch Controller - Blade mass imbalance/'+turbinefast+'-'+str(v)+'ms') == False:
            os.mkdir(path_fast+turbinefast+' Customized - Collective Pitch Controller - Blade mass imbalance/'+turbinefast+'-'+str(v)+'ms')
    if os.path.isdir(path_fast+turbinefast+' Customized - Collective Pitch Controller - Blade mass imbalance/'+turbinefast+'-'+str(v)+'ms/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)) == False:
            os.mkdir(path_fast+turbinefast+' Customized - Collective Pitch Controller - Blade mass imbalance/'+turbinefast+'-'+str(v)+'ms/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n))
   
    new_path = path_fast+turbinefast+' Customized - Collective Pitch Controller - Blade mass imbalance/'+turbinefast+'-'+str(v)+'ms/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'/'
              
    str_fast=new_path+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'.fst'
    txtfast=open(str_fast,'w')

    if os.path.isdir(new_path+'/Aerodata')==True:
        shutil.rmtree(new_path+'/Aerodata')
    if os.path.isdir(new_path+'/Airfoils')==True:
        shutil.rmtree(new_path+'/Airfoils')

    shutil.copytree(path_modules+'Aerodata',new_path+'/Aerodata')
    shutil.copytree(path_modules+'Airfoils',new_path+'/Airfoils')
        
    for linha in fast_standard:
        txtfast.write(linha+'\n')
    txtfast.close()
    
    insert_modules = open(str_fast).read().splitlines()           
    Elasto=''
    Inflow =''
    Aero=''
    Servo=''
    Hidro = ''
    Sub = ''
    Moor = ''
    Ice = ''
    Beam = ''
    Blade = ''
    Tower = ''
    Aero_blade = ''


    ## Get modules
    
    a = 0
    for i in insert_modules[21]:
        if a <2:
            if i == '"':
                a = a+1
            else:
                Elasto = Elasto + str(i)

    Elasto_dyn=''
    for i in Elasto:
        if i == '/':
            Elasto_dyn = ''
        else:
            Elasto_dyn = Elasto_dyn+i
    
    a = 0
    for i in insert_modules[25]:
        if a<2:
            if i =='"':
                a = a+1
            else:
                Inflow = Inflow + str(i)

    Inflow_wind=''
    for i in Inflow:
        if i == '/':
            Inflow_wind = ''
        else:
            Inflow_wind = Inflow_wind+i

    a=0
    for i in insert_modules[26]:
        if a<2:
            if i =='"':
                a = a+1
            else:
                Aero = Aero + str(i)

    Aero_dyn=''
    for i in Aero:
        if i == '/':
            Aero_dyn = ''
        else:
            Aero_dyn = Aero_dyn+i
    
    a=0
    for i in insert_modules[27]:
        if a<2:
            if i=='"':
                a = a+1
            else:
                Servo = Servo + str(i)

    Servo_dyn=''
    for i in Servo:
        if i == '/':
            Servo_dyn = ''
        else:
            Servo_dyn = Servo_dyn+i
    
    insert_elastocomponents = open(path_modules+Elasto_dyn).read().splitlines()
    a=0
    for i in insert_elastocomponents[87]:
        if a<2:
            if i=='"':
                a=a+1
            else:
                Blade = Blade + str(i)
                
    a = 0
    for i in insert_elastocomponents[109]:
        if a<2:
            if i=='"':
                a=a+1
            else:
                Tower= Tower + str(i)
                
    insert_aerocomponents = open(path_modules+Aero_dyn).read().splitlines()
    
    if len(insert_aerocomponents)>40:
        a = 0
        for i in insert_aerocomponents[40]:
            if a<2:
                if i=='"':
                    a=a+1
                else:
                    Aero_blade = Aero_blade + str(i)
    
    else:
        pass
    
    a = 0
    for i in insert_modules[22]:
        if a <2:
            if i == '"':
                a = a+1
            else:
                Beam = Beam + str(i)

    Beam_dyn=''
    for i in Beam:
        if i == '/':
            Beam_dyn = ''
        else:
            Beam_dyn = Beam_dyn+i
    
    a = 0
    for i in insert_modules[28]:
        if a <2:
            if i == '"':
                a = a+1
            else:
                Hidro = Hidro + str(i)

    Hidro_dyn=''
    for i in Hidro:
        if i == '/':
            Hidro_dyn = ''
        else:
            Hidro_dyn = Hidro_dyn+i

    a = 0
    for i in insert_modules[29]:
        if a <2:
            if i == '"':
                a = a+1
            else:
                Sub = Sub + str(i)
                
    Sub_dyn=''
    for i in Sub:
        if i == '/':
            Sub_dyn = ''
        else:
            Sub_dyn = Sub_dyn+i
                
    a = 0
    for i in insert_modules[30]:
        if a <2:
            if i == '"':
                a = a+1
            else:
                Moor = Moor + str(i)

    Moor_dyn=''
    for i in Moor:
        if i == '/':
            Moor_dyn = ''
        else:
            Moor_dyn = Moor_dyn+i
            
    a = 0
    for i in insert_modules[31]:
        if a <2:
            if i == '"':
                a = a+1
            else:
                Ice = Ice + str(i)

    Ice_dyn=''
    for i in Ice:
        if i == '/':
            Ice_dyn = ''
        else:
            Ice_dyn = Ice_dyn+i

    ## Create new_modules
            
    if os.path.exists(path_modules+Elasto_dyn) == True:
        Elasto_standard=open(path_modules+Elasto_dyn).read().splitlines()
        new_elasto = open(new_path+'Elasto.dat','w')
        for linha in Elasto_standard:
            new_elasto.write(linha+'\n')
        new_elasto.close()
        
    if os.path.exists(path_modules+Servo_dyn) == True:
        Servo_standard=open(path_modules+Servo_dyn).read().splitlines()
        new_servo = open(new_path+'Servo.dat','w')
        for linha in Servo_standard:
            new_servo.write(linha+'\n')
        new_servo.close()

    if os.path.exists(path_modules+Aero_dyn) == True:
        Aero_standard=open(path_modules+Aero_dyn).read().splitlines()
        new_aero = open(new_path+'Aero.dat','w')
        for linha in Aero_standard:
            new_aero.write(linha+'\n')
        new_aero.close()
        
    if os.path.exists(path_modules+Inflow_wind)== True:
        Inflow_standard=open(path_modules+Inflow_wind).read().splitlines()
        new_inflow = open(new_path+'Inflow.dat','w')
        for linha in Inflow_standard:
            new_inflow.write(linha+'\n')
        new_inflow.close()
           
    if os.path.exists(path_modules+Sub_dyn) == True:
        Sub_standard=open(path_modules+Sub_dyn).read().splitlines()
        new_sub = open(new_path+'Sub.dat','w')
        for linha in Sub_standard:
            new_sub.write(linha+'\n')
        new_sub.close()
        
    if os.path.exists(path_modules+Hidro_dyn) == True:
        Hidro_standard=open(path_modules+Hidro_dyn).read().splitlines()
        new_hidro = open(new_path+'Hidro.dat','w')
        for linha in Hidro_standard:
            new_hidro.write(linha+'\n')
        new_hidro.close()
 
    if os.path.exists(path_modules+Moor_dyn) == True:
        Moor_standard=open(path_modules+Moor_dyn).read().splitlines()
        new_moor = open(new_path+'Moor.dat','w')
        for linha in Moor_standard:
            new_moor.write(linha+'\n')
        new_moor.close()
        
    if os.path.exists(path_modules+Ice_dyn) == True:
        Ice_standard=open(path_modules+Ice_dyn).read().splitlines()
        new_ice = open(new_path+'Ice.dat','w')
        for linha in Ice_standard:
            new_ice.write(linha+'\n')
        new_ice.close()
    
    if os.path.exists(path_modules+Beam_dyn) == True:
        Beam_standard=open(path_modules+Beam_dyn).read().splitlines()
        new_beam = open(new_path+'Beam.dat','w')
        for linha in Beam_standard:
            new_beam.write(linha+'\n')
        new_beam.close()

    ## Inflow Wind ##
    fast_input = open(path_fast+turbinefast+'.fst').read().splitlines()
    wind_file=str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(n)+'.inp'

    ## Get wind

    wind_inflow= open(new_path+'Inflow.dat').read().splitlines()
    a=0
    wind =''
    for i in wind_inflow[21]:
        if a<2:
            if i != '"':
                wind = wind+i
            else:
                a= a+1
                
    ## Get Wind name only

    wind2 = ''
    for i in wind:
        if i =='/':
            wind2=''
        else:
            wind2=wind2+i

    ## Modify path
    a=0
    for i in wind:
        if i == '/':
            a = 0
        else:
            a = a+1
    path_wind = wind[0:(len(wind)-a)]

    wind_inflow= open(new_path+'Inflow.dat').read().splitlines()
    wind_inflow[4]='          4   WindType       - switch for wind file type (1=steady; 2=uniform; 3=binary TurbSim FF; 4=binary Bladed-style FF; 5=HAWC format; 6=User defined)'
    wind_inflow[21]= '"'+path_modules+path_wind+wind_file[0:len(wind_file)-4]+'"    FilenameRoot   - Rootname of the full-field wind file to use (.wnd, .sum)'
    open(new_path+'Inflow.dat','w').write('\n'.join(wind_inflow))  

    ## Elasto_Dyn ##
    inserte = open(new_path+'Elasto.dat').read().splitlines()
    inserte[5]='    %f  DT          - Integration time step (s)'%((1/frequency)/10)
    inserte[87] = '"'+path_modules+Blade+'"    BldFile(1)  - Name of file containing properties for blade 1 (quoted string)'
    inserte[88]= '"'+path_modules+Blade+'"     BldFile(2)  - Name of file containing properties for blade 1 (quoted string)'
    inserte[89]= '"'+path_modules+Blade+'"     BldFile(3)  - Name of file containing properties for blade 1 (quoted string)'
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
        if any("RootMyb1" in l for l in lines)==False:
            file.write('"RootMyb1"\n')                      ## Blade root flapwise bending moment (1)
        if any("RootMyb2" in l for l in lines)==False:
            file.write('"RootMyb2"\n')                      ## Blade root flapwise bending moment (2)
        if any("RootMyb3" in l for l in lines)==False:
            file.write('"RootMyb3"\n')                      ## Blade root flapwise bending moment (3)
        if any("RootMxb1" in l for l in lines)==False:
            file.write('"RootMxb1"\n')                      ## Blade root edgewise bending moment (1)
        if any("RootMxb2" in l for l in lines)==False:
            file.write('"RootMxb2"\n')                      ## Blade root edgewise bending moment (2)
        if any("RootMxb3" in l for l in lines)==False:
            file.write('"RootMxb3"\n')                      ## Blade root edgewise bending moment (3)
        if any("LSSTipMys" in l for l in lines)==False:
            file.write('"LSSTipMys"\n')                     ## Rotor Tilt
        if any("LssTipMzs" in l for l in lines)==False:
            file.write('"LssTipMzs"\n')                     ## Rotor Yaw
        if any("LSShftMxa" in l for l in lines)==False:
            file.write('"LSShftMxa"\n')                     ## Rotor Torque
        if any("TwrBsMyt" in l for l in lines)==False:
            file.write('"TwrBsMyt"\n')                     ## Tower base normal moment
        if any("TwrBsMxt" in l for l in lines)==False:
            file.write('"TwrBsMxt"\n')                     ## Tower base lateral moment
        if any("RootMzc1" in l for l in lines)==False:
            file.write('"RootMzc1"\n')                      ## Pitch Actuation Loads (1)
        if any("RootMzc2" in l for l in lines)==False:
            file.write('"RootMzc2"\n')                      ## Pitch Actuation Loads (2)
        if any("RootMzc3" in l for l in lines)==False:
            file.write('"RootMzc3"\n')                      ## Pitch Actuation Loads (3)
        if any("Spn1MLzb1" in l for l in lines)==False:
            file.write('"Spn1MLzb1"\n')                     ## Blade pitching moment at span location (1)
        if any("Spn1MLzb2" in l for l in lines)==False:
            file.write('"Spn1MLzb2"\n')                     ## Blade pitching moment at span location (2)
        if any("Spn1MLzb3" in l for l in lines)==False:
            file.write('"Spn1MLzb3"\n')                     ## Blade pitching moment at span location (3)
        if any("YawBrTAxp" in l for l in lines)==False:
            file.write('"YawBrTAxp"\n')                     ## Tower-top acceleration normal
        if any("YawBrTAyp" in l for l in lines)==False:
            file.write('"YawBrTAyp"\n')                     ## Tower-top acceleration lateral
        if any("TwHt1MLyt" in l for l in lines)==False:
            file.write('"TwHt1MLyt"\n')                     ## Tower normal moment at span location 
        if any("TwHt1MLxt" in l for l in lines)==False:
            file.write('"TwHt1MLxt"\n')                     ## Tower lateral moment at span location 
        if any("YawBrMyp" in l for l in lines)==False:
            file.write('"YawBrMyp"\n')                      ## Tower top normal moment 
        if any("YawBrMxp" in l for l in lines)==False:
            file.write('"YawBrMxp"\n')                      ## Tower top lateral moment
        if any("TwrBsMzt" in l for l in lines)==False:
            file.write('"TwrBsMzt"\n')                      ## Tower Torque
        if any("RotPwr" in l for l in lines)==False:
            file.write('"RotPwr"\n')                        ## Generator Power
        if any("GenSpeed" in l for l in lines)==False:
            file.write('"GenSpeed"\n')                      ## Generator Speed
        if any("RotSpeed " in l for l in lines)==False:
            file.write('"RotSpeed "\n')                     ## Rotor Speed
        if any("Azimuth " in l for l in lines)==False:
            file.write('"Azimuth "\n')                      ## Azimuth Angle 
        if any("PtchPMzc1" in l for l in lines)==False:
            file.write('"PtchPMzc1"\n')                     ## Blade pitch angle (1)
        if any("PtchPMzc2" in l for l in lines)==False:
            file.write('"PtchPMzc2"\n')                     ## Blade pitch angle (2)
        if any("PtchPMzc3" in l for l in lines)==False:
            file.write('"PtchPMzc3"\n')                     ## Blade pitch angle (3)
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
        if any("GenTq" in l for l in lines)==False:
            file.write('"GenTq"\n')                      ## Generator torque
        if any("GenPwr" in l for l in lines)==False:
            file.write('"GenPwr"\n')                      ## Generator Power            
        file.write('END of input file (the word "END" must appear in the first 3 columns of this last OutList line)\n')
        file.write('---------------------------------------------------------------------------------------')
    
    ## .fst ##                      
    insertmod=open(str_fast).read().splitlines()
    insertmod[21]='"'+new_path+'Elasto.dat"    EDFile          - Name of file containing ElastoDyn input parameters (quoted string)'
    insertmod[22]='"'+new_path+'Beam.dat"    BDBldFile(1)    - Name of file containing BeamDyn input parameters for blade 1 (quoted string)'
    insertmod[23]='"'+new_path+'Beam.dat"    BDBldFile(2)    - Name of file containing BeamDyn input parameters for blade 2 (quoted string)'
    insertmod[24]='"'+new_path+'Beam.dat"    BDBldFile(3)    - Name of file containing BeamDyn input parameters for blade 3 (quoted string)'
    insertmod[25]='"'+new_path+'Inflow.dat"    InflowFile      - Name of file containing inflow wind input parameters (quoted string)'
    insertmod[26]='"'+new_path+'Aero.dat"    AeroFile        - Name of file containing aerodynamic input parameters (quoted string)'
    insertmod[27]='"'+new_path+'Servo.dat"    ServoFile       - Name of file containing control and electrical-drive input parameters (quoted string)'
    insertmod[28]='"'+new_path+'Hidro.dat"    HydroFile       - Name of file containing hydrodynamic input parameters (quoted string)'
    insertmod[29]='"'+new_path+'Sub.dat"     SubFile         - Name of file containing sub-structural input parameters (quoted string)'
    insertmod[30]='"'+new_path+'Moor.dat"      MooringFile     - Name of file containing mooring system input parameters (quoted string)'
    insertmod[31]='"'+new_path+'Ice.dat"      IceFile         - Name of file containing ice input parameters (quoted string)'
    insertmod[36]='   %f    DT_Out          - Time step for tabular output (s) (or "default")'%(1/frequency)
    insertmod[5]='        %i   TMax            - Total run time (s)'%(s)
    insertmod[6]='   %f   DT              - Recommended module time step (s)'%((1/frequency)/10)
    open(str_fast,'w').write('\n'.join(insertmod))
     
    ## Aero_Dyn
    if len(insert_aerocomponents) > 40:
        insert_aerocomponents[6]='          1   AFAeroMod          - Type of blade airfoil aerodynamics model (switch) {1=steady model, 2=Beddoes-Leishman unsteady model}'
        insert_aerocomponents[16]='          1   SkewMod            - Type of skewed-wake correction model (switch) {1=uncoupled, 2=Pitt/Peters, 3=coupled} [used only when WakeMod=1]'
        insert_aerocomponents[40]='"'+path_modules+Aero_blade+'"    ADBlFile(1)        - Name of file containing distributed aerodynamic properties for Blade #1 (-))'
        insert_aerocomponents[41]='"'+path_modules+Aero_blade+'"    ADBlFile(2)        - Name of file containing distributed aerodynamic properties for Blade #2 (-))'
        insert_aerocomponents[42]='"'+path_modules+Aero_blade+'"    ADBlFile(3)        - Name of file containing distributed aerodynamic properties for Blade #3 (-))'
        
        open(new_path+'Aero.dat','w').write('\n'.join(insert_aerocomponents))
        insert_aerocomponents = open(new_path+'Aero.dat').read().splitlines()
        insert_aerocomponents[14]='   %f   DTAero       - Time interval for aerodynamic calculations (sec)'%((1/frequency)/10)
        open(new_path+'Aero.dat','w').write('\n'.join(insert_aerocomponents))
        
    else:
        insert_aerocomponents = open(new_path+'Aero.dat').read().splitlines()
        insert_aerocomponents[14]='   %f   DTAero       - Time interval for aerodynamic calculations (sec)'%((1/frequency)/10)
        open(new_path+'Aero.dat','w').write('\n'.join(insert_aerocomponents))
    
    pitch = open(path_fast+'pitch.ipt').read().splitlines()
    pitcht = open(new_path+'/pitch.ipt','w')
                
    for linha in pitch:
        pitcht.write(linha+'\n')
    pitcht.close()    
    # Run Fast
    
    eng = matlab.engine.start_matlab()
    eng.workspace['path_from_python'] = path_fast
    eng.workspace['turbine_from_python'] = str_fast
    eng.workspace['simulink_from_python'] = simulink_IPC
    eng.workspace['Time_from_python'] = str(s)
    eng.fast_nrel(nargout=0)
