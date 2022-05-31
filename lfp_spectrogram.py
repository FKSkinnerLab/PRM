import numpy as np
from scipy.signal import welch, find_peaks, butter, filtfilt
import matplotlib.pyplot as plt
import os
plt.rcParams.update({'font.size': 14}) 

def bandPassFilter(data, cutoff, fs, order=3):
    #nyquist frequency
    nyq = 0.5 * fs
    band = cutoff / nyq
    b, a = butter(order, band, btype = 'band', analog = False)
    y = filtfilt(b, a, data)
    return y

def highPassFilter(data, cutoff, fs, order=3):
    #nyquist frequency
    nyq = 0.5 * fs
    high = cutoff / nyq
    b, a = butter(order, high, btype = 'high', analog = False)
    y = filtfilt(b, a, data)
    return y
    
run_name = 'Alexandra_loquat/Sc1_SimD4000_DegSt065_70nodes_conn1074_cellnum101_syn120'
fname = './Data/{}/lfp.dat'.format(run_name)
savedir = './Figures/Alexandra_Paper_Figures_2/{}/'.format(run_name)

try:
    os.mkdir(savedir)
except FileExistsError:
    pass

lfp_data = np.loadtxt(fname)
# lfp_data[:, 1] /= 1000
a = fname.split('/')[-1].split('.')[0]
name = (' '.join(a.split('_'))).upper()

T = 4.0
dt = T / len(lfp_data[:, 0])
time = np.arange(0, T, dt)

Plot = True
Filter = False

if Plot:
    plt.figure(figsize = [4, 3], dpi=400)
    plt.plot(time, lfp_data[:, 1], linewidth = 0.5)
    #plt.xlim([3.0, 3.5])
    # plt.xlabel('Time ($s$)')
    plt.xlabel('Time')
    # plt.ylabel('LFP ($mV$)')
    plt.ylabel('LFP')
    # plt.title('{}'.format(name))
    plt.savefig(savedir + 'lfp.png', bbox_inches = 'tight')
    #plt.savefig(savedir + 'lfp_blowup.png', bbox_inches = 'tight')
if Filter:
	cutoff = np.array([3.0, 20.0])    

	filtered_lfp = bandPassFilter(lfp_data[:, 1], cutoff, 1/dt)
	if Plot:
	    plt.figure(figsize = [4, 3], dpi=400)
	    plt.plot(time, filtered_lfp, linewidth = 0.5)
	    plt.xlabel('Time (s)')
	    plt.ylabel('LFP ($mV$)')
	    plt.title('{} filtered'.format(name))
	    plt.savefig(savedir + 'lfp_filtered.png', bbox_inches = 'tight')

	freq, lfp_spectral = welch(filtered_lfp, 1/dt, nperseg = 2e4)
	plt.figure(figsize = [4, 3], dpi=400)
	plt.plot(freq, lfp_spectral, linewidth = 0.5)
	plt.xlabel('Frequency ($Hz$)')
	plt.ylabel('Power ($mV^2/Hz$)')
	plt.xlim(0, 100)
	plt.title('LFP Spectrogram\nPeak Freq = {}'.format(str(freq[np.argmax(lfp_spectral)].round(2))))
	plt.savefig(savedir + 'lfp_spectral_filtered.png', bbox_inches = 'tight')

else:
    freq, lfp_spectral = welch(lfp_data[:,1], 1/dt, nperseg = 2e4)
    plt.figure(figsize = [4, 3], dpi=400)
    plt.plot(freq, lfp_spectral, linewidth = 0.5)
    # plt.xlabel('Frequency ($Hz$)')
    # plt.ylabel('Power ($mV^2/Hz$)')
    plt.xlabel('Frequency')
    plt.ylabel('PSD')
    plt.xlim(0, 100)
    # plt.title('LFP Spectrogram\nPeak Freq = {}'.format(str(freq[np.argmax(lfp_spectral)].round(2))))
    plt.savefig(savedir + 'lfp_spectral_unfiltered.png', bbox_inches = 'tight')
	
print(freq[np.argmax(lfp_spectral)])


