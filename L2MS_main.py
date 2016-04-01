#import relevant libraries
import L2MS_plot
import L2MS_analysis
import os
import numpy as np
import sys

#define paths
data_path = '/Users/kyleuckert/Documents/Research/MS/Data/2015JUL22/enstatite_tryptophan_1000ppm_room_temp/'
analysis_path='/Users/kyleuckert/Documents/Research/MS/Analysis/2015JUL22/enstatite_tryptophan_1000ppm_room_temp/'
IR_data_path=['/Users/kyleuckert/Documents/Research/AOTF_IR_spectrometer/Data/2014AUG_epsomite_tryp/', '/Users/kyleuckert/Documents/Research/AOTF_IR_spectrometer/Data/2015JUL23/']

all_sample_files = 'filenames.txt'

#create list of data files
unix_command='\ls '+ data_path + ' | grep \'.txt\' > ' + analysis_path + all_sample_files
#comment next two lines out after first run
os.system(unix_command)
sys.exit()	

#########################################################
#main body

#names of file lists
file_list=['filenames_IR.txt', 'filenames_temp_2935.txt', 'filenames_temp_2710.txt']
#dictionary with 6 keys (mass and intensity for each list)
data = {}

#read all data
for filename in file_list:
	#data stored in dictionary
	#define key
	key=filename.lstrip('filenames_')
	key=key.rstrip('.txt')
	#read all files within file list
	data[key+'_mass']=[]
	data[key+'_intensity']=[]
	L2MS_analysis.read_data_files(data_path, analysis_path+filename, data[key+'_mass'], data[key+'_intensity'])

#array for IR wavelength list
IR = []
#read IR wavelengths
L2MS_analysis.IR_wavelength(analysis_path+file_list[0], IR)

#dictionary for temperature
temp = {}
#skip IR filenames (start at index 1)
for filename in file_list[1:]:
	#define key
	key=filename.lstrip('filenames_')
	key=key.rstrip('.txt')
	temp[key]=[]
	L2MS_analysis.temperature_id(analysis_path+filename, temp[key])

#calculate integrated peak value
peak_center=130
peak_width=4
#calculate the integrated peak value for every file
peak130={}
#this could be completed in the first loop, but is seprated for readability
for filename in file_list:
	#data stored in dictionary
	#define key
	key=filename.lstrip('filenames_')
	key=key.rstrip('.txt')
	#read all files within file list
	peak130[key]=[]
	L2MS_analysis.peak_value(data[key+'_mass'], data[key+'_intensity'], peak130[key], peak_center, peak_width)

#calculate max peak intensity
peak_center=130
#calculate the max peak value for every file
max_peak130={}
#this could be completed in the first loop, but is seprated for readability
for filename in file_list:
	#data stored in dictionary
	#define key
	key=filename.lstrip('filenames_')
	key=key.rstrip('.txt')
	#read all files within file list
	max_peak130[key]=[]
	L2MS_analysis.max_peak_value(data[key+'_mass'], data[key+'_intensity'], max_peak130[key], peak_center, peak_width)


#read IR spectrum
IR_file=['tryptophan_powder/tryptophan_powder.txt', 'enstatite_powder/enstatite_powder.txt']
IR_data={}

for i, filename in enumerate(IR_file):
	#data stored in dictionary
	#define key
	#take all characters after '/'
	key = filename.split('/',1)[-1]
	#key=key.rstrip('_powder.txt')
	key=key.split('_', 1)[0]
	#read all files within file list
	IR_data[key+'_wavelength']=[]
	IR_data[key+'_reflectance']=[]
	L2MS_analysis.read_IR_data(IR_data_path[i]+filename, IR_data[key+'_wavelength'], IR_data[key+'_reflectance'])


#normalize MS intensity (optional)
#data['IR_intensity'][:] = [x /np.array(data['IR_intensity']).max() for x in data['IR_intensity']]

#plot data
#plot 130 peak vs temperature at each wavelength (2935)
L2MS_plot.plot_peak_vs_T(peak130['temp_2935'], temp['temp_2935'], '2935 nm', '2935nm_integrated_peak_vs_T.png')
L2MS_plot.plot_peak_vs_T(peak130['temp_2710'], temp['temp_2710'], '2710 nm', '2710nm_integrated_peak_vs_T.png')

#plot IR spectrum
for filename in IR_file:
	#this could be completed earlier, but is separated for readability
	#define key
	#take all characters after '/'
	key = filename.split('/',1)[-1]
	#key=key.rstrip('_powder.txt')
	key=key.split('_', 1)[0]
	L2MS_plot.plot_IR_spectrum(np.array(IR_data[key+'_wavelength']), np.array(IR_data[key+'_reflectance']), [1.6, 3.6], str(key)+' IR spectrum', str(key)+'_IR_spectrum.png')

#plot 130 peak vs IR wavelength
L2MS_plot.plot_peak_vs_IR(peak130['IR'], IR, 'Integrated 130 Da Peak at -20 C', '130Da_vs_IR.png')

#plot mass spectrum wavelength dependence
L2MS_plot.plot_mass_spectrum_wavelength_with_IR(np.array(data['IR_mass']), np.array(data['IR_intensity']), np.array(IR), IR_file, IR_data, [2.7,3.05], 'L2MS_plot_IR_dependence.png')

#plot mass spectrum
L2MS_plot.plot_mass_spectrum(np.array(data['IR_mass'][4]), np.array(data['IR_intensity'][4]), [0,250], '2935_mass_spectrum.png')

#plot mass spectrum
L2MS_plot.plot_mass_spectrum_smooth(np.array(data['IR_mass'][4]), np.array(data['IR_intensity'][4]), [0,250], '2935_mass_spectrum.png', 10)


