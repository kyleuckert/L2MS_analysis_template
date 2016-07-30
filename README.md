# L2MS analysis template
<b>Description:</b><br>
<p>
These programs will plot L2MS mass spectrometry data, including intensity vs mass plots and intensity vs mass vs wavelength plots
</p>

<b>Instructions:</b><br>
<p>
<i>Define File Names:</i>
<ul>
<li>Open "L2MS_main.py"</li>
<li>Define data, analysis, and IR spectra path variables (lines 9-12)</li>
<ul><li>IR spectra data path variable may have multiple paths</li></ul></ul></p>
	data_path = '/path/to/data/enstatite_tryptophan_1000ppm_room_temp/'
	analysis_path='/path/to/analysis/enstatite_tryptophan_1000ppm_room_temp/'
	IR_data_path=['/path/to/IR/spectra/MS/NIST_IR_spectra/']

<p><ul>
<li>Autonomously create a list of data files (lines 14-20)</li>
<ul><li>Run "L2MS.main.py" (type "python L2MS_main.py" on the command line within the analysis directory)</li>
<li>A list of all data files located in "data_path" will be stored in "filenames.txt" in the analysis directory</li>
<li>Comment out lines 19-20 (add # at the start of the line) of "L2MS_main.py"</li>
<li>Create new file lists (e.g. "filenames_IR.txt" for a series of mass spectra at different IR wavelengths, "filenames_temp_2935.txt" for mass spectra at the same IR wavelength at different temperatures)</li>
<li>Add these files to the "file_list" list (line 26)</li></ul>
</ul></p>

<p>
<i>Read Meta Data from Filenames:</i>
<ul>
<li>Obtain IR wavelength values (line 44)</li>
<ul><li>Change the index of "file_list" to the index corresponding to the wavelength variable mass spectra array</li>
<li>File name format (first four digits correspond to wavelength in nm):</li></ul></ul></p>
		"####.txt"

<p><ul>
<li>Obtain temperature values (line 49)</li>
<ul><li>Change the index of "file_list" to the index corresponding to the temperature variable mass spectra array</li>
<li>File name format (the temperature ID corresponds to everything after "wwww_"):</li></ul></ul></p>
		"wwww_-tt.t.txt"

<p>
<i>Calculate the standard deviation of the spectrum noise (line 57-67):</i>
<ul>
<li>Define "mass_range" to reflect a mass range with no strong peaks near the peak of interest</li>
</ul></p>
	mass_range = [low_mass_range_value, high_mass_range_value]

<p>
<i>Calculate the integrated peak value (line 71-95):</i>
<ul>
<li>Define the approximate central peak value ("peak_center"), the mass range enclosing the max peak value ("peak_width"), and the boundary of the peak area calculation ("int_frac"), where "int_frac = 0.5" corresponds to the FWHM of the peak</li>
<li>For the example below, the program will search for the maximum peak between 125-130 Da, and integrate the area bounded by mass values associated with 90% on the peak intensity on eaither side of the peak (i.e. 129.3-130.7 Da)</li>
</ul></p>
	peak_center=130
	peak_width=10
	int_frac=0.9

<p>
<i>Calculate the maximum peak value (line 97-111):</i>
<ul>
<li>Define the approximate central peak value ("peak_center") and the mass range enclosing the max peak value ("peak_width")</li>
<li>For the example below, the program will return the maximum peak value between 128-132 Da</li>
</ul></p>
	peak_center=130
	peak_width=4

<p>
<i>Calculate the signal-to-noise ratio (SNR) for a given peak (line 115-116):</i>
<ul>
<li>The SNR is calculated on line 115. To change the peak location of the SNR, edit the "peak_center" variable (line 98) and the "mass_range" variable (line 59)</li>
<li>Uncomment line 116 to print SNR calculation</li>
</ul></p>

<p>
<i>Print the location of the tallest peaks (line 124-132):</i>
<ul>
<li>Define the "peak_approx" and "peak_range" lists to include the approximate locations of the peaks, and the mass range to search for the maximum value.</li>
</ul></p>
	peak_approx = [peak1, peak2, peak3]
	peak_range =[range1, range2, range3]

<p>
<i>Read IR data (line 134-151):</i>
<ul>
<li>Input the name of the IR spectrum (or spectra) to be read (line 135)</li>
<ul><li>Multiple IR filenames require multiple IR paths (line 11)</li>
<li>The index of each file corresponds to the index of the path</li></ul>
<li>IR spectra should be formatted as 2 columns (wavelength, reflectance), separated by a space, tab, or comma</li>
</ul></p>
	IR_file=['IR_file_name_1.txt', 'IR_file_name_2.txt']

<i>Plot Data:</i>
<p>
<ul>
<b>Plot IR spectrum (spectra) (line 170-177):</b>
<li>Edit the following template (and place after line 152) with the following required input parameters:</li>
<ul>
<li>IR specturm index value for key=key.split('_', 1)[index] (from line 135, counting starts at index 0)</li>
<li>x axis range ([wavelength_min, wavelength_max])</li>
<li>plot title (str(key)+' IR spectrum')</li>
<li>save file name (str(key)+'_IR_spectrum.png')</li>
</ul></ul></p>
	for filename in IR_file:
		key = filename.split('/',1)[-1]
		key=key.split('_', 1)[index]
		L2MS_plot.plot_IR_spectrum(np.array(IR_data[key+'_wavelength']), np.array(IR_data[key+'_reflectance']), [wavelength_min, wavelength_max], str(key)+' IR spectrum', str(key)+'_IR_spectrum.png')

<p><ul>
<b>Plot individual mass spectrum (line 185-186):</b>
<li>Edit the following template (and place after line 152) with the following required input parameters:</li>
<ul>
<li>mass specturm index value (from .txt file list, counting starts at index 0)</li>
<li>x axis range ([mass_min, mass_max])</li>
<li>save file name</li>
</ul></ul></p>
	L2MS_plot.plot_mass_spectrum(np.array(data['IR_mass'][index]), np.array(data['IR_intensity'][index]), [mass_min, mass_max], 'mass_spectrum_file1.png')

<p><ul>
<b>Plot mass spectra vs wavelength (line 182-183):</b>
<li>Edit the following template (and place after line 152) with the following required input parameters:</li>
<ul>
<li>dictionary key value for mass and intensity arrays (key='IR_mass'; key='IR_intensity', end of string in .txt file: 'filenames_IR.txt')</li>
<li>IR filename (for annotation)</li>
<li>IR data dictionary (IR_data)</li>
<li>x axis range ([mass_min, mass_max])</li>
<li>save file name</li>
</ul></ul></p>
	L2MS_plot.plot_mass_spectrum_wavelength_with_IR(np.array(data['IR_mass']), np.array(data['IR_intensity']), np.array(IR), IR_file, IR_data, [mass_min, mass_max], 'mass_spectra_IR_dependence_file1.png')

<p><ul>
<b>Plot peak value vs wavelength (line 179-180):</b>
<li>Edit the following template (and place after line 152) with the following required input parameters:</li>
<ul>
<li>dictionary key value (key='IR', end of string in .txt file: 'filenames_IR.txt')</li>
<li>plot title ('' for no title)</li>
<li>save file name</li>
</ul></ul></p>
	L2MS_plot.plot_peak_vs_IR(peak130['IR'], IR, 'plot title', 'peak_vs_IR_file1.png')

<p><ul>
<b>Plot peak value vs temperature at a specific wavelength (line 158-160):</b>
<li>Edit the following template (and place after line 152) with the following required input parameters:</li>
<ul>
<li>dictionary key value (key='temp_2935', end of string in .txt file: 'filenames_temp_2935.txt')</li>
<li>plot title ('' for no title)</li>
<li>save file name</li>
</ul></ul></p>
	L2MS_plot.plot_peak_vs_T(peak130[key], temp[key], 'plot title', 'int_peak_vs_temp_file1.png')

<p><ul>
<b>Plot peak value vs concentration of analyte (line 162-167):</b>
<li>Edit the following template (and place after line 152) with the following required input parameters:</li>
<ul>
<li>define concentration series (e.g. concentration = [1000, 100, 10] in ppm)</li>
<li>dictionary key value (key='breadboard', end of string in .txt file: 'filenames_breadboard.txt')</li>
<li>plot title ('' for no title)</li>
<li>save file name</li>
</ul></ul></p>
	concentration = [high_con, med_con, low_con]
	L2MS_plot.plot_peak_vs_concentration(peak180[breadboard], concentration, 'plot title', 'peak_value_vs_concentration_file1.png')

<p><ul>
<b>Annotate, Compare, and/or offset mass spectra (line > 200):</b>
<li>The templates after line 200 demonstrate how to plot mass spectra in a more customizable way (e.g. compare two mass spectra, offset mass spectra, plot on a log scale).</li>
<li>Edit the templates (and place after line 152) with the the following required input parameters:</li>
<ul>
<li>dictionary key value (key='breadboard', end of string in .txt file: 'filenames_breadboard.txt')</li>
<li>mass specturm index value (from .txt file list, counting starts at index 0)</li>
<li>offset value</li>
<li>mass spectra colors and linestyles (b- produces a solid blue line, r. produces a dotted red line, etc)</li>
</ul></ul></p>
	ax1.plot(data['breadboard_mass'][index_1], [x+offset_1 for x in data['breadboard_intensity'][index_1]], 'b-', data['breadboard_mass'][index_2], [x+offset_2 for x in data['breadboard_intensity'][index_2]], 'r-', data['breadboard_mass'][index_3], data['breadboard_intensity'][index_3], 'g-')
<p><ul><ul>
<li>axis labels</li>
<li>x axis range ([mass_min, mass_max]) and or log scaling (ax1.set_yscale('log'))</li>
<li>save file name</li>
<li>annotations:</li>
</ul></ul></p>
	ax1.text(x_pos, y_pos, 'annotation text', verticalalignment='bottom', horizontalalignment='right', transform=ax1.transAxes, color='r')


<b>Installation:</b><br>
<p>
<ul>
<li>Install Python V2.7 using the <a href="http://continuum.io/downloads">Anaconda distribution</a>, which includes several useful scientific packages that will be necessary for the program to run.</li>
<li>Follow the installation instructions, select the default installation configuration.</li>
<li>Open the "Anaconda Command Prompt".</li>
<li>Type the following commands:</li></ul></p>
	conda install matplotlib
	conda install numpy
<p>
<ul>
<li>Download this github repository (<a href="https://github.com/kyleuckert/L2MS_analysis_template/archive/master.zip">Download ZIP button</a>) and place "IR_main.py", "IR_analysis.py", and "IR_plot.py" in the a directory that you would like the output files to be generated in.</li>
<li>Open "L2MS_main.py" in a text editor and edit the necessary lines described above</li>
<li>Run "L2MS_main.py" on the command line within the appropriate directory using the following command:</li>
</ul></p>
	python L2MS_main.py
