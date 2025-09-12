from kmcos.run import KMC_Model
import random

# Model parameters
Ts = [350, 450]  # Growth temperatures
kads = 3e-3  # Rate constant for adsorption
size = (30, 30, 30)  # Size of simulation box
targetML = 5.0  # Stop the growth after the target number of layers have been reached

nsteps = 100  # Number of steps to run in each iteration

for i, T in enumerate(Ts):
    random_seed = random.random() * 1e12
    model = KMC_Model(banner=False, size=size, random_seed=random_seed)
    #add put command to place the substrate atoms :   model.put(site=[x,y,z,n], model.proclist.<species>)
    for i in range(size[0]):
        for j in range(size[1]):
            model._put([i,j,0,1],2)
    model._adjust_database()
    model.parameters.T = T
    model.parameters.kads = kads
    tsim = 0.0
    ML = 0.0
    while ML < targetML:
        model.do_steps(nsteps)
        at = model.get_atoms(geometry=False)
        # Convert TOF into ML growth
        ML += at.tof_data[model.tofs.index("Growth")] * at.delta_t * size[2]
    outname = "_".join(
        ["config", "T{}".format(T)] + ["{}".format(d) for d in model.size]
    )
    model.dump_config(outname)  # Save current configuration for visualization
    print("Finished with T={}K".format(T))
    print("Deposited {}ML in {} s".format(ML, model.base.get_kmc_time()))

    model.deallocate()
