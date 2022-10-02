FAST_InputFileName = turbine_from_python;
matlab=matlab_from_python;
TMax = str2num(Time_from_python);
addpath(path_from_python); % User .m folder
simulation_number= num2str(SimulationNumber_from_python);
wind_speed=num2str(WindSpeed_from_python);
ti=num2str(Turbulence_from_python);

run(matlab)