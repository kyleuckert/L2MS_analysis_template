#import relevant libraries
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import pylab
from matplotlib import gridspec
import scipy.signal
import math
from matplotlib.ticker import AutoMinorLocator
#import matplotlib.font_manager as fm
#import plotly

#########################################################
#plotting function definitions:
def plot_peak_vs_T(peak_value, temperature, title, save_file):
	#sort lists by increasing temperature
	sorted_index = sorted(range(len(temperature)), key=lambda k: temperature[k])
	temp_temp=[]
	temp_peak=[]
	for index in sorted_index:
		#print temperature[index], peak_value[index]
		temp_temp.append(temperature[index])
		temp_peak.append(peak_value[index])
	#plt.plot(temperature, peak_value)
	plt.plot(temp_temp, temp_peak, 'k.')
	plt.plot(temp_temp, temp_peak, 'k-')
	plt.xlabel('Temperature ($^{\circ}$C)')
	plt.ylabel('Integrated peak')
	plt.title(title)
	#plt.show()
	pylab.savefig(save_file, format='png', dpi=100)
	plt.clf()

def plot_peak_vs_time(peak_value, time, title, save_file):
	#sort lists by increasing temperature
	sorted_index = sorted(range(len(time)), key=lambda k: time[k])
	temp_time=[]
	temp_peak=[]
	for index in sorted_index:
		#print temperature[index], peak_value[index]
		temp_time.append(time[index])
		temp_peak.append(peak_value[index])
	#plt.plot(temperature, peak_value)
	plt.plot(temp_time, temp_peak, 'k.')
	plt.plot(temp_time, temp_peak, 'k-')
	plt.xlabel('Delay Time ($\mu$s)')
	plt.ylabel('Integrated peak')
	plt.title(title)
	#plt.show()
	pylab.savefig(save_file, format='png', dpi=100)
	plt.clf()

def plot_max_vs_T(peak_value, temperature, title, save_file):
	#sort lists by increasing temperature
	sorted_index = sorted(range(len(temperature)), key=lambda k: temperature[k])
	temp_temp=[]
	temp_peak=[]
	for index in sorted_index:
		#print temperature[index], peak_value[index]
		temp_temp.append(temperature[index])
		temp_peak.append(peak_value[index])
	#plt.plot(temperature, peak_value)
	plt.plot(temp_temp, temp_peak, 'k.')
	plt.plot(temp_temp, temp_peak, 'k-')
	plt.xlabel('Temperature ($^{\circ}$C)')
	plt.ylabel('Max peak')
	plt.title(title)
	#plt.show()
	pylab.savefig(save_file, format='png', dpi=100)
	plt.clf()

def plot_max_peak_vs_T(peak_value, max_value, temperature, title, save_file):
	#sort lists by increasing temperature
	sorted_index = sorted(range(len(temperature)), key=lambda k: temperature[k])
	temp_temp=[]
	temp_peak=[]
	temp_max=[]
	for index in sorted_index:
		#print temperature[index], peak_value[index]
		temp_temp.append(temperature[index])
		temp_peak.append(peak_value[index])
		temp_max.append(max_value[index])

	fig, ax1=plt.subplots()
	ax1.plot(temp_temp, temp_peak, 'b.')
	ax1.plot(temp_temp, temp_peak, 'b-')
	ax1.set_xlabel('Temperature ($^{\circ}$C)')
	ax1.set_ylabel('Peak Value', color='b')
	for tl in ax1.get_yticklabels():
		tl.set_color('b')

	ax2 = ax1.twinx()
	ax2.plot(temp_temp, temp_max, 'r.')
	ax2.plot(temp_temp, temp_max, 'r-')
	ax2.set_ylabel('Max peak', color='r')
	for tl in ax2.get_yticklabels():
		tl.set_color('r')

	plt.title(title)
	#plt.show()
	pylab.savefig(save_file)
	plt.clf()

def plot_peak_vs_IR(peak_value, IR, title, save_file):
	#sort lists by increasing temperature
	sorted_index = sorted(range(len(IR)), key=lambda k: IR[k])
	temp_IR=[]
	temp_peak=[]
	for index in sorted_index:
		#print temperature[index], peak_value[index]
		temp_IR.append(IR[index])
		temp_peak.append(peak_value[index])
	#plt.plot(temperature, peak_value)
	plt.plot(temp_IR, temp_peak, 'k.')
	plt.plot(temp_IR, temp_peak, 'k-')
	plt.xlabel('IR wavelength (nm)')
	plt.ylabel('Peak Value')
	plt.title(title)
	#plt.show()
	pylab.savefig(save_file, format='png', dpi=100)
	plt.clf()

def plot_peak_vs_concentration(peak_value, con, title, save_file):
	#sort lists by increasing temperature
	sorted_index = sorted(range(len(con)), key=lambda k: con[k])
	temp_con=[]
	temp_peak=[]
	for index in sorted_index:
		#print temperature[index], peak_value[index]
		temp_con.append(con[index])
		temp_peak.append(peak_value[index])
	fig = plt.figure()
	ax1=fig.add_subplot(111)
	ax1.plot(temp_con, temp_peak, 'k.')
	ax1.plot(temp_con, temp_peak, 'k-')
	m, b = np.polyfit(temp_con, temp_peak, 1)
	#to add a line of best fit
	#ax1.plot([50,100,1000,10000,50000], np.poly1d(np.polyfit(temp_con, temp_peak, 2))([50,100,1000,10000,50000]), 'r-')
	ax1.set_xlabel('concentration (ppm)')
	ax1.set_ylabel('peak value')
	ax1.set_title(title)
	#ax1.set_xlim([10,50000])
	#for log scaling
	ax1.set_yscale('log')
	ax1.set_xscale('log')
	pylab.savefig(save_file, format='png', dpi=100)
	plt.clf()

def runningMeanFast(x, N):
    return np.convolve(x, np.ones((N,))/N)[(N-1):]

def plot_IR_spectrum(wavelength, reflectance, x_range, title, save_file):
	fig = plt.figure()
	ax1=fig.add_subplot(111)
	ax2=ax1.twiny()
	ax1.plot(wavelength.T, reflectance.T, '-')
	#ax1.plot(wavelength.T-0.00855064, reflectance.T, '-')
	#plt.plot(wavelength.T, runningMeanFast(reflectance.T,10))
	ax1.set_xlabel('Wavelength (nm)')
	ax1.set_ylabel('Reflectance')
	#ax1.set_ylabel('Transmitance')
	ax1.set_xlim(x_range)
	ax1.xaxis.set_minor_locator(AutoMinorLocator(5))
	ax1.yaxis.set_minor_locator(AutoMinorLocator(2)) 
	#remove tick label and tick marks
	ax2.xaxis.set_major_formatter(plt.NullFormatter())
	ax2.xaxis.set_minor_formatter(plt.NullFormatter())
	for tic in ax2.xaxis.get_major_ticks():
		tic.tick1On = tic.tick2On = False
		tic.label1On = tic.label2On = False

	ax2=ax1.twiny()
	ax2.set_xlabel('wavenumber (cm$^{-1}$)')
	#array with values of tick mark locations
	#wavenumber labels multiple of 1000 cm^-1
	wavenumber_label=[]
	wavenumber_location=[]
	for loc in range(int(1+(1E4/x_range[0] - 1E4/x_range[1])/1000)):
		wavenumber=int((1E4/x_range[0]) - 1000*loc)/1000*1000
		wavenumber_label.append(wavenumber)
		location= 1 - ((x_range[1] - 1E4/wavenumber)/(x_range[1] - x_range[0]))
		wavenumber_location.append(location)

	minor_locator=[]
	num_minor=len(wavenumber_location)*3
	for i in range(len(wavenumber_location)-1):
		diff=wavenumber_location[i+1]-wavenumber_location[i]
		for j in range(4):
			minor_locator.append((j+1) * (diff/4.0) + wavenumber_location[i])
	
	ax2.set_xticks(wavenumber_location)
	ax2.set_xticklabels(wavenumber_label)
	ax2.xaxis.set_minor_locator(plt.FixedLocator(minor_locator))

	#ax2.set_title(title)
	#plt.show()
	pylab.savefig(save_file)
	plt.clf()
	
def plot_mass_spectrum(mass, intensity, mass_range, save_file):
	#plt.close('all')
	fig = plt.figure()
	ax1=fig.add_subplot(111)
	ax1.plot(mass, intensity, '-')
	ax1.set_xlabel('Mass/Charge (Da)')
	ax1.set_ylabel('Intensity (V)')
	ax1.set_xlim(mass_range)
	#ax1.set_ylim([0,0.5])
	ax1.xaxis.set_minor_locator(AutoMinorLocator(5))
	ax1.yaxis.set_minor_locator(AutoMinorLocator(2)) 
	#plt.show()
	pylab.savefig(save_file)
	plt.clf()

def plot_mass_spectrum_wavelength(mass, intensity, IR, save_file):
	cmap=cm.get_cmap('jet')
	fig, ax=plt.subplots()
	ax.set_axis_bgcolor('black')

	cs = plt.contourf(IR, mass[0], intensity.T-0.00, levels = (np.logspace(1,1.75,50))*0.0048-0.043)
	#cs = plt.contourf(IR, mass[0], intensity.T - 0.005, levels = (np.logspace(0.1,0.23,50)) - 10**0.1)
	plt.ylim(0,250)
	cb = plt.colorbar(cs, orientation='vertical')
	cb.set_label('intensity')
	#plt.show()
	pylab.savefig(save_file, format='png', dpi=100)
	plt.clf()

def plot_mass_spectrum_smooth(mass, intensity, mass_range, save_file, smooth):
	#plt.close('all')
	fig = plt.figure()
	ax1=fig.add_subplot(111)
	#ax1.plot(mass, intensity, 'k-')
	ax1.plot(mass, runningMeanFast(intensity,smooth), 'k-')
	ax1.set_xlabel('Mass/Charge (Da)')
	ax1.set_ylabel('Intensity (V)')
	ax1.set_xlim(mass_range)
	#ax1.set_ylim([-0.005,0.065])
	ax1.xaxis.set_minor_locator(AutoMinorLocator(5))
	ax1.yaxis.set_minor_locator(AutoMinorLocator(2)) 
	#plt.show()
	pylab.savefig(save_file)
	plt.clf()


def plot_mass_spectrum_wavelength_with_IR(mass, intensity, IR, IR_file, IR_data, x_range, save_file):

	plt.figure(figsize=(8, 10), dpi=1000)
	plt.subplots_adjust(left=None, bottom=0.01, right=None, top=0.90, wspace=None, hspace=0.0)
	gs = gridspec.GridSpec(2, 1, height_ratios=[1, 3.5]) 
	
	ax1 = plt.subplot(gs[0])
	ax2=ax1.twiny()
	
	#IR plot
	for index, sample in enumerate(IR_file):
		#define key
		#take all characters after '/'
		key = sample.split('/',1)[-1]
		key=key.split('_', 1)[0]
		wavelength=np.array(IR_data[key+'_wavelength'])
		reflectance=np.array(IR_data[key+'_reflectance'])
		#scale IR spectrum reflectance (optional)
		#if index > 0:
			#reflectance = reflectance*2
		reflectance_smooth=scipy.signal.savgol_filter(reflectance, 21, 3)
		line, = ax1.plot(wavelength.T, reflectance_smooth.T)
		ax1.text(0.94, 0.84-(index*0.12), key, verticalalignment='bottom', horizontalalignment='right', transform=ax1.transAxes, color=line.get_color())
	
	#ax1.plot(IR_tryp_wavelength.T-0.00855064, tryp_smooth.T, 'b-')
	#ax1.plot(IR_epsomite_wavelength.T-0.00855064, epsomite_smooth.T, 'r-')
	ax1.set_xticklabels([])
	ax1.set_ylabel('Reflectance')
	#ax1.set_ylabel('Transmitance')
	ax1.set_xlim(x_range)
	#ax1.set_ylim([0,0.1])
	ax1.minorticks_on()
	ax1.locator_params(axis='y', nbins = 4)
	#ax2.set_xlabel('wavenumber (cm$^{-1}$)')
	##if x_range is in microns
	#ax2.set_xlim(1E4/np.array(x_range))
	#remove tick label and tick marks
	ax2.xaxis.set_major_formatter(plt.NullFormatter())
	for tic in ax2.xaxis.get_major_ticks():
		tic.tick1On = tic.tick2On = False
		tic.label1On = tic.label2On = False
	ax2=ax1.twiny()
	ax2.set_xlabel('wavenumber (cm$^{-1}$)')
	#array with values of tick mark locations
	#wavenumber labels multiple of 100 cm^-1
	wavenumber_label=[]
	wavenumber_location=[]
	for loc in range(int(1+(1E4/x_range[0] - 1E4/x_range[1])/100)):
		wavenumber=int((1E4/x_range[0]) - 100*loc)/100*100
		wavenumber_label.append(wavenumber)
		location= 1 - ((x_range[1] - 1E4/wavenumber)/(x_range[1] - x_range[0]))
		wavenumber_location.append(location)

	minor_locator=[]
	num_minor=len(wavenumber_location)*3
	for i in range(len(wavenumber_location)-1):
		diff=wavenumber_location[i+1]-wavenumber_location[i]
		for j in range(4):
			minor_locator.append((j+1) * (diff/4.0) + wavenumber_location[i])
	
	ax2.set_xticks(wavenumber_location)
	ax2.set_xticklabels(wavenumber_label)
	ax2.xaxis.set_minor_locator(plt.FixedLocator(minor_locator))

	#set up MS plot
	cmap=cm.get_cmap('jet')
	ax3 = plt.subplot(gs[1])
	ax3.minorticks_on()
	ax3.set_axis_bgcolor('black')
	plt.xlabel('IR desorption wavelength (nm)')
	#ax3.spines['bottom'].set_color('white')
	#ax3.spines['top'].set_color('white')
	#ax3.spines['right'].set_color('white')
	#ax3.spines['left'].set_color('white')
	for t in ax3.xaxis.get_ticklines(): t.set_color('white')
	for t in ax3.xaxis.get_minorticklines(): t.set_color('white')
	for t in ax3.yaxis.get_ticklines(): t.set_color('white')
	for t in ax3.yaxis.get_minorticklines(): t.set_color('white')
	plt.ylabel('mass/charge (Da)')
	plt.yticks(np.arange(0, 250, 50))
	
	#plot MS data and colorbar
	#if data is within 1 std, set to 0
	#threshold = intensity.std()
	#for i in range(0, len(intensity)):
		#for j in range(0, len(intensity.T)):
			#if abs(intensity[i,j]) <= threshold:
				#intensity[i,j] = -5

	cs = plt.contourf(IR, mass[0], intensity.T-0.00, levels = (np.linspace(0, intensity.max(), 200)))
	plt.ylim(0,250)
	#cs.set_clim([0, intensity.max()])
	cb = plt.colorbar(cs, ax=ax3, orientation='horizontal')
	cb.set_ticks([0, intensity.max()/4, intensity.max()/2, intensity.max()*3/4, intensity.max()])
	cb.ax.minorticks_on()
	#cb.set_label('intensity')
	plt.savefig(save_file, format='png', dpi=100)
	plt.clf()

