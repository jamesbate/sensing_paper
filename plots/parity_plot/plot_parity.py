##------------------PREAMBLE-------------------##
import numpy as np
import scipy
import qutip as qt
import matplotlib.pyplot as plt
from stdlib_sensing import setting_enumerator, power_enumerator, ProjectionAnalysis, PlotTemplate

##------------------PARAMETERS--------------------##
#Read data
projections_full = scipy.io.loadmat('data/parity_data/projections.mat')['out']
phase = np.linspace(0, 1.6, 60)

observable = qt.tensor([qt.sigmaz()]*3)
parity = np.empty((7, 3, 60))
dparity = np.empty((7, 3, 60))

power_toplot = ['nosignal', '-23.5db', '-27.5db']

pt = PlotTemplate((3, 1))
pt.figsize = (8, 10)
pt.property_params['legend.fontsize'] = 12
ax, fig = pt.generate_figure(fig_ret = True)

##------------------PLOTPARITY--------------##

plot_counter = 0
for power in power_enumerator.keys():
    for setting in setting_enumerator.keys():

        #Projections for given experiment. (3, 60, 72) -> ion, point, shot
        projections = projections_full[power_enumerator[power], setting_enumerator[setting]]

        for p in range(phase.size):
            pa = ProjectionAnalysis(projections[:, p, :].T)
            parity[power_enumerator[power], setting_enumerator[setting], p], dparity[power_enumerator[power], setting_enumerator[setting], p] = pa.get_correlator(observable, error=True)

        if power in power_toplot:
            pt.plot(phase, parity[power_enumerator[power], setting_enumerator[setting], :], ax[plot_counter], errors = dparity[power_enumerator[power], setting_enumerator[setting], p], colour_index = setting_enumerator[setting], plottype = 'scatterline', label = setting)#, errors = parity[power_enumerator[power], setting_enumerator[setting], :]
            ax[plot_counter].set_ylim((-1, 1))
            ax[plot_counter].set_title(power)

    if power in power_toplot:
        plot_counter += 1

ax[0].set_xlabel('Measurement phase')
ax[0].set_ylabel('Parity')
fig.savefig('plots/parity_plot/example_parity.png')
plt.show()




