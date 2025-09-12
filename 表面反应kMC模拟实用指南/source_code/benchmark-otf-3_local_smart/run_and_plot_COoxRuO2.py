from kmcos.run import KMC_Model
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np

# Set up the plot
fig = plt.figure(figsize=(9.3, 6))
gs = gridspec.GridSpec(4, 4)
ax1 = plt.subplot(gs[0, 0])
ax2 = plt.subplot(gs[0, 1], sharey=ax1)
ax3 = plt.subplot(gs[0, 2], sharey=ax1)
ax4 = plt.subplot(gs[0, 3], sharey=ax1)
ax5 = plt.subplot(gs[1, 0], sharex=ax1)
ax6 = plt.subplot(gs[1, 1], sharex=ax2, sharey=ax5)
ax7 = plt.subplot(gs[1, 2], sharex=ax3, sharey=ax5)
ax8 = plt.subplot(gs[1, 3], sharex=ax4, sharey=ax5)
ax9 = plt.subplot(gs[2:, 0], sharex=ax1)
ax10 = plt.subplot(gs[2:, 1], sharex=ax2, sharey=ax9)
ax11 = plt.subplot(gs[2:, 2], sharex=ax3, sharey=ax9)
ax12 = plt.subplot(gs[2:, 3], sharex=ax4, sharey=ax9)

# Model parameters
species = ["empty", "o"]  # Species to add to cus sites in the initial state
colors = ["#0065bd", "#a2ad00", "#e37222", "#B452CD", "#dad7cb", "#000000", "r"]
ass_axes = [[ax1, ax5, ax9, ax2, ax6, ax10], [ax3, ax7, ax11, ax4, ax8, ax12]]

rerun = True  # If True rerun model, if False read previous results from files

Temp = 450  # Temperature in Kelvin
p_COgas = 1  # CO pressure in bar
p_O2gas = 1  # O2 pressure in bar

# Run and plot
plot_num = 1
for axes, init in zip(ass_axes, species):

    # Short timescale simulations
    if rerun:

        # load model
        model = KMC_Model(print_rates=False, banner=False)

        # set pressures and temperature
        model.parameters.T = Temp
        model.parameters.p_COgas = p_COgas
        model.parameters.p_O2gas = p_O2gas

        # prepare initial state
        if (
            init == "o"
        ):  # prepare initial state of system with all cus sites covered by O
            for i in range(model.size[0]):
                for j in range(model.size[1]):
                    model._put([i, j, 0, model.lattice.ruo2_cus], model.proclist.o)
            model._adjust_database()

        # get TOF labels
        tof_labels = model.get_tof_header().split(" ")

        # get coverage labels
        cov_labels = model.get_occupation_header().split(" ")

        # Number of kmc steps taken in each sample
        sample_step = 20

        # Number of samples
        N = 100

        # prepare arrays for TOFs, coverages and kmc steps
        tofs = np.zeros((N, len(tof_labels)))
        covs = np.zeros((N, len(cov_labels)))
        times = np.zeros((N, 1))

        # run model and save data
        for i in range(N):
            atoms = model.get_atoms(geometry=False)
            tof = atoms.tof_integ
            tofs[i, :] = tof
            cov = atoms.occupation
            covs[i, :] = cov.flatten()
            time = atoms.kmc_time
            times[i] = time
            model.do_steps(sample_step)

        np.savetxt("times_short_run%d.txt" % plot_num, times)
        np.savetxt("tofs_short_run%d.txt" % plot_num, tofs)
        np.savetxt("covs_short_run%d.txt" % plot_num, covs)

        # plot TOFs
        for i in range(len(tof_labels)):
            axes[0].plot(times * 1e9, tofs[:, i], color=colors[i], label="CO ox.")
            axes[1].plot(times * 1e9, tofs[:, i], color=colors[i], label="CO ox.")

    else:

        # load model
        model = KMC_Model(print_rates=False, banner=False)

        # get TOF labels
        tof_labels = model.get_tof_header().split(" ")

        # get coverage labels
        cov_labels = model.get_occupation_header().split(" ")

        model.deallocate()

        times = np.loadtxt("times_short_run%d.txt" % plot_num)
        tofs = np.loadtxt("tofs_short_run%d.txt" % plot_num)
        covs = np.loadtxt("covs_short_run%d.txt" % plot_num)
        # print times
        # print tofs

        # plot TOFs
        for i in range(len(tof_labels)):
            axes[0].plot(times * 1e9, tofs, color=colors[i], label="CO ox.")
            axes[1].plot(times * 1e9, tofs, color=colors[i], label="CO ox.")

    # plot covs
    for i in range(len(cov_labels)):
        axes[2].plot(
            times * 1e9,
            covs[:, i],
            color=colors[i],
            label=cov_labels[i]
            .replace("_ruo2", "")
            .replace("bridge", "br")
            .replace("empty", "*"),
        )

    # Long timescale simulations
    if rerun:

        # Number of kmc steps taken in each sample
        sample_step = 2e5

        # Number of samples
        N = 1000

        # prepare arrays for TOFs, coverages and kmc steps
        tofs = np.zeros((N, len(tof_labels)))
        covs = np.zeros((N, len(cov_labels)))
        times = np.zeros((N, 1))

        # run model and save data
        for i in range(N):
            atoms = model.get_atoms(geometry=False)
            tof = atoms.tof_integ
            tofs[i, :] = tof
            cov = atoms.occupation
            covs[i, :] = cov.flatten()
            time = atoms.kmc_time
            times[i] = time
            model.do_steps(sample_step)

        model.deallocate()

        np.savetxt("times_long_run%d.txt" % plot_num, times)
        np.savetxt("tofs_long_run%d.txt" % plot_num, tofs)
        np.savetxt("covs_long_run%d.txt" % plot_num, covs)

        # plot TOFs
        for i in range(len(tof_labels)):
            axes[3].plot(times, tofs[:, i], color=colors[i], label="CO ox.")
            axes[4].plot(times, tofs[:, i], color=colors[i], label="CO oxid.")

    else:
        times = np.loadtxt("times_long_run%d.txt" % plot_num)
        tofs = np.loadtxt("tofs_long_run%d.txt" % plot_num)
        covs = np.loadtxt("covs_long_run%d.txt" % plot_num)

        # plot TOFs
        for i in range(len(tof_labels)):
            axes[3].plot(times, tofs, color=colors[i], label="CO ox.")
            axes[4].plot(times, tofs, color=colors[i], label="CO oxid.")

    # plot covs
    for i in range(len(cov_labels)):
        axes[5].plot(
            times,
            covs[:, i],
            color=colors[i],
            label=cov_labels[i]
            .replace("_ruo2", "")
            .replace("bridge", "br")
            .replace("empty", "*"),
        )

    plot_num += 1

# adjust axis limits
ax1.set_ylim(1000, 8000)
ax1.set_xlim(0, 58)
ax6.set_ylim(0, 11.7)
ax6.set_xlim(0.1, 140)
ax3.set_xlim(0, 58)
ax8.set_xlim(0.1, 140)
ax9.set_ylim(-0.03, 1.03)

# adjust splines
# TOFs
ax1.spines["right"].set_visible(False)
ax1.spines["bottom"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.spines["bottom"].set_visible(False)
ax3.spines["right"].set_visible(False)
ax3.spines["bottom"].set_visible(False)
ax4.spines["left"].set_visible(False)
ax4.spines["bottom"].set_visible(False)
ax5.spines["right"].set_visible(False)
ax5.spines["top"].set_visible(False)
ax6.spines["left"].set_visible(False)
ax6.spines["top"].set_visible(False)
ax7.spines["right"].set_visible(False)
ax7.spines["top"].set_visible(False)
ax8.spines["left"].set_visible(False)
ax8.spines["top"].set_visible(False)
# covs
ax9.spines["right"].set_visible(False)
ax10.spines["left"].set_visible(False)
ax11.spines["right"].set_visible(False)
ax12.spines["left"].set_visible(False)


# adjust ticks
# TOFs
ax1.yaxis.tick_left()
ax1.xaxis.tick_top()
ax2.yaxis.tick_right()
ax2.xaxis.tick_top()
ax3.yaxis.tick_left()
ax3.xaxis.tick_top()
ax4.yaxis.tick_right()
ax4.xaxis.tick_top()
ax5.yaxis.tick_left()
ax5.xaxis.tick_bottom()
ax6.yaxis.tick_right()
ax6.xaxis.tick_bottom()
ax7.yaxis.tick_left()
ax7.xaxis.tick_bottom()
ax8.yaxis.tick_right()
ax8.xaxis.tick_bottom()
# covs
ax9.yaxis.tick_left()
ax10.yaxis.tick_right()
ax11.yaxis.tick_left()
ax12.yaxis.tick_right()

# set ticks
ax1.set_yticks([2000, 4000, 6000, 8000])
ax10.set_xticks([40, 80, 120])
ax12.set_xticks([40, 80, 120])

# adjust tick labels
# TOFs
ax1.tick_params(labeltop="off")
ax2.tick_params(labeltop="off")
ax2.tick_params(labelright="off")
ax3.tick_params(labeltop="off")
ax3.tick_params(labelleft="off")
ax4.tick_params(labeltop="off")
ax4.tick_params(labelright="off")
ax5.tick_params(labeltop="off")
ax5.tick_params(labelbottom="off")
ax6.tick_params(labeltop="off")
ax6.tick_params(labelright="off")
ax6.tick_params(labelbottom="off")
ax7.tick_params(labeltop="off")
ax7.tick_params(labelleft="off")
ax7.tick_params(labelbottom="off")
ax8.tick_params(labeltop="off")
ax8.tick_params(labelright="off")
ax8.tick_params(labelbottom="off")
# covs
ax10.tick_params(labelright="off")
ax11.tick_params(labelleft="off")
ax12.tick_params(labelright="off")

# set axis labels
fig.text(0.02, 0.87, r"TOF (s$^{-1}$ unit cell$^{-1}$)", rotation=90)
ax9.set_ylabel("Coverage (ML)")
ax9.set_xlabel("Time (ns)")
ax10.set_xlabel("Time (s)")
ax11.set_xlabel("Time (ns)")
ax12.set_xlabel("Time (s)")

# draw diagonal lines
d = 0.03  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax1.transAxes, color="k", clip_on=False)
ax1.plot((-d, +d), (-d, +d), **kwargs)
ax1.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)
kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # bottom-left diagonal
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal
kwargs = dict(transform=ax3.transAxes, color="k", clip_on=False)
ax3.plot((-d, +d), (-d, +d), **kwargs)
ax3.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)
kwargs.update(transform=ax4.transAxes)  # switch to the bottom axes
ax4.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # bottom-left diagonal
ax4.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal
kwargs = dict(transform=ax5.transAxes, color="k", clip_on=False)
ax5.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # bottom-left diagonal
ax5.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal
kwargs.update(transform=ax6.transAxes)  # switch to the bottom axes
ax6.plot((-d, +d), (-d, +d), **kwargs)  # bottom-left diagonal
ax6.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal
kwargs = dict(transform=ax7.transAxes, color="k", clip_on=False)
ax7.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # bottom-left diagonal
ax7.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal
kwargs.update(transform=ax8.transAxes)  # switch to the bottom axes
ax8.plot((-d, +d), (-d, +d), **kwargs)  # bottom-left diagonal
ax8.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal
d2 = d / 2.0
kwargs = dict(transform=ax9.transAxes, color="k", clip_on=False)
ax9.plot((1 - d, 1 + d), (-d2, +d2), **kwargs)  # bottom-left diagonal
ax9.plot((1 - d, 1 + d), (1 - d2, 1 + d2), **kwargs)  # bottom-right diagonal
kwargs.update(transform=ax10.transAxes)  # switch to the bottom axes
ax10.plot((-d, +d), (-d2, +d2), **kwargs)  # bottom-left diagonal
ax10.plot((-d, +d), (1 - d2, 1 + d2), **kwargs)  # bottom-right diagonal
kwargs = dict(transform=ax11.transAxes, color="k", clip_on=False)
ax11.plot((1 - d, 1 + d), (-d2, +d2), **kwargs)  # bottom-left diagonal
ax11.plot((1 - d, 1 + d), (1 - d2, 1 + d2), **kwargs)  # bottom-right diagonal
kwargs.update(transform=ax12.transAxes)  # switch to the bottom axes
ax12.plot((-d, +d), (-d2, +d2), **kwargs)  # bottom-left diagonal
ax12.plot((-d, +d), (1 - d2, 1 + d2), **kwargs)  # bottom-right diagonal

# add legends
box = ax8.get_position()
ax8.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax8.legend(bbox_to_anchor=(1, 0.916), bbox_transform=plt.gcf().transFigure)
box = ax12.get_position()
ax12.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax12.legend(bbox_to_anchor=(0.99, 0.5), bbox_transform=plt.gcf().transFigure)

# Add text
ax1.text(55, 8700, "(a)", fontsize=14)
ax3.text(55, 8700, "(b)", fontsize=14)

# save plot
plt.subplots_adjust(left=0.1, right=0.81, top=0.94, bottom=0.08, hspace=0.1, wspace=0.1)
plt.savefig("COoxRuO2_relaxation.png")
