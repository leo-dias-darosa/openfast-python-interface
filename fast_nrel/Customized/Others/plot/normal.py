import pandas as pd
import matplotlib.pyplot as plt
import xlwt
import os

def IEC_output(parameters):

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

    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/FAST Standalone Outputs/IEC61400.13 Outputs/'+turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s')==False:
        print('Run your turbine with '+str(v)+'m/s wind speed '+str(h)+'hub heigh '+str(t)+'% turbulence intensity with '+str(s)+' seconds of duration first')
    else:
        new_path = path_fast+turbinefast+'-'+str(v)+'ms/FAST Standalone Outputs/IEC61400.13 Outputs/'+turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s/'
        out = turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s.out'
        
    sim_path = new_path+'/Output data/'
    standard_out = open(new_path+out).read().splitlines()
    output_string = out[0:len(out)-4]

    if os.path.exists(new_path+'/Output data') == False:
        os.mkdir(new_path+'/Output data')

    sim_path = new_path+'/Output data/'
    out_noHeader = open(sim_path+output_string+'noHeader.out','w')
                            
    i = 0
    for linha in standard_out:
        if i >6:
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
    for column in column_list:
        for item in range(len(column)):
            worksheet.write(item, i, column[item])
        workbook.save(out_noHeader+'.xls')
        i+=1
        
    dados = pd.read_excel(out_noHeader+'.xls')
    Time = dados.iloc[2:,0]
    
    FlapwiseBlade1RootM = dados.iloc[2:,4]
    FlapwiseBlade2RootM = dados.iloc[2:,6]
    FlapwiseBlade3RootM = dados.iloc[2:,8]
    
    EdgewiseBlade1RootM = dados.iloc[2:,5]
    EdgewiseBlade2RootM = dados.iloc[2:,7]
    EdgewiseBlade3RootM = dados.iloc[2:,9]
    
    RotorTilt = dados.iloc[2:,10]
    RotorYaw = dados.iloc[2:,11]
    RotorTorque = dados.iloc[2:,12]
    
    PitchLoadR1 = dados.iloc[2:,13]
    PitchLoadR2 = dados.iloc[2:,14]
    PitchLoadR3 = dados.iloc[2:,15]
    
    PitchLoadM1 = dados.iloc[2:,16]
    PitchLoadM2 = dados.iloc[2:,17]
    PitchLoadM3 = dados.iloc[2:,18]
    
    TowerTopAccNormal = dados.iloc[2:,19]
    TowerTopAccLat = dados.iloc[2:,20]
    
    TowerMidMoNormal = dados.iloc[2:,21]
    TowerMidMoLat = dados.iloc[2:,22]
    
    TowerTopMoNormal = dados.iloc[2:,23]
    TowerTopMoLat = dados.iloc[2:,24]
    
    Power = dados.iloc[2:,25]
    RotorSpeed = dados.iloc[2:,26]
    GeneratorSpeed = dados.iloc[2:,27]
    Azimuth = dados.iloc[2:,28]
    
    Pitch1 = dados.iloc[2:,29]
    Pitch2 = dados.iloc[2:,30]
    Pitch3 = dados.iloc[2:,31]
         
    #%% Graficos
    ## Flapwise blade root moment ##
    
    plt.close('all')
    
    plt.subplot(3,1,1)
    plt.plot(FlapwiseBlade1RootM,'b')
    plt.title('Flapwise Blade Root Moments \n Blade 1')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)
    
    plt.subplot(3,1,2)
    plt.plot(FlapwiseBlade2RootM,'b')
    plt.title('Blade 2')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None) 
    
    plt.subplot(3,1,3)
    plt.plot(Time,FlapwiseBlade3RootM,'b')
    plt.title('Blade 3')
    plt.ylabel('kN.m')
    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.box(on=None) 
    plt.tight_layout()
    
    plt.savefig(sim_path+'/BladesRootsFlapsMoments.png',bbox_inches='tight')
    
    ## Edgewise blade root moment ##
       
    plt.figure()
    plt.subplot(3,1,1)
    plt.plot(EdgewiseBlade1RootM,'b')
    plt.title('Edgewise Blade Root Moments \n Blade 1')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)    
    
    plt.subplot(3,1,2)
    plt.plot(EdgewiseBlade2RootM,'b')
    plt.title('Blade 2')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)    
    
    plt.subplot(3,1,3)
    plt.plot(Time,EdgewiseBlade3RootM,'b')
    plt.title('Blade 3')
    plt.ylabel('kN.m')
    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.box(on=None)
    plt.tight_layout()
    
    plt.savefig(sim_path+'/BladesRootsEdgeMoments.png',bbox_inches='tight')
    
    ## Rotor moments ##
    
    plt.figure()
    plt.subplot(3,1,1)
    plt.plot(RotorTilt,'b')
    plt.title('Rotor Moments \n Rotor tilt moment')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)    
    
    
    plt.subplot(3,1,2)
    plt.plot(RotorYaw,'b')
    plt.title('Rotor yaw moment')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)    
    
    
    plt.subplot(3,1,3)
    plt.plot(Time,RotorTorque,'b')
    plt.title('Rotor Torque')
    plt.ylabel('kN.m')
    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.box(on=None)    
    plt.tight_layout()
         
    plt.savefig(sim_path+'/RotorMoments.png',bbox_inches='tight')
    
    ## Pitch actuaion loads blade root ##
    
    plt.figure()
    plt.subplot(3,1,1)
    plt.plot(PitchLoadR1,'b')
    plt.title('Pitch actuation loads at blade root \n Blade 1')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)    
    
       
    plt.subplot(3,1,2)
    plt.plot(PitchLoadR2,'b')
    plt.title('Blade 2')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)    
    
    
    plt.subplot(3,1,3)
    plt.plot(Time,PitchLoadR3,'b')
    plt.title('Blade 3')
    plt.ylabel('kN.m')
    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.box(on=None)    
    plt.tight_layout()
    
    plt.savefig(sim_path+'/PitchActuationLoadsRoot.png',bbox_inches='tight')
    
    ## Pitch actuaion loads blade mid ##
      
    plt.figure()
    plt.subplot(3,1,1)
    plt.plot(PitchLoadM1,'b')
    plt.title('Pitch actuation loads at blade mid \n Blade 1')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)    
                  
    plt.subplot(3,1,2)
    plt.plot(PitchLoadM2,'b')
    plt.title(' Blade 2')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)                           
    
    plt.subplot(3,1,3)
    plt.plot(Time,PitchLoadM3,'b')
    plt.title(' Blade 3')
    plt.ylabel('kN.m')
    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.box(on=None)    
    plt.tight_layout()
    
    plt.savefig(sim_path+'/PitchActuationLoadsMid.png',bbox_inches='tight')
    
    ## Tower top accelerations ##
    
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(TowerTopAccNormal,'b')
    plt.title('Tower top accelerations \n Normal direction')
    plt.ylabel('m/s²')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)                    
       
    plt.subplot(2,1,2)
    plt.plot(Time,TowerTopAccLat,'b')
    plt.title('Lateral direction')
    plt.ylabel('m/s²')
    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.box(on=None)                
    plt.tight_layout()

    plt.savefig(sim_path+'/TowerTopAccelerations.png',bbox_inches='tight')
    
    ## Tower mid moments ##
    
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(TowerMidMoNormal,'b')
    plt.title('Tower mid moments \n Normal')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)                     
       
    plt.subplot(2,1,2)
    plt.plot(Time,TowerMidMoLat,'b')
    plt.title('Lateral')
    plt.ylabel('kN.m')
    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.box(on=None)    
    plt.tight_layout()
    
    plt.savefig(sim_path+'/TowerMidMoments.png',bbox_inches='tight')
    
    ## Tower top moments ##
    
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(TowerTopMoNormal,'b')
    plt.title('Tower top moments \n Normal')
    plt.ylabel('kN.m')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)    
       
    plt.subplot(2,1,2)
    plt.plot(Time,TowerTopMoLat,'b')
    plt.title('Lateral')
    plt.ylabel('kN.m')
    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.box(on=None)    
    plt.tight_layout()
    
    plt.savefig(sim_path+'/TowerTopMoments.png',bbox_inches='tight')
    
    ## Turbine Quantities ##
    
    plt.figure()
    plt.subplot(4,1,1)
    plt.plot(Power,'b')
    plt.title('Turbine quantities \n Power')
    plt.ylabel('kW')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)    
       
    plt.subplot(4,1,2)
    plt.plot(RotorSpeed,'b')
    plt.title('Rotor speed')
    plt.ylabel('RPM')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)    
    
    plt.subplot(4,1,3)
    plt.plot(GeneratorSpeed,'b')
    plt.title('Generator speed')
    plt.ylabel('RPM')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.tick_params(axis='x',labelbottom=False)
    plt.box(on=None)    
    
    plt.subplot(4,1,4)
    plt.plot(Time,Azimuth,'b')
    plt.title('Azimuth angle')
    plt.ylabel('degree')
    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s')
    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
    plt.box(on=None)   
    plt.tight_layout()
    
    plt.savefig(sim_path+'/TurbineQuantities.png',bbox_inches='tight')
    plt.close('all')
    print('Check at "'+new_path+'Output data" folder')

############################################################################################################################################################################################
############################################################################################################################################################################################
    
def User_output(parameters):

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

    if os.path.exists(path_fast+turbinefast+'-'+str(v)+'ms/FAST Standalone Outputs/User Outputs/'+turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s')==False:
        print('Run your turbine with '+str(v)+'m/s wind speed '+str(h)+'hub heigh '+str(t)+'% turbulence intensity with '+str(s)+' seconds of duration first')
    else:
        new_path = path_fast+turbinefast+'-'+str(v)+'ms/FAST Standalone Outputs/User Outputs/'+turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s/'
        out = turbinefast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s.out'
        
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
    for column in column_list:
        for item in range(len(column)):
            worksheet.write(item, i, column[item])
        workbook.save(out_noHeader+'.xls')
        i+=1
    
    data = pd.read_excel(out_noHeader+'.xls',header=None)
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
            
    for i in range(1,len(fig)):
        plt.close('all')
        plt.figure()
        plt.plot(Time,fig[i])
        plt.title(output[i])
        plt.ylabel(legend[i])
        plt.box(on=None)
        plt.savefig(sim_path+output[i]+'.png',bbox_inches='tight')
        plt.close('all')

      #%% Graficos
##    ## Flapwise blade root moment ##
##    
##    plt.close('all')
##    
##    plt.subplot(3,1,1)
##    plt.plot(FlapwiseBlade1RootM,'b')
##    plt.title('Flapwise Blade Root Moments \n Blade 1')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)
##    
##    plt.subplot(3,1,2)
##    plt.plot(FlapwiseBlade2RootM,'b')
##    plt.title('Blade 2')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None) 
##    
##    plt.subplot(3,1,3)
##    plt.plot(Time,FlapwiseBlade3RootM,'b')
##    plt.title('Blade 3')
##    plt.ylabel('kN.m')
##    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.box(on=None) 
##    plt.tight_layout()
##    
##    plt.savefig(sim_path+'/BladesRootsFlapsMoments.png',bbox_inches='tight')
##    
##    ## Edgewise blade root moment ##
##       
##    plt.figure()
##    plt.subplot(3,1,1)
##    plt.plot(EdgewiseBlade1RootM,'b')
##    plt.title('Edgewise Blade Root Moments \n Blade 1')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##    
##    plt.subplot(3,1,2)
##    plt.plot(EdgewiseBlade2RootM,'b')
##    plt.title('Blade 2')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##    
##    plt.subplot(3,1,3)
##    plt.plot(Time,EdgewiseBlade3RootM,'b')
##    plt.title('Blade 3')
##    plt.ylabel('kN.m')
##    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.box(on=None)
##    plt.tight_layout()
##    
##    plt.savefig(sim_path+'/BladesRootsEdgeMoments.png',bbox_inches='tight')
##    
##    ## Rotor moments ##
##    
##    plt.figure()
##    plt.subplot(3,1,1)
##    plt.plot(RotorTilt,'b')
##    plt.title('Rotor Moments \n Rotor tilt moment')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##    
##    
##    plt.subplot(3,1,2)
##    plt.plot(RotorYaw,'b')
##    plt.title('Rotor yaw moment')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##    
##    
##    plt.subplot(3,1,3)
##    plt.plot(Time,RotorTorque,'b')
##    plt.title('Rotor Torque')
##    plt.ylabel('kN.m')
##    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.box(on=None)    
##    plt.tight_layout()
##         
##    plt.savefig(sim_path+'/RotorMoments.png',bbox_inches='tight')
##    
##    ## Pitch actuaion loads blade root ##
##    
##    plt.figure()
##    plt.subplot(3,1,1)
##    plt.plot(PitchLoadR1,'b')
##    plt.title('Pitch actuation loads at blade root \n Blade 1')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##    
##       
##    plt.subplot(3,1,2)
##    plt.plot(PitchLoadR2,'b')
##    plt.title('Blade 2')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##    
##    
##    plt.subplot(3,1,3)
##    plt.plot(Time,PitchLoadR3,'b')
##    plt.title('Blade 3')
##    plt.ylabel('kN.m')
##    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.box(on=None)    
##    plt.tight_layout()
##    
##    plt.savefig(sim_path+'/PitchActuationLoadsRoot.png',bbox_inches='tight')
##    
##    ## Pitch actuaion loads blade mid ##
##      
##    plt.figure()
##    plt.subplot(3,1,1)
##    plt.plot(PitchLoadM1,'b')
##    plt.title('Pitch actuation loads at blade mid \n Blade 1')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##                  
##    plt.subplot(3,1,2)
##    plt.plot(PitchLoadM2,'b')
##    plt.title(' Blade 2')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)                           
##    
##    plt.subplot(3,1,3)
##    plt.plot(Time,PitchLoadM3,'b')
##    plt.title(' Blade 3')
##    plt.ylabel('kN.m')
##    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.box(on=None)    
##    plt.tight_layout()
##    
##    plt.savefig(sim_path+'/PitchActuationLoadsMid.png',bbox_inches='tight')
##    
##    ## Tower top accelerations ##
##    
##    plt.figure()
##    plt.subplot(2,1,1)
##    plt.plot(TowerTopAccNormal,'b')
##    plt.title('Tower top accelerations \n Normal direction')
##    plt.ylabel('m/s²')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)                    
##       
##    plt.subplot(2,1,2)
##    plt.plot(Time,TowerTopAccLat,'b')
##    plt.title('Lateral direction')
##    plt.ylabel('m/s²')
##    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.box(on=None)                
##    plt.tight_layout()
##
##    plt.savefig(sim_path+'/TowerTopAccelerations.png',bbox_inches='tight')
##    
##    ## Tower mid moments ##
##    
##    plt.figure()
##    plt.subplot(2,1,1)
##    plt.plot(TowerMidMoNormal,'b')
##    plt.title('Tower mid moments \n Normal')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)                     
##       
##    plt.subplot(2,1,2)
##    plt.plot(Time,TowerMidMoLat,'b')
##    plt.title('Lateral')
##    plt.ylabel('kN.m')
##    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.box(on=None)    
##    plt.tight_layout()
##    
##    plt.savefig(sim_path+'/TowerMidMoments.png',bbox_inches='tight')
##    
##    ## Tower top moments ##
##    
##    plt.figure()
##    plt.subplot(2,1,1)
##    plt.plot(TowerTopMoNormal,'b')
##    plt.title('Tower top moments \n Normal')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##       
##    plt.subplot(2,1,2)
##    plt.plot(Time,TowerTopMoLat,'b')
##    plt.title('Lateral')
##    plt.ylabel('kN.m')
##    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.box(on=None)    
##    plt.tight_layout()
##    
##    plt.savefig(sim_path+'/TowerTopMoments.png',bbox_inches='tight')
##    
##    ## Turbine Quantities ##
##    
##    plt.figure()
##    plt.subplot(4,1,1)
##    plt.plot(Power,'b')
##    plt.title('Turbine quantities \n Power')
##    plt.ylabel('kW')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##       
##    plt.subplot(4,1,2)
##    plt.plot(RotorSpeed,'b')
##    plt.title('Rotor speed')
##    plt.ylabel('RPM')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##    
##    plt.subplot(4,1,3)
##    plt.plot(GeneratorSpeed,'b')
##    plt.title('Generator speed')
##    plt.ylabel('RPM')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##    
##    plt.subplot(4,1,4)
##    plt.plot(Time,Azimuth,'b')
##    plt.title('Azimuth angle')
##    plt.ylabel('degree')
##    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.box(on=None)   
##    plt.tight_layout()
##    
##    plt.savefig(sim_path+'/TurbineQuantities.png',bbox_inches='tight')
##    plt.close('all')
##    print('Check at "'+new_path+'Output data" folder')
##    

##def comparison(parameters):
##    
##    path_modules = parameters[0]
##    path_fast = parameters[1]
##    turbinafast=parameters[2]
##    path_turbsim = parameters[3]
##    turbsim = parameters[4]
##    v = parameters[5]
##    h = parameters[6]
##    t = parameters[7]
##    s = parameters[8]
##    frequency = parameters[9]
##    e=parameters[10]
##    n = parameters[11]
##    failure_source=parameters[12]
##    
##    turbinafast = turbinafast[0:len(turbinafast)-4]
##    
##    padraooutsemerro = open(path_fast+turbinafast+'-'+str(v)+'ms/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(n+1)+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(n+1)+'.out').read().splitlines()
##    outsemerro = open(path_fast+turbinafast+'-'+str(v)+'ms/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(n+1)+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(n+1)+'SEMCABECALHO.out','w')
##                            
##    i = 0
##    for linha in padraooutsemerro:
##        if i >6:
##            outsemerro.write(linha+'\n')
##        else:
##            i=i+1 
##                                    
##    outsemerro.close()
##    
##    padraooutcomerro = open(path_fast+turbinafast+'-'+str(v)+'ms/'+failure_source+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'e'+failure_source+str(n+1)+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'e'+failure_source+str(n+1)+'.out').read().splitlines()
##    outcomerro = open(path_fast+turbinafast+'-'+str(v)+'ms/'+failure_source+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'e'+failure_source+str(n+1)+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'e'+failure_source+str(n+1)+'SEMCABECALHO.out','w')
##   
##    i = 0
##    for linha in padraooutcomerro:
##        if i >6:
##                outcomerro.write(linha+'\n')
##        else:
##            i=i+1   
##                                    
##    outcomerro.close()
##    
##    f = open(path_fast+turbinafast+'-'+str(v)+'ms/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(n+1)+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(n+1)+'SEMCABECALHO.out', 'r+')                  
##    row_list = []
##    
##    for row in f:
##        row_list.append(row.split())
##    column_list = zip(*row_list)
##    workbook = xlwt.Workbook()
##    worksheet = workbook.add_sheet('Sheet1')
##    i = 0 
##    for column in column_list:
##        for item in range(len(column)):
##            worksheet.write(item, i, column[item])
##        workbook.save(path_fast+turbinafast+'-'+str(v)+'ms/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(n+1)+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(n+1)+'SEMCABECALHO.xls')
##        i+=1        
##    g = open(path_fast+turbinafast+'-'+str(v)+'ms/'+failure_source+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'e'+failure_source+str(n+1)+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'e'+failure_source+str(n+1)+'SEMCABECALHO.out', 'r+')
##    row_list = []  
##    for row in g:
##        row_list.append(row.split())
##    column_list = zip(*row_list)
##    workbook = xlwt.Workbook()
##    worksheet = workbook.add_sheet('Sheet1')
##    i = 0 
##    for column in column_list:
##        for item in range(len(column)):
##            worksheet.write(item, i, column[item])
##        workbook.save(path_fast+turbinafast+'-'+str(v)+'ms/'+failure_source+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'e'+failure_source+str(n+1)+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'e'+failure_source+str(n+1)+'SEMCABECALHO.xls')
##        i+=1
##    
##    dados = pd.read_excel(path_fast+turbinafast+'-'+str(v)+'ms/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(n+1)+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(n+1)+'SEMCABECALHO.xls')
##    dadoserro = pd.read_excel(path_fast+turbinafast+'-'+str(v)+'ms/'+failure_source+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'e'+failure_source+str(n+1)+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'e'+failure_source+str(n+1)+'SEMCABECALHO.xls')
##                            
##    Time = dados.iloc[2:,0]
##    FlapwiseBlade1RootM = dados.iloc[2:,4]
##    FlapwiseBlade1RootMerro = dadoserro.iloc[2:,4]
##    FlapwiseBlade2RootM = dados.iloc[2:,6]
##    FlapwiseBlade2RootMerro = dadoserro.iloc[2:,6]
##    FlapwiseBlade3RootM = dados.iloc[2:,8]
##    FlapwiseBlade3RootMerro = dadoserro.iloc[2:,8]
##    
##    EdgewiseBlade1RootM = dados.iloc[2:,5]
##    EdgewiseBlade1RootMerro = dadoserro.iloc[2:,5]
##    EdgewiseBlade2RootM = dados.iloc[2:,7]
##    EdgewiseBlade2RootMerro = dadoserro.iloc[2:,7]
##    EdgewiseBlade3RootM = dados.iloc[2:,9]
##    EdgewiseBlade3RootMerro = dadoserro.iloc[2:,9]
##    
##    RotorTilt = dados.iloc[2:,10]
##    RotorTilterro = dadoserro.iloc[2:,10]
##    RotorYaw = dados.iloc[2:,11]
##    RotorYawerro = dadoserro.iloc[2:,11]
##    RotorTorque = dados.iloc[2:,12]
##    RotorTorqueerro = dadoserro.iloc[2:,12]
##    
##    PitchLoadR1 = dados.iloc[2:,13]
##    PitchLoadR1erro = dadoserro.iloc[2:,13]
##    PitchLoadR2 = dados.iloc[2:,14]
##    PitchLoadR2erro = dadoserro.iloc[2:,14]
##    PitchLoadR3 = dados.iloc[2:,15]
##    PitchLoadR3erro = dadoserro.iloc[2:,15]
##    
##    PitchLoadM1 = dados.iloc[2:,16]
##    PitchLoadM1erro = dadoserro.iloc[2:,16]
##    PitchLoadM2 = dados.iloc[2:,17]
##    PitchLoadM2erro = dadoserro.iloc[2:,17]
##    PitchLoadM3 = dados.iloc[2:,18]
##    PitchLoadM3erro = dadoserro.iloc[2:,18]
##    
##    TowerTopAccNormal = dados.iloc[2:,19]
##    TowerTopAccNormalerro = dadoserro.iloc[2:,19]
##    TowerTopAccLat = dados.iloc[2:,20]
##    TowerTopAccLaterro = dadoserro.iloc[2:,20]
##    
##    TowerMidMoNormal = dados.iloc[2:,21]
##    TowerMidMoNormalerro = dadoserro.iloc[2:,21]
##    TowerMidMoLat = dados.iloc[2:,22]
##    TowerMidMoLaterro = dadoserro.iloc[2:,22]
##    
##    TowerTopMoNormal = dados.iloc[2:,23]
##    TowerTopMoNormalerro = dadoserro.iloc[2:,23]
##    TowerTopMoLat = dados.iloc[2:,24]
##    TowerTopMoLaterro = dadoserro.iloc[2:,24]
##    
##    Power = dados.iloc[2:,25]
##    Powererro = dadoserro.iloc[2:,25]
##    RotorSpeed = dados.iloc[2:,26]
##    RotorSpeederro = dadoserro.iloc[2:,26]
##    GeneratorSpeed = dados.iloc[2:,27]
##    GeneratorSpeederro = dadoserro.iloc[2:,27]
##    Azimuth = dados.iloc[2:,28]
##    Azimutherro = dados.iloc[2:,28]
##    
##    Pitch1 = dados.iloc[2:,29]
##    Pitch1erro = dadoserro.iloc[2:,29]
##    Pitch2 = dados.iloc[2:,30]
##    Pitch2erro = dadoserro.iloc[2:,30]
##    Pitch3 = dados.iloc[2:,31]
##    Pitch3erro = dadoserro.iloc[2:,31]
##         
##    #%% Graficos
##    ## Flapwise blade root moment ##
##    
##    plt.close('all')
##    
##    plt.subplot(3,1,1)
##    plt.plot(FlapwiseBlade1RootM,'b', label = 'Sem Erro',)
##    plt.plot(FlapwiseBlade1RootMerro,'r', label = 'Com erro')
##    plt.plot(abs(FlapwiseBlade1RootM-FlapwiseBlade1RootMerro),'k',label='Diferença')
##    plt.title('Flapwise Blade Root Moments \n Blade 1')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)
##    
##    plt.subplot(3,1,2)
##    plt.plot(FlapwiseBlade2RootM,'b', label = 'Sem Erro',)
##    plt.plot(FlapwiseBlade2RootMerro,'r', label = 'Com erro')
##    plt.plot(abs(FlapwiseBlade2RootM-FlapwiseBlade2RootMerro),'k',label='Diferença')
##    plt.title('Blade 2')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None) 
##    
##    plt.subplot(3,1,3)
##    plt.plot(Time,FlapwiseBlade3RootM,'b', label = 'Sem Erro')
##    plt.plot(Time,FlapwiseBlade3RootMerro,'r', label = 'Com erro')
##    plt.plot(Time,abs(FlapwiseBlade3RootM-FlapwiseBlade3RootMerro),'k',label='Diferença')
##    plt.title('Blade 3')
##    plt.ylabel('kN.m')
##    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s, pá 1 '+str(e)+'% da massa original')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.box(on=None) 
##    plt.tight_layout()
##    
##    plt.savefig(path_fast+turbinafast+'-'+str(v)+'ms/'+failure_source+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'e'+failure_source+str(n+1)+'/BladesRootsFlapsMoments.png',bbox_inches='tight')
##    
##    ## Edgewise blade root moment ##
##       
##    plt.figure()
##    plt.subplot(3,1,1)
##    plt.plot(EdgewiseBlade1RootM,'b', label = 'Sem Erro')
##    plt.plot(EdgewiseBlade1RootMerro,'r', label = 'Com erro')
##    plt.plot(abs(EdgewiseBlade1RootM-EdgewiseBlade1RootMerro),'k',label='Diferença')
##    plt.title('Edgewise Blade Root Moments \n Blade 1')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##    
##    plt.subplot(3,1,2)
##    plt.plot(EdgewiseBlade2RootM,'b', label = 'Sem Erro')
##    plt.plot(EdgewiseBlade2RootMerro,'r', label = 'Com erro')
##    plt.plot(abs(EdgewiseBlade2RootM-EdgewiseBlade2RootMerro),'k',label='Diferença')
##    plt.title('Blade 2')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##    
##    plt.subplot(3,1,3)
##    plt.plot(Time,EdgewiseBlade3RootM,'b', label = 'Sem Erro')
##    plt.plot(Time,EdgewiseBlade3RootMerro,'r', label = 'Com erro')
##    plt.plot(Time,abs(EdgewiseBlade3RootM-EdgewiseBlade3RootMerro),'k',label='Diferença')
##    plt.title('Blade 3')
##    plt.ylabel('kN.m')
##    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s, pá 1 '+str(e)+'% da massa original')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.box(on=None)
##    plt.tight_layout()
##    
##    plt.savefig(path_fast+turbinafast+'-'+str(v)+'ms/'+failure_source+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'e'+failure_source+str(n+1)+'/BladesRootsEdgeMoments.png',bbox_inches='tight')
##    
##    ## Rotor moments ##
##    
##    plt.figure()
##    plt.subplot(3,1,1)
##    plt.plot(RotorTilt,'b', label = 'Sem Erro')
##    plt.plot(RotorTilterro,'r', label = 'Com erro')
##    plt.plot(abs(RotorTilt-RotorTilterro),'k',label='Diferença')
##    plt.title('Rotor Moments \n Rotor tilt moment')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##    
##    
##    plt.subplot(3,1,2)
##    plt.plot(RotorYaw,'b', label = 'Sem Erro')
##    plt.plot(RotorYawerro,'r', label = 'Com erro')
##    plt.plot(abs(RotorYaw-RotorYawerro),'k',label='Diferença')
##    plt.title('Rotor yaw moment')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##    
##    
##    plt.subplot(3,1,3)
##    plt.plot(Time,RotorTorque,'b', label = 'Sem Erro')
##    plt.plot(Time,RotorTorqueerro,'r', label = 'Com erro')
##    plt.plot(Time,abs(RotorTorque-RotorTorqueerro),'k',label='Diferença')
##    plt.title('Rotor Torque')
##    plt.ylabel('kN.m')
##    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s, pá 1 '+str(e)+'% da massa original')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.box(on=None)    
##    plt.tight_layout()
##         
##    plt.savefig(path_fast+turbinafast+'-'+str(v)+'ms/'+failure_source+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'e'+failure_source+str(n+1)+'/RotorMoments.png',bbox_inches='tight')
##    
##    ## Pitch actuaion loads blade root ##
##    
##    plt.figure()
##    plt.subplot(3,1,1)
##    plt.plot(PitchLoadR1,'b', label = 'Sem Erro',)
##    plt.plot(PitchLoadR1erro,'r', label = 'Com erro')
##    plt.plot(abs(PitchLoadR1-PitchLoadR1erro),'k',label='Diferença')
##    plt.title('Pitch actuation loads at blade root \n Blade 1')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##    
##       
##    plt.subplot(3,1,2)
##    plt.plot(PitchLoadR2,'b', label = 'Sem Erro',)
##    plt.plot(PitchLoadR2erro,'r', label = 'Com erro')
##    plt.plot(abs(PitchLoadR2-PitchLoadR2erro),'k',label='Diferença')
##    plt.title('Blade 2')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##    
##    
##    plt.subplot(3,1,3)
##    plt.plot(Time,PitchLoadR3,'b', label = 'Sem Erro',)
##    plt.plot(Time,PitchLoadR3erro,'r', label = 'Com erro')
##    plt.plot(Time,abs(PitchLoadR3-PitchLoadR3erro),'k',label='Diferença')
##    plt.title('Blade 3')
##    plt.ylabel('kN.m')
##    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s, pá 1 '+str(e)+'% da massa original')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.box(on=None)    
##    plt.tight_layout()
##    
##    plt.savefig(path_fast+turbinafast+'-'+str(v)+'ms/'+failure_source+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'e'+failure_source+str(n+1)+'/PitchActuationLoadsRoot.png',bbox_inches='tight')
##    
##    ## Pitch actuaion loads blade mid ##
##      
##    plt.figure()
##    plt.subplot(3,1,1)
##    plt.plot(PitchLoadM1,'b', label = 'Sem Erro',)
##    plt.plot(PitchLoadM1erro,'r', label = 'Com erro')
##    plt.plot(abs(PitchLoadM1-PitchLoadM1erro),'k',label='Diferença')
##    plt.title('Pitch actuation loads at blade root \n Blade 1')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##                  
##    plt.subplot(3,1,2)
##    plt.plot(PitchLoadM2,'b', label = 'Sem Erro',)
##    plt.plot(PitchLoadM2erro,'r', label = 'Com erro')
##    plt.plot(abs(PitchLoadM2-PitchLoadM2erro),'k',label='Diferença')
##    plt.title(' Blade 2')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)                           
##    
##    plt.subplot(3,1,3)
##    plt.plot(Time,PitchLoadM3,'b', label = 'Sem Erro',)
##    plt.plot(Time,PitchLoadM3erro,'r', label = 'Com erro')
##    plt.plot(Time,abs(PitchLoadM3-PitchLoadM3erro),'k',label='Diferença')
##    plt.title(' Blade 3')
##    plt.ylabel('kN.m')
##    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s, pá 1 '+str(e)+'% da massa original')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.box(on=None)    
##    plt.tight_layout()
##    
##    plt.savefig(path_fast+turbinafast+'-'+str(v)+'ms/'+failure_source+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'e'+failure_source+str(n+1)+'/PitchActuationLoadsMid.png',bbox_inches='tight')
##    
##    ## Tower top accelerations ##
##    
##    plt.figure()
##    plt.subplot(2,1,1)
##    plt.plot(TowerTopAccNormal,'b', label = 'Sem Erro',)
##    plt.plot(TowerTopAccNormalerro,'r', label = 'Com erro')
##    plt.plot(abs(TowerTopAccNormal-TowerTopAccNormalerro),'k',label='Diferença')
##    plt.title('Tower top accelerations \n Normal direction')
##    plt.ylabel('m/s²')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)                    
##       
##    plt.subplot(2,1,2)
##    plt.plot(Time,TowerTopAccLat,'b', label = 'Sem Erro',)
##    plt.plot(Time,TowerTopAccLaterro,'r', label = 'Com erro')
##    plt.plot(Time,abs(TowerTopAccLat-TowerTopAccLaterro),'k',label='Diferença')
##    plt.title('Lateral direction')
##    plt.ylabel('m/s²')
##    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s, pá 1 '+str(e)+'% da massa original')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.box(on=None)                
##    plt.tight_layout()
##    
##    plt.savefig(path_fast+turbinafast+'-'+str(v)+'ms/'+failure_source+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'e'+failure_source+str(n+1)+'/TowerTopAccelerations.png',bbox_inches='tight')
##    
##    ## Tower mid moments ##
##    
##    plt.figure()
##    plt.subplot(2,1,1)
##    plt.plot(TowerMidMoNormal,'b', label = 'Sem Erro',)
##    plt.plot(TowerMidMoNormalerro,'r', label = 'Com erro')
##    plt.plot(abs(TowerMidMoNormal-TowerMidMoNormalerro),'k',label='Diferença')
##    plt.title('Tower mid moments \n Normal')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)                     
##       
##    plt.subplot(2,1,2)
##    plt.plot(Time,TowerMidMoLat,'b', label = 'Sem Erro',)
##    plt.plot(Time,TowerMidMoLaterro,'r', label = 'Com erro')
##    plt.plot(Time,abs(TowerMidMoLat-TowerMidMoLaterro),'k',label='Diferença')
##    plt.title('Lateral')
##    plt.ylabel('kN.m')
##    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s, pá 1 '+str(e)+'% da massa original')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.box(on=None)    
##    plt.tight_layout()
##    
##    plt.savefig(path_fast+turbinafast+'-'+str(v)+'ms/'+failure_source+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'e'+failure_source+str(n+1)+'/TowerMidMoments.png',bbox_inches='tight')
##    
##    ## Tower top moments ##
##    
##    plt.figure()
##    plt.subplot(2,1,1)
##    plt.plot(TowerTopMoNormal,'b', label = 'Sem Erro',)
##    plt.plot(TowerTopMoNormalerro,'r', label = 'Com erro')
##    plt.plot(abs(TowerTopMoNormal-TowerTopMoNormalerro),'k',label='Diferença')
##    plt.title('Tower top moments \n Normal')
##    plt.ylabel('kN.m')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##       
##    plt.subplot(2,1,2)
##    plt.plot(Time,TowerTopMoLat,'b', label = 'Sem Erro',)
##    plt.plot(Time,TowerTopMoLaterro,'r', label = 'Com erro')
##    plt.plot(Time,abs(TowerTopMoLat-TowerTopMoLaterro),'k',label='Diferença')
##    plt.title('Lateral')
##    plt.ylabel('kN.m')
##    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s, pá 1 '+str(e)+'% da massa original')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.box(on=None)    
##    plt.tight_layout()
##    
##    plt.savefig(path_fast+turbinafast+'-'+str(v)+'ms/'+failure_source+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'e'+failure_source+str(n+1)+'/TowerTopMoments.png',bbox_inches='tight')
##    
##    ## Turbine Quantities ##
##    
##    plt.figure()
##    plt.subplot(4,1,1)
##    plt.plot(Power,'b', label = 'Sem Erro',)
##    plt.plot(Powererro,'r', label = 'Com erro')
##    plt.plot(abs(Power-Powererro),'k',label='Diferença')
##    plt.title('Turbine quantities \n Power')
##    plt.ylabel('kW')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##       
##    plt.subplot(4,1,2)
##    plt.plot(RotorSpeed,'b', label = 'Sem Erro',)
##    plt.plot(RotorSpeederro,'r', label = 'Com erro')
##    plt.plot(abs(RotorSpeed-RotorSpeederro),'k',label='Diferença')
##    plt.title('Rotor speed')
##    plt.ylabel('RPM')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##    
##    plt.subplot(4,1,3)
##    plt.plot(GeneratorSpeed,'b', label = 'Sem Erro',)
##    plt.plot(GeneratorSpeederro,'r', label = 'Com erro')
##    plt.plot(abs(GeneratorSpeed-GeneratorSpeederro),'k',label='Diferença')
##    plt.title('Generator speed')
##    plt.ylabel('RPM')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.tick_params(axis='x',labelbottom=False)
##    plt.box(on=None)    
##    
##    plt.subplot(4,1,4)
##    plt.plot(Time,Azimuth,'b', label = 'Sem Erro',)
##    plt.plot(Time,Azimutherro,'r', label = 'Com erro')
##    plt.plot(Time,abs(Azimuth-Azimutherro),'k',label='Diferença')
##    plt.title('Azimuth angle')
##    plt.ylabel('degree')
##    plt.xlabel('time (s)\n\n Velocidade do vento '+str(v)+'m/s, pá 1 '+str(e)+'% da massa original')
##    plt.legend(frameon=False,bbox_to_anchor=(0.85, 0.88))
##    plt.box(on=None)   
##    plt.tight_layout()
##    
##    plt.savefig(path_fast+turbinafast+'-'+str(v)+'ms/'+failure_source+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'e'+failure_source+str(n+1)+'/TurbineQuantities.png',bbox_inches='tight')
##    plt.close('all')
##    print('Check at "'+turbinafast+'-'+str(v)+'ms/'+failure_source+'/'+turbinafast+'-'+str(v)+'ms-'+str(h)+'m-'+str(t)+'t-'+str(s)+'s-'+str(e)+'e'+failure_source+str(n+1)+'" folder')
