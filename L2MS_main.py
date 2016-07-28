#import relevant libraries
import L2MS_plot
import L2MS_analysis
import os
import numpy as np
import sys

#define paths
data_path = '/Users/kyleuckert/Documents/Research/MS/Data/2015JUL22/enstatite_tryptophan_1000ppm_room_temp/'
analysis_path='/Users/kyleuckert/Documents/Research/MS/Analysis/2015JUL22/enstatite_tryptophan_1000ppm_room_temp/'
IR_data_path=['/Users/kyleuckert/Documents/Research/MS/NIST_IR_spectra/']
#IR_data_path=['/Users/kyleuckert/Documents/Research/AOTF_IR_spectrometer/Data/2014AUG_epsomite_tryp/', '/Users/kyleuckert/Documents/Research/AOTF_IR_spectrometer/Data/2015JUL23/']

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
#read IR wavelengths (index 0 in file list)
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

#calculate std of spectrum for every file
noise_std={}
#the mass range to calculate the std over
mass_range = [165, 175]
for filename in file_list:
	#data stored in dictionary
	#define key
	key=filename.lstrip('filenames_')
	key=key.rstrip('.txt')
	#read all files within file list
	noise_std[key]=[]
	L2MS_analysis.std_values(data[key+'_mass'], data[key+'_intensity'], noise_std[key], mass_range)

#print 'std of spectrum: ', noise_std['breadboard']

#calculate integrated peak value
peak_center=130
#peak must be the highest within this range (125-135)
#integration is over entire peak_width range
peak_width=10
#boundary for peak area calculation (0.5 is FWHM)
int_frac=0.9
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
	#old calculation - integrate over entire width
	#L2MS_analysis.peak_value(data[key+'_mass'], data[key+'_intensity'], peak130[key], peak_center, peak_width)
	#new method - integrate over specified range
	L2MS_analysis.peak_value_FWHM(data[key+'_mass'], data[key+'_intensity'], peak130[key], peak_center, peak_width, int_frac)

#print 'int peak 130 Da: ', peak130['breadboard']
#int_SNR = np.array(peak130['breadboard'])/np.array(noise_std['breadboard'])
#print 'int peak SNR= ', int_SNR

#calculate max peak intensity
peak_center=130
#peak must be the highest within this range (128-132)
peak_width=4
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

#print 'max peak 130 Da: ', max_peak130['breadboard']
#this is a better SNR estimate than the int_SNR
peak_SNR = np.array(max_peak130['breadboard'])/np.array(noise_std['breadboard'])
#print 'max peak SNR= ', peak_SNR

#find peak
peak_approx = 150
peak_width = 10
peak_location = L2MS_analysis.max_peak_location(data['IR_mass'][5], data['IR_intensity'][5], peak_approx, peak_width)
print 'peak location: ', peak_location

#find peaks
#estimate of peak location
peak_approx = [180, 202]
#width to search for max value
peak_range = [10, 10]
#list to hold peak locations
peak_location = []
L2MS_analysis.max_peak_locations(data['breadboard_mass'][0], data['breadboard_intensity'][0], peak_approx, peak_range, peak_location)
print 'peak location: ', peak_location

#read IR spectrum
IR_file=['caffeic_acid_NIST.txt']
#IR_file=['tryptophan_powder/tryptophan_powder.txt', 'enstatite_powder/enstatite_powder.txt']
IR_data={}

for i, filename in enumerate(IR_file):
	#data stored in dictionary
	#define key
	#for NIST
	key = filename
	#take all characters after '/' (for AOTF)
	#key = filename.split('/',1)[-1]
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

#LOD for organic in mineral
concentration = [10000, 1000, 100]
#integrated peak vs concentration
L2MS_plot.plot_peak_vs_concentration(peak180['breadboard'], concentration, 'Integrated 180 Da Peak', '180Da_int_vs_concentration.png')
#max peak vs concentration
L2MS_plot.plot_peak_vs_concentration(max_peak180['breadboard'], concentration, 'Max 180 Da Peak Value', '180Da_max_vs_concentration.png')

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

#plot smoothed mass spectrum
L2MS_plot.plot_mass_spectrum_smooth(np.array(data['IR_mass'][4]), np.array(data['IR_intensity'][4]), [0,250], '2935_mass_spectrum.png', 10)


#to plot manually (need to comment out exit command)
sys.exit()
#need to add to start:
#import matplotlib
#import pylab
#from matplotlib.ticker import AutoMinorLocator
#import matplotlib.pyplot as plt


#compare mass spectra, offset
fig = plt.figure(dpi=200)
ax1=fig.add_subplot(111)
ax1.plot(data['breadboard_mass'][0], [x+0.025 for x in data['breadboard_intensity'][0]], 'b-', data['breadboard_mass'][1], [x+0.01 for x in data['breadboard_intensity'][1]], 'r-', data['breadboard_mass'][2], data['breadboard_intensity'][2], 'g-')
ax1.set_xlabel('Mass/Charge (Da)')
ax1.set_ylabel('Intensity (mV)')
ax1.text(0.29, 0.84, '1,000 ppm (0.1%)', verticalalignment='bottom', horizontalalignment='right', transform=ax1.transAxes, color='r')
ax1.text(0.28, 0.92, '10,000 ppm (1%)', verticalalignment='bottom', horizontalalignment='right', transform=ax1.transAxes, color='b')
ax1.text(0.28, 0.76, '100 ppm (0.01%)', verticalalignment='bottom', horizontalalignment='right', transform=ax1.transAxes, color='g')
ax1.set_xlim([0,250])
#for log scale:
#ax1.set_yscale('log')
#ax1.set_ylim([5E-3,1])
#ax1.set_title('tryptophan: 2935 nm')
ax1.xaxis.set_minor_locator(AutoMinorLocator(5))
ax1.yaxis.set_minor_locator(AutoMinorLocator(2)) 
#plt.show()
pylab.savefig('caffeic_acid_concentration_series_offset.png', dpi=200)
plt.clf()


#plot integrated peak value (blue) and SNR (red)
#extrapolate to SNR=10 (line of best fit)
fig, ax1=plt.subplots()
ax1.plot([10000,1000,100], max_peak180['breadboard'], 'b.', markersize=15)
ax1.set_xlabel('concentration (ppm)')
ax1.set_xscale('log')
ax1.set_xlim([10,50000])
# Make the y-axis label and tick labels match the line color.
ax1.set_ylabel('Integrated Peak Intensity', color='b')
ax1.set_yscale('log')
ax1.minorticks_on()
ax1.tick_params(axis='y', colors='b')
ax1.spines['left'].set_color('b')
for t in ax1.yaxis.get_minorticklines():
	t.set_color('b')
ax2 = ax1.twinx()
ax2.set_xlim([10,50000])
ax2.plot([10000,1000,100], peak_SNR, 'r.', markersize=15)
#line of best fit:
#ax2.plot([10000,1000,100,10,1], np.poly1d(np.polyfit([10000,1000,100], peak_SNR, 3))([10000,1000,100,10,1]), 'r-')
ax2.plot([10000,1000,100], peak_SNR, 'r-')
ax2.set_yscale('log')
ax2.set_ylabel('SNR (180 Da peak value / $\sigma$)', color='r')
ax2.minorticks_on()
ax2.tick_params(axis='y', colors='r')
ax2.spines['right'].set_color('r')
for t in ax2.yaxis.get_minorticklines():
	t.set_color('r')
#plt.show()
pylab.savefig('caffeic_acid_concentration_int_peak_SNR.png', format='png', dpi=100)
plt.clf()


