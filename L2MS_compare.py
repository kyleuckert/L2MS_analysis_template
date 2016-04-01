#import relevant libraries
import L2MS_plot
import L2MS_analysis
import os
import numpy as np
import sys
import matplotlib
import matplotlib.pyplot as plt
import pylab
from matplotlib.ticker import AutoMinorLocator


#define paths
data_pathDOM21 = '/Users/kyleuckert/Documents/Research/MS/Data/2015AUG21/DOM03183/-100C/'
data_pathDOM27 = '/Users/kyleuckert/Documents/Research/MS/Data/2015AUG27/DOM03183/-100C/'
analysis_path='/Users/kyleuckert/Documents/Research/MS/Analysis/2015AUG26/tryptophan/'

filename21=['2820.txt']
filename27=['2820.txt']

data={}
data['21_mass']=[]
data['21_intensity']=[]
data['27_mass']=[]
data['27_intensity']=[]

file=open(data_pathDOM21+filename21[0],'r')
mass=[]
intensity=[]
header=file.readline()
for line in file:
	#read each row - store data in columns
	columns=line.split()
	mass.append(float(columns[0]))
	intensity.append(float(columns[1]))
#save mass and intensity data to dictionary
data['21_mass'].append(mass)
data['21_intensity'].append(intensity)

file=open(data_pathDOM27+filename27[0],'r')
mass=[]
intensity=[]
header=file.readline()
for line in file:
	#read each row - store data in columns
	columns=line.split()
	mass.append(float(columns[0]))
	intensity.append(float(columns[1]))
#save mass and intensity data to dictionary
data['27_mass'].append(mass)
data['27_intensity'].append(intensity)


#plot data
fig = plt.figure(dpi=200)
ax1=fig.add_subplot(111)
ax1.plot(data['21_mass'][0], data['21_intensity'][0], 'r-', data['27_mass'][0], data['27_intensity'][0], 'b-')
ax1.set_xlabel('Mass/Charge (Da)')
ax1.set_ylabel('Intensity (mV)')
ax1.text(0.94, 0.92, 'August 21: 0.8mJ', verticalalignment='bottom', horizontalalignment='right', transform=ax1.transAxes, color='r')
ax1.text(0.94, 0.84, 'August 27: 0.45mJ', verticalalignment='bottom', horizontalalignment='right', transform=ax1.transAxes, color='b')
ax1.set_xlim([0,300])
#ax1.set_title('tryptophan: 2820 nm')
ax1.xaxis.set_minor_locator(AutoMinorLocator(5))
ax1.yaxis.set_minor_locator(AutoMinorLocator(2)) 
#plt.show()
pylab.savefig('DOM03183_AUG21_AUG27_2820nm.png', dpi=200)
plt.clf()

fig = plt.figure(dpi=200)
ax1=fig.add_subplot(111)
ax1.plot(data['27_mass'][0], data['27_intensity'][0], 'b-', data['21_mass'][0], [x+0.15 for x in data['21_intensity'][0]], 'r-')
ax1.set_xlabel('Mass/Charge (Da)')
ax1.set_ylabel('Intensity (mV)')
ax1.text(0.94, 0.92, 'August 21: 0.8mJ', verticalalignment='bottom', horizontalalignment='right', transform=ax1.transAxes, color='r')
ax1.text(0.94, 0.84, 'August 27: 0.45mJ', verticalalignment='bottom', horizontalalignment='right', transform=ax1.transAxes, color='b')
ax1.set_xlim([0,300])
#ax1.set_title('tryptophan: 2935 nm')
ax1.xaxis.set_minor_locator(AutoMinorLocator(5))
ax1.yaxis.set_minor_locator(AutoMinorLocator(2)) 
#plt.show()
pylab.savefig('DOM03183_AUG21_AUG27_2820nm_offset.png', dpi=200)
plt.clf()
