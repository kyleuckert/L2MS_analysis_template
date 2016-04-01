#import relevant libraries
import numpy as np
import sys

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
		#columns[0]=columns[0].rstrip(',')
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

#integrated peak value calculation
def peak_value(mass, intensity, peak_value, peak_center, peak_width):
	for i in range(len(mass)):
		#temporary variable to hold the integrated peak values
		peak_temp=[]
		#search for the index associated with the low and high ends of the peak
		index_low=next(idx for idx, v in enumerate(mass[i][:]) if v > (peak_center-(peak_width/2.0)))
		index_high=next(idx for idx, v in enumerate(mass[i][:]) if v > (peak_center+(peak_width/2.0)))
		
		#subtract median from intensity (shift bias)
		peak_temp = sum((intensity[i][index_low:index_high]) - np.median(intensity[i][:])) * (index_high-index_low) * (mass[i][index_high] - mass[i][index_low])
		peak_value.append(peak_temp)


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
