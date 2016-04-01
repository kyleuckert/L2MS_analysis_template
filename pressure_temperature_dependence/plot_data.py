import sys
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import pylab

path='/Users/kyleuckert/Documents/Research/MS/Analysis/2015JUL10/1000ppm_epsomite_tryp_in_methanol/pressure_temperature_dependence/'

file=open(path+'data.txt','r')
header=file.readline()
#data=[]
time=[]
pressure=[]
temperature=[]
#LN2=[]
for line in file:
	columns=line.split()
	time.append(float(columns[0][0:2]) + ((float(columns[0][2:4]))/60.0))
	pressure.append(float(columns[1]))
	temperature.append(float(columns[2]))
	#LN2.append(int(columns[3]))

pressure_plot=np.array(pressure)
pressure_plot=pressure_plot*1E5


fig, ax1=plt.subplots()

#p = plt.axvspan(14.18, 14.27, facecolor='g', alpha=0.5)
#ax1.axvline(12.92, color='k', linestyle='-')

ax1.plot(time, pressure_plot, 'b.')
ax1.plot(time, pressure_plot, 'b-')
ax1.set_xlabel('time (hours on July 10, 2015)')
# Make the y-axis label and tick labels match the line color.
ax1.set_ylabel('Pressure (10$^{-5}$ torr)', color='b')
ax1.minorticks_on()
ax1.tick_params(axis='y', colors='b')
ax1.spines['left'].set_color('b')
for t in ax1.yaxis.get_minorticklines():
	t.set_color('b')

ax2 = ax1.twinx()
ax2.plot(time, temperature, 'r.')
ax2.plot(time, temperature, 'r-')
ax2.set_ylabel('Temperature ($^{\circ}$C)', color='r')
ax2.minorticks_on()
ax2.tick_params(axis='y', colors='r')
ax2.spines['right'].set_color('r')
for t in ax2.yaxis.get_minorticklines():
	t.set_color('r')


#plt.show()
pylab.savefig('epsomite_tryptophan_in_methanol.png', format='png', dpi=100)
plt.clf()