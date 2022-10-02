# x-*- coding: utf-8 -*-
"""
Created on Mon Nov 12 16:00:53 2018
 
"""

import fast_nrel as fst
import numpy as np
import pandas as pd
import random

path_modules = '5MW_Land_DLL_WTurb' # MODULE PATH
path_fast= 'C:/Users/LeonardoDiasdaRosa/Desktop/fast'# FAST PATH
turbsim_path =  'C:/Users/LeonardoDiasdaRosa/Desktop/fast/turbsim' #TURBSIM PATH
turbsim = 'TurbSim' # TURBSIM MAIN
turbinefast = '5MW_Land_DLL_WTurb.fst' # FAST .FST

############################################################### Parameters ###############################################################

mfile='C:/Softwares/OpenFAST/FASTRotSpeedEstStandardDataset.m'
#wind_speed=[7.4,7.5,7.7,8,8.3,8.5,8.6,8.9,9.2,9.5,9.8,10] # Region2 TRAINING
#wind_speed=[7.6,7.9,8.2,8.4, 8.7, 9.1, 9.2,9.7] # Region2 TESTING
wind_speed=[10] # Region3 TRAINING
wind_height = [84]  #hub height (meters)
turbulence = [5] #turbulence intensity (%)
duration = [120]  #duracao da time-series (seconds) 
fast_frequency = [20] # data output frequency in hertz
number_1=1
number_2=2
############################################################### Routine ##################################################################

for v in wind_speed:
    for t in turbulence:
        for h in wind_height:
            for s in duration:
                for f in fast_frequency:
                    for n in range(number_1,number_2):
                        parameters = [turbsim_path,turbsim,path_fast,path_modules,turbinefast,v,h,t,s,n,f,mfile]
                        fst.wind.binary_turbsim_full_field_files(parameters)
                        fst.Customized.FAST.simulation(parameters)
