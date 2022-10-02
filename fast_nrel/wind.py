import subprocess
import os
from random import randrange, uniform

def steady(parameters):
    
    path_fast = parameters[2]
    path_modules = parameters[3]
    turbinefast=parameters[4]
    v = parameters[5]
    h = parameters[6]
    t = parameters[7]
    s = parameters[8]
    n=parameters[9]
    frequency = parameters[10]

    ## Parameters for wind generation and FAST simulation

    path_modules=path_modules+'/'
    path_fast = path_fast+'/'

    v = float(v)
    fast_input = open(path_fast+turbinefast).read().splitlines()
    inflow=''

    a=0
    for i in fast_input[25]:
        if a<2:
            if i != '"':
                inflow = inflow+i
            else:
                a= a+1

    v = str(v)
    h = str(h)
    wind_inflow= open(path_fast+inflow).read().splitlines()
    wind_inflow[4]='          1   WindType       - switch for wind file type (1=steady; 2=uniform; 3=binary TurbSim FF; 4=binary Bladed-style FF; 5=HAWC format; 6=User defined)'
    wind_inflow[12]='         %s  HWindSpeed     - Horizontal windspeed                            (m/s)'%(v)
    wind_inflow[13]='         %s   RefHt          - Reference height for horizontal wind speed      (m)'%(h)
    open(path_fast+inflow,'w').write('\n'.join(wind_inflow))
    
def uniform_wind_file(parameters):

    path_modules = parameters[0]
    path_fast = parameters[1]
    turbinefast = parameters[2]
    path_turbsim = parameters[3]
    turbsim = parameters[4]
    v = parameters[5]
    h = parameters[6]
    t = parameters[7]
    s = parameters[8]
    fast_frequency = parameters[9]
    r = parameters[12]
    
    fast_input = open(path_fast+turbinefast).read().splitlines()
    inflow=''
    path_wind=''
    wind_file=str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'.inp'

    ## Read inflow wind module
    a=0
    for i in fast_input[25]:
        if a<2:
            if i != '"':
                inflow = inflow+i
            else:
                a= a+1
    
    ## Modify inflow wind
                
    wind_inflow= open(path_fast+inflow).read().splitlines()
    wind_inflow[4]='          2   WindType       - switch for wind file type (1=steady; 2=uniform; 3=binary TurbSim FF; 4=binary Bladed-style FF; 5=HAWC format; 6=User defined)'
    open(path_fast+inflow,'w').write('\n'.join(wind_inflow))

    ## Get wind

    a=0
    wind =''
    for i in wind_inflow[15]:
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
    wind2 = wind2[0:len(wind2)-4]
    
    ## Create new wind file
    
    if os.path.exists(path_modules+path_wind+wind_file)==False:
        new_wind = open(path_modules+path_wind+wind_file, 'w')
            
        txtwind = open(path_modules+path_wind+wind2+'.inp').read().splitlines()
        for linha in txtwind:
            new_wind.write(linha+'\n')
        new_wind.close()

        
        ## Modificar velocidade do vento ## 
        insert = open(path_modules+path_wind+wind_file).read().splitlines()
        insert[20]='%i                 AnalysisTime    - Length of analysis time series [seconds] (program will add time if necessary: AnalysisTime = MAX(AnalysisTime, UsableTime+GridWidth/MeanHHWS) )'%(s)
        insert[21]='%i                 UsableTime      - Usable length of output time series [seconds] (program will add GridWidth/MeanHHWS seconds)'%(s)    
        insert[23]='%i                GridHeight      - Grid height [m]'%(r)
        insert[24]='%f                GridWidth       - Grid width [m] (should be >= 2*(RotorRadius+ShaftLength))'%(r)
        insert[31]='"%f"                 IECturbc        - IEC turbulence characteristic ("A", "B", "C" or the turbulence intensity in percent) ("KHTEST" option with NWTCUP model, not used for other models)'%(t)
        insert[35]='%i                  RefHt           - Height of the reference wind speed [m]'%(h)
        insert[36]='%i                  URef            - Mean (total) wind speed at the reference height [m/s] (or "default" for JET wind profile)'%(v)
        open(path_modules+path_wind+wind_file, 'w').write('\n'.join(insert))
        subprocess.run([path_turbsim+turbsim, path_modules+path_wind+new_wind])

        ## Inflow Wind
        new_wind=new_wind[0:len(new_wind)-4]
        insertwind = open(path_fast+inflow).read().splitlines()
        insertwind[15]= '"'+path_wind+new_wind+'.bts"    Filename       - Filename of time series data for uniform wind field.      (-)'
        insertwind[17]='         %i   RefHt          - Reference height for horizontal wind speed                (m)'%(h)
        open(path_fast+inflow,'w').write('\n'.join(insertwind))
    
def binary_turbsim_full_field_files(parameters):
    
    path_turbsim=parameters[0]
    turbsim=parameters[1]
    path_fast = parameters[2]
    path_modules = parameters[3]
    turbinefast=parameters[4]
    v = parameters[5]
    h = parameters[6]
    t = parameters[7]
    s = parameters[8]
    n=parameters[9]
    frequency = parameters[10]
    
    path_turbsim=path_turbsim+'/'
    path_fast = path_fast+'/'
    path_modules = path_modules+'/'
    turbinefast=str(turbinefast)
    
    fast_input = open(path_fast+turbinefast).read().splitlines()
    wind_INP = str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'.inp'

    ## Get inflow wind

    inflow_line=fast_input[36].split()
    Inflow = inflow_line[0]
    Inflow=Inflow[1:len(Inflow)-1]
        
    ## Modify inflow wind
    
    wind_inflow= open(path_fast+Inflow).read().splitlines()
    wind_inflow[4]='          3   WindType       - switch for wind file type (1=steady; 2=uniform; 3=binary TurbSim FF; 4=binary Bladed-style FF; 5=HAWC format; 6=User defined)'
    open(path_fast+Inflow,'w').write('\n'.join(wind_inflow))

    ## Get wind
    
    wind_line=wind_inflow[20].split()
    wind = wind_line[0]
    wind = wind[1:len(wind)-1]
    ## Get Wind name only and modify path

    wind_name = ''
    for i in wind:
        if i =='/':
            wind_name=''
        else:
            wind_name=wind_name+i

    path_wind = wind[0:(len(wind)-len(wind_name))]
    wind_name = wind_name[0:len(wind_name)-4]
    ## Create new wind file
    wind_WND = wind_INP[0:len(wind_INP)-4]
    if os.path.exists(path_modules+path_wind+wind_WND+'.wnd')==False:
        
        new_wind = open(path_modules+path_wind+wind_INP, 'w')
        txtwind = open(path_modules+path_wind+wind_name +'.inp').read().splitlines()
            
        for linha in txtwind:
            new_wind.write(linha+'\n')
        new_wind.close()

        ## Elasto dyn ##
        a = 0
        Elasto_line = fast_input[32].split()
        Elasto = Elasto_line[0]
        Elasto = Elasto[1:len(Elasto)-1]

        Elasto_dyn=''
        for i in Elasto:
            if i == '/':
                Elasto_dyn = ''
            else:
                Elasto_dyn = Elasto_dyn+i
        Elasto_dyn = path_modules+Elasto_dyn

        get_radius = open(Elasto_dyn).read().splitlines()

        radius_list=get_radius[44].split()
        radius = radius_list[0]
        diameter = int(radius)*2.5

        hub_height_list=get_radius[63].split()
        hub_height = hub_height_list[0]

        ## Modify INP parameters ##

        v = str(v)
        s = str(s)
        t = str(t)

        new_wind = path_modules+path_wind+wind_INP
        
        insert = open(new_wind).read().splitlines()
        RandSeed1 = randrange(-2147483648, 2147483647)
        RandSeed2 = randrange(-2147483648, 2147483647)
        insert[3] = '%s             RandSeed1       - First random seed  (-2147483648 to 2147483647)'%(RandSeed1)
        insert[4] = '%s             RandSeed2       - Second random seed (-2147483648 to 2147483647) for intrinsic pRNG, or an alternative pRNG: "RanLux" or "RNSNLW"'%(RandSeed2)
        insert[19]= '%s              TimeStep        - Time step [seconds]'%(frequency/10)
        insert[20]='%s              AnalysisTime    - Length of analysis time series [seconds] (program will add time if necessary: AnalysisTime = MAX(AnalysisTime, UsableTime+GridWidth/MeanHHWS) )'%(s)
        insert[21]='%s              UsableTime      - Usable length of output time series [seconds] (program will add GridWidth/MeanHHWS seconds)'%(s)    
        insert[22]='%s              HubHt           - Hub height [m] (should be > 0.5*GridHeight)' %(hub_height)
        insert[23]='%s              GridHeight      - Grid height [m]'%(diameter)
        insert[24]='%s              GridWidth       - Grid width [m] (should be >= 2*(RotorRadius+ShaftLength))'%(diameter)
        insert[31]='%s              IECturbc        - IEC turbulence characteristic ("A", "B", "C" or the turbulence intensity in percent) ("KHTEST" option with NWTCUP model, not used for other models)'%(t)
        insert[35]='%s              RefHt           - Height of the reference wind speed [m]'%(hub_height)
        insert[36]='%s              URef            - Mean (total) wind speed at the reference height [m/s] (or "default" for JET wind profile)'%(v)
        open(new_wind, 'w').write('\n'.join(insert))
        
        print(path_turbsim+turbsim, new_wind)
        subprocess.run([path_turbsim+turbsim, new_wind])

    ## Inflow Wind
    insertwind = open(path_fast+Inflow).read().splitlines()
    insertwind[19]= '"'+path_wind+wind_WND+'"    Filename       - Name of the Full field wind file to use (.bts)'
    open(path_fast+Inflow,'w').write('\n'.join(insertwind))  
        
############################################################################################################################################################################################        
############################################################################################################################################################################################

def binary_bladed_style_full_field(parameters):

    path_turbsim=parameters[0]
    turbsim=parameters[1]
    path_fast = parameters[2]
    path_modules = parameters[3]
    turbinefast=parameters[4]
    v = parameters[5]
    h = parameters[6]
    t = parameters[7]
    s = parameters[8]
    n=parameters[9]
    frequency = parameters[10]
    
    path_turbsim=path_turbsim+'/'
    path_fast = path_fast+'/'
    path_modules = path_modules+'/'
    turbinefast=str(turbinefast)
    
    fast_input = open(path_fast+turbinefast).read().splitlines()
    wind_INP = str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'.inp'

    ## Get inflow wind

    inflow_line=fast_input[36].split()
    Inflow = inflow_line[0]
    Inflow=Inflow[1:len(Inflow)-1]
        
    ## Modify inflow wind
    
    wind_inflow= open(path_fast+Inflow).read().splitlines()
    wind_inflow[4]='          4   WindType       - switch for wind file type (1=steady; 2=uniform; 3=binary TurbSim FF; 4=binary Bladed-style FF; 5=HAWC format; 6=User defined)'
    open(path_fast+Inflow,'w').write('\n'.join(wind_inflow))

    ## Get wind
    
    wind_line=wind_inflow[22].split()
    wind = wind_line[0]
    wind = wind[1:len(wind)-1]
                
    ## Get Wind name only and modify path

    wind_name = ''
    for i in wind:
        if i =='/':
            wind_name=''
        else:
            wind_name=wind_name+i

    path_wind = wind[0:(len(wind)-len(wind_name))]

    ## Create new wind file
    wind_WND = wind_INP[0:len(wind_INP)-4]

    if os.path.exists(path_modules+path_wind+wind_WND+'.wnd')==False:
        
        new_wind = open(path_modules+path_wind+wind_INP, 'w')
        txtwind = open(path_modules+path_wind+wind_name+'.inp').read().splitlines()
            
        for linha in txtwind:
            new_wind.write(linha+'\n')
        new_wind.close()

        ## Elasto dyn ##
        a = 0
        Elasto_line = fast_input[21].split()
        Elasto = Elasto_line[0]
        Elasto = Elasto[1:len(Elasto)-1]

        Elasto_dyn=''
        for i in Elasto:
            if i == '/':
                Elasto_dyn = ''
            else:
                Elasto_dyn = Elasto_dyn+i
        Elasto_dyn = path_modules+Elasto_dyn

        get_radius = open(Elasto_dyn).read().splitlines()

        radius_list=get_radius[46].split()
        radius = radius_list[0]
        diameter = int(radius)*2.5

        hub_height_list=get_radius[65].split()
        hub_height = hub_height_list[0]

        ## Modify INP parameters ##

        v = str(v)
        s = str(s)
        t = str(t)

        new_wind = path_modules+path_wind+wind_INP
        
        insert = open(new_wind).read().splitlines()
        RandSeed1 = randrange(-2147483648, 2147483647)
        RandSeed2 = randrange(-2147483648, 2147483647)
        insert[3] = '%s             RandSeed1       - First random seed  (-2147483648 to 2147483647)'%(RandSeed1)
        insert[4] = '%s             RandSeed2       - Second random seed (-2147483648 to 2147483647) for intrinsic pRNG, or an alternative pRNG: "RanLux" or "RNSNLW"'%(RandSeed2)
        insert[19]= '%s              TimeStep        - Time step [seconds]'%(frequency/10)
        insert[20]='%s              AnalysisTime    - Length of analysis time series [seconds] (program will add time if necessary: AnalysisTime = MAX(AnalysisTime, UsableTime+GridWidth/MeanHHWS) )'%(s)
        insert[21]='%s              UsableTime      - Usable length of output time series [seconds] (program will add GridWidth/MeanHHWS seconds)'%(s)    
        insert[22]='%s              HubHt           - Hub height [m] (should be > 0.5*GridHeight)' %(hub_height)
        insert[23]='%s              GridHeight      - Grid height [m]'%(diameter)
        insert[24]='%s              GridWidth       - Grid width [m] (should be >= 2*(RotorRadius+ShaftLength))'%(diameter)
        insert[31]='%s              IECturbc        - IEC turbulence characteristic ("A", "B", "C" or the turbulence intensity in percent) ("KHTEST" option with NWTCUP model, not used for other models)'%(t)
        insert[35]='%s              RefHt           - Height of the reference wind speed [m]'%(hub_height)
        insert[36]='%s              URef            - Mean (total) wind speed at the reference height [m/s] (or "default" for JET wind profile)'%(v)
        open(new_wind, 'w').write('\n'.join(insert))
        
        subprocess.run([path_turbsim+turbsim, new_wind])

    ## Inflow Wind
    insertwind = open(path_fast+Inflow).read().splitlines()
    insertwind[22]= '"'+path_wind+wind_WND+'"    FilenameRoot   - Rootname of the full-field wind file to use (.wnd, .sum)'
    open(path_fast+Inflow,'w').write('\n'.join(insertwind))   
