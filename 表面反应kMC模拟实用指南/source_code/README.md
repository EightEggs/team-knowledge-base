# KMCOS Python Scripts for A Practical Guide to Surface Kinetic Monte Carlo Simulations

> ref: Andersen M, Panosetti C and Reuter K (2019) A Practical Guide to Surface Kinetic Monte Carlo Simulations. Front. Chem. 7:202. [doi: 10.3389/fchem.2019.00202](https://doi.org/10.3389/fchem.2019.00202)

## Au100_diffusion

Adatom diffusion on Au(100) model discussed in Section 5.1.

In the top of the script various model parameters are defined. Try to vary the parameter “conc” to see how the concentration of particles on the lattice influences the diffusion constant. The parameter “Nruns” defined the number of trajectories to average over. 

Try to decrease the value and observe how the statistical error on the diffusion constant increases (e.g. calculate the mean and the standard error of the mean). You can also try to play around with the barriers for hopping and exchange diffusion defined a bit further down in the script.

## COoxRuO2

CO oxidation on RuO2(110) model with and without lateral interactions discussed in Section 6.1 and 9.1.

In the top of the script various model parameters are defined. You can for example change how the lattice should be initialized, i.e. which species to add to the cus sites, through the “species” parameter. 

You can also modify the script further to make your own custom initialization. Finally, you can try to change the temperature as well as the partial pressures of CO and O2.

## SOSadsdes

Solid-on-solid crystal growth model discussed in Section 9.1.

In the top of the script various model parameters are defined. Try to change the growth temperature, the rate constant for adsorption, the size of the simulation box as well as the target number of layers to grow. 

Hint: Make sure that the grown structure does not extend beyond the size of the simulation box, or you will encounter an error. You can use the “view_SOSadsdes.py” to visualize the grown structures.
