from cairo import FONT_WEIGHT_BOLD
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 14})

import os
from itertools import (takewhile,repeat)

def rawincount(filename):
    f = open(filename, 'rb')
    bufgen = takewhile(lambda x: x, (f.raw.read(1024*1024) for _ in repeat(None)))
    return sum( buf.count(b'\n') for buf in bufgen )
    

run_name = 'stim_06_conn_5103_bez_sca'

fname = './Data/{}/spikeraster.dat'.format(run_name)
savedir = './Figures/SimTracker/{}/'.format(run_name)

try:
    os.mkdir(savedir)
except FileExistsError:
    pass
    
cell_range = {
    'PYR': [21310, 332809],
    'BiC': [1470, 3679],
    'PV': [332810, 338339],
    'CCK': [3680, 7279],
    'OLM': [19670, 21309],
    'AAC': [0, 1469],
    'NGF': [16090, 19669],
    'IVY': [7280, 16089],
    'SCA': [338340, 338739],
    'ca3': [338740, 543439],
    'ecc': [543440, 793439],
    'ca3rip': [793440, 813909],
    'onc': [813910, 834379],
}

color_dict = {
    'PYR': '#1f77b4',
    'BiC': '#ff7f0e',
    'PV': '#d62728',
    'CCK': '#2ca02c',
    'OLM': '#7f7f7f',
    'AAC': '#7f7f7f',
    'NGF': '#7f7f7f',
    'IVY': '#7f7f7f',
    'SCA': '#7f7f7f',
    'ca3': '#7f7f7f',
    'ecc': '#7f7f7f',
    'ca3rip': '#7f7f7f',
    'onc': '#7f7f7f',
}

base_height = 2

height_ratio = []

for cell in cell_range:
    ht = base_height * (cell_range[cell][1] - cell_range[cell][0]) / (cell_range['IVY'][1] - cell_range['IVY'][0])
    height_ratio.append(max(0.8, min(3, ht)))
    
DATA = np.loadtxt(fname)
print('Completed loading file:', fname)

fig, ax = plt.subplots(9, 1,  figsize = [16, 9], gridspec_kw = {'height_ratios': height_ratio[:9]}, dpi = 400, sharex=True)

tstart, tend = 3700, 4000 

#flines = rawincount(fname)

#chunk = 100000
#start, end = 0, chunk


i = 0
for cell_to_plot in [*cell_range][:9]:
    to_plot = tuple([(DATA[:, 1] >= cell_range[cell_to_plot][0]) & (DATA[:, 1] <= cell_range[cell_to_plot][1])])
    ax[i].plot(DATA[:, 0][to_plot], DATA[:, 1][to_plot], '.', color = color_dict[cell_to_plot], markersize = 0.3)
    ax[i].set_ylim(cell_range[cell_to_plot])
    ax[i].set_xlim([tstart, tend])
    ax[i].set_yticks([])
    ax[i].set_ylabel(cell_to_plot, fontweight = 'bold')
    plt.rcParams.update({'font.size': 16})
    plt.xlabel('Time (ms)')
    # plt.tight_layout()
    print('Completed for cell type: ', i+1)
    i += 1	
    
plt.savefig(savedir + 'spikeraster_{}_{}_ms_colour.png'.format(str(tstart), str(tend)), bbox_inches = 'tight')
#plt.savefig(savedir + 'spikeraster.png', bbox_inches = 'tight')
plt.close()

