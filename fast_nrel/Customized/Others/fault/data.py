import os
import subprocess
import shutil
import matlab.engine
import fast_nrel as fst
import xlwt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft

def csv_out(parameters):

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

    turbinefast = turbinefast[0:len(turbinefast)-4]

    if os.path.isdir(path_fast+turbinefast+' Customized - Collective Pitch Controller/Blade Mass Fault/'+turbinefast+'-'+str(v)+'ms/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'-'+str(e)+'BladeMassFault/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'-'+str(e)+'BladeMassFault.sfunc.out')==False:
        print("You don't have one simulation for getting csv data")
    sim_path = path_fast+turbinefast+' Customized - Collective Pitch Controller/Blade Mass Fault/'+turbinefast+'-'+str(v)+'ms/'+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'-'+str(e)+'BladeMassFault/'
    out_file = sim_path+turbinefast+'-'+str(v)+'ms-'+str(t)+'ti-'+str(h)+'m-'+str(s)+'s-'+str(n)+'-'+str(e)+'BladeMassFault.sfunc.out'
    out_file_noHeaderStr = out_file[0:len(out_file)-4]+"noHeader.out"

    out_header = open(out_file).read().splitlines()
    out_file_header=open(out_file).read().splitlines()
    out_noHeader = open(out_file_noHeaderStr,'w')

    i = 0
    for linha in out_header:
            if i >5:
                    out_noHeader.write(linha+'\n')
            else:
                    i=i+1

    out_noHeader.close()

    f = open(out_file_noHeaderStr, 'r+')                  
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
            workbook.save(out_file_noHeaderStr+'.xls')
            i+=1
