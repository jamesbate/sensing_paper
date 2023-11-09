##------------------PREAMBLE-------------------##
import numpy as np
import scipy
import qutip as qt
import matplotlib.pyplot as plt
from stdlib_sensing import setting_enumerator, power_enumerator, ProjectionAnalysis, PlotTemplate

##------------------PARAMETERS--------------------##
# Read data
projections_full = scipy.io.loadmat('data/parity_data/projections.mat')['out']
phase = np.linspace(0, 1.6, 60)

observable = qt.tensor([qt.sigmaz()] * 3)
parity = np.empty((7, 3, 60))
dparity = np.empty((7, 3, 60))

phase_index_toplot = range(60)

pt = PlotTemplate((len(phase_index_toplot), 1))
pt.figsize = (8, 300)
pt.property_params['legend.fontsize'] = 12
ax, fig = pt.generate_figure(fig_ret=True)

##------------------CONVERSIONS-----------------------##
def power2signal(power):
    if power == 'nosignal':
        return 0
    sdb = float(power[:-2])
    s = 10**(sdb/10)
    return s

##------------------PLOTPARITYOVERSIGNAL--------------##

plot_counter = 0
for phase_index in phase_index_toplot:
    for setting in setting_enumerator.keys():

        signals = []
        for power in power_enumerator.keys():
            # Projections for given experiment. (3, 60, 72) -> ion, point, shot
            projections = projections_full[power_enumerator[power], setting_enumerator[setting]]

            pa = ProjectionAnalysis(projections[:, phase_index, :].T)
            parity[power_enumerator[power], setting_enumerator[setting], phase_index], dparity[
                power_enumerator[power], setting_enumerator[setting], phase_index] = pa.get_correlator(observable, error=True)

            signals.append(power2signal(power))
        pt.plot(signals, parity[:, setting_enumerator[setting], phase_index], ax[plot_counter],
                errors=dparity[:, setting_enumerator[setting], phase_index],
                colour_index=setting_enumerator[setting], plottype='scatterline',
                label=setting)  # , errors = parity[power_enumerator[power], setting_enumerator[setting], :]
    ax[plot_counter].set_ylim((-1, 1))
    ax[plot_counter].set_title(f'Meassurement phase index: {phase_index}')
    ax[plot_counter].set_xlabel('Signal')
    ax[plot_counter].set_ylabel('Parity')
    plot_counter += 1


fig.savefig('plots/parity_over_signal_plot/example_parity_signal.png')
plt.show()
