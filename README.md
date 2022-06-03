# PRM
Code for simulations and visualisations of the Population Rate Model containing PYR, CCK, PV and BiC cell populations.

## cell.py
Contains the parameters and initialises the population rate model with the parameters outlined in the Methods section.

## icck-ipv.py 
Performs the simulations of the population rate model and creates visualisations for the theta and gamma frequency and power with changing $i_{cck}$ and $i_{pv}$ parameters. 

## lfp_spectrogram.py
Plots the LFP trace for simulations of the Full Scale Model as well as computes the Welch's Periodogram of the LFP. It also contains the option to filter the LFP within the theta or gamma frequency band. The same code is used to compute the power for the visualisations of the theta or gamma power for the simulations of the PRM

## spikeraster.py
Plots the spike raster that displays the spiking for each cell, grouped by cell type, for simulations of the FSM. 
