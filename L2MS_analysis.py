#import relevant libraries
import numpy as np
import sys
import operator

#########################################################
#function definitions:

#read in MS data
#store data in array
def read_data_files(data_path, filename, dict_mass, dict_intensity):
	#open filename (list of data files)
	filelist=open(filename,'r')
	#for each data file in the .txt list:
	for file in filelist:
		#temporary variable to hold the mass values
		mass=[]
		#temporary varibale to hold the intensity values
		intensity=[]
		file=open(data_path+file.rstrip('\n'),'r')
		#there is some extra formatting on the first line - delete this data
		header=file.readline()
		#read each row in the file
		for line in file:
			#read each row - store data in columns
			columns=line.split()
			mass.append(float(columns[0]))
			intensity.append(float(columns[1]))
		#save mass and intensity data to dictionary
		dict_mass.append(mass)
		dict_intensity.append(intensity)

#read IR data
def read_IR_data(filename, dict_wavelength, dict_reflectance):
	#open filename
	file=open(filename,'r')
	#header=file.readline()
	wavelength=[]
	reflectance=[]
	for line in file:
		columns=line.split()
		#needed for NIST spectra
		columns[0]=columns[0].rstrip(',')
		wavelength.append(float(columns[0]))
		reflectance.append(float(columns[1]))
	dict_wavelength.append(wavelength)
	dict_reflectance.append(reflectance)

#IR wavelength identification
def IR_wavelength(filename, IR):
	filelist=open(filename,'r')
	for file in filelist:
		#save IR wavelength in temporary variable
		IR_temp=file[0:4]
		#save IR wavelength value to IR array
		IR.append(float(IR_temp))

#temperature value identification
def temperature_id(filename, temperature):
	filelist=open(filename,'r')
	for file in filelist:
		#save temperature value to temporary variable

		#if file format is: nnnn_-tt.t.txt
		temp_temp=file[5:]
		#if file format is: nnnn_n.nmJ_-tt.t.txt
		#temp_temp=file[11:]

		temp_temp=temp_temp.rstrip('.txt\n')
		#save temperature value to IR array
		temperature.append(float(temp_temp))

#temperature value identification
def time_id(filename, time):
	filelist=open(filename,'r')
	for file in filelist:
		#save temperature value to temporary variable

		#if file format is: nnnn_-tt.t.txt
		temp_time=file[6]
		#if file format is: nnnn_n.nmJ_-tt.t.txt
		#temp_temp=file[11:]

		#temp_temp=temp_temp.rstrip('.txt\n')
		#save temperature value to IR array
		time.append(float(temp_time))

#standard deviation calculation
def std_values(mass, intensity, noise_std, mass_range):
	for i in range(len(mass)):
		#temporary variabile to hold the std value
		temp_std=[]
		#find index associated with mass_range[0]
		std_low=next(idx for idx, v in enumerate(mass[i]) if v >= mass_range[0])
		#find index associated with mass_range[1]
		std_high=next(idx for idx, v in enumerate(mass[i]) if v >= mass_range[1])
		#calculate std of range
		temp_std = np.std(intensity[i][std_low:std_high])
		noise_std.append(temp_std)

#integrated peak value calculation
def peak_value(mass, intensity, peak_value, peak_center, peak_width):
	for i in range(len(mass)):
		#temporary variable to hold the integrated peak values
		peak_temp=[]
		#search for the index associated with the low and high ends of the peak
		index_low=next(idx for idx, v in enumerate(mass[i][:]) if v > (peak_center-(peak_width/2.0)))
		index_high=next(idx for idx, v in enumerate(mass[i][:]) if v > (peak_center+(peak_width/2.0)))
		
		#subtract median from intensity (shift bias)
		peak_temp = sum((intensity[i][index_low:index_high]) - np.median(intensity[i][:])) * ((mass[i][index_high] - mass[i][index_low]) / (index_high-index_low))
		peak_value.append(peak_temp)

#integrated peak value calculation calculating FWHM
#int_frac is the fraction of the peak to include (0.5 is FWHM)
#int_frac must be a float between 0 and 1
def peak_value_FWHM(mass, intensity, peak_value, peak_center, peak_width, int_frac):
	for i in range(len(mass)):
		#temporary variable to hold the integrated peak values
		peak_temp=[]
		#search for the index associated with the low and high ends of the peak
		# the peak of interest must be the dominant peak in this range
		index_low=next(idx for idx, v in enumerate(mass[i][:]) if v > (peak_center-(peak_width/2.0)))
		index_high=next(idx for idx, v in enumerate(mass[i][:]) if v > (peak_center+(peak_width/2.0)))
		
		#offset data by median value (bias shift)
		intensity[i][index_low:index_high] = intensity[i][index_low:index_high] - np.median(intensity[i][:])

		#locate peak index value (within low-high range)
		peak_index = intensity[i].index(max(intensity[i][index_low:index_high]))

		#find idicies associated with FWHM (within low-high range)
		#low index is the first index greater than half the peak value				
		FWHM_low = next(idx for idx, v in enumerate(intensity[i][index_low:index_high]) if v >= max(intensity[i][index_low:index_high])*(1.0-int_frac))
		FWHM_low = FWHM_low+index_low
		#high index is the first index less than half the peak value
		#(start counting from peak value)
		FWHM_high = next(idx for idx, v in enumerate(intensity[i][peak_index:index_high]) if v <= max(intensity[i][index_low:index_high])*(1.0-int_frac))
		FWHM_high = FWHM_high+peak_index
		
		#print index_low, FWHM_low, peak_index, FWHM_high, index_high
		#print 'index vaues: ', FWHM_high - FWHM_low
		#print mass[i][index_low], mass[i][FWHM_low], mass[i][peak_index], mass[i][FWHM_high], mass[i][index_high]
		#print intensity[i][index_low], intensity[i][FWHM_low], intensity[i][peak_index], intensity[i][FWHM_high], intensity[i][index_high]

		#calculate integrated peak value
		#use composite trapezoidal rule for discrete numerical integration
		#trapz_int - intensity values within range
		trapz_int = intensity[i][FWHM_low:FWHM_high]
		#trapz_mass - mass values within range
		trapz_mass = mass[i][FWHM_low:FWHM_high]
		#integrated peak returns one element list
		peak_temp = np.trapz(trapz_int, x=[trapz_mass])
		peak_temp=peak_temp[0]
		print 'integrated peak at FWHM: ', peak_temp
		#to compare with conventional integration
		#print sum(intensity[i][FWHM_low:FWHM_high]) * ((mass[i][FWHM_high] - mass[i][FWHM_low])/(FWHM_high-FWHM_low))
		peak_value.append(peak_temp)
		#reset intensity values for plotting
		intensity[i][index_low:index_high] = intensity[i][index_low:index_high] + np.median(intensity[i][:])

#max peak value calculation
def max_peak_value(mass, intensity, peak_value, peak_center, peak_width):
	for i in range(len(mass)):
		#temporary variable to hold the integrated peak values
		peak_temp=[]
		#search for the index associated with the low and high ends of the peak
		index_low=next(idx for idx, v in enumerate(mass[i][:]) if v > (peak_center-(peak_width/2.0)))
		index_high=next(idx for idx, v in enumerate(mass[i][:]) if v > (peak_center+(peak_width/2.0)))
		
		#subtract median from intensity (shift bias)
		peak_temp = max(intensity[i][index_low:index_high]) - np.median(intensity[i][:])
		peak_value.append(peak_temp)


def max_peak_location(mass, intensity, peak_approx, peak_width):
	#temporary variable to hold the peak values
	peak_temp=[]
	#search for the index associated with the low and high ends of the peak
	index_low=next(idx for idx, v in enumerate(mass) if v > (peak_approx-(peak_width/2.0)))
	index_high=next(idx for idx, v in enumerate(mass) if v > (peak_approx+(peak_width/2.0)))

	#identify index of maximum value in range
	peak_index, peak_value = max(enumerate(intensity[index_low:index_high]), key=operator.itemgetter(1))

	return mass[index_low+peak_index]

def max_peak_locations(mass, intensity, peak_approx, peak_width, peak_location):
	for i in range(len(peak_approx)):
		#temporary variable to hold the peak values
		peak_temp=[]
		#search for the index associated with the low and high ends of the peak
		index_low=next(idx for idx, v in enumerate(mass) if v > (peak_approx[i]-(peak_width[i]/2.0)))
		index_high=next(idx for idx, v in enumerate(mass) if v > (peak_approx[i]+(peak_width[i]/2.0)))

		#identify index of maximum value in range
		peak_index, peak_value = max(enumerate(intensity[index_low:index_high]), key=operator.itemgetter(1))

		peak_location.append(mass[index_low+peak_index])
		#return mass[index_low+peak_index]
