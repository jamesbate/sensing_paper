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

##=======##
#Example 1
# signals = ['-25.5db']#'-25.5db'
# groups = 3
# point_index = 19 #Sit at phase 0.51525424

##=======##
#Example 2
signals = ['-27.5db']
groups = 3
point_index = 19 #Sit at phase 0.51525424

##------------------READ PARITY--------------##

POINTS = 60
SHOTS = 72

cycles = SHOTS//groups

parity = np.empty((groups, 7, 3, POINTS))
dparity = np.empty((groups, 7, 3, POINTS))

def get_parity(projections):
    _parity = np.empty((groups, POINTS)) 
    _dparity = np.empty((groups, POINTS)) 
    for p in range(POINTS):
        for g in range(groups):
            pa = ProjectionAnalysis(projections[:, p, g*cycles:(g+1)*cycles].T)
            _parity[g, p], _dparity[g, p] = pa.get_correlator(observable, error=True)      
    return _parity, _dparity

for power in power_enumerator.keys():
    for setting in setting_enumerator.keys():
        projections = projections_full[power_enumerator[power], setting_enumerator[setting]]
        parity[:, power_enumerator[power], setting_enumerator[setting], :], dparity[:, power_enumerator[power], setting_enumerator[setting], :] = get_parity(projections) 

##------------------PLOT SIGNAL--------------##

pt = PlotTemplate((1, 2))
ax, fig = pt.generate_figure(fig_ret=True)

for n, power in enumerate(power_enumerator.keys()):
    for m, setting in enumerate(['entangledsensing', 'productsensing']):#setting_enumerator.keys(), ['entangledsensing']
        if power not in signals and power != 'nosignal':
            continue
        if n == 0:
            _ax = ax[0]
        else:
            _ax = ax[1]
        pt.plot(range(groups), parity[:, power_enumerator[power], setting_enumerator[setting], point_index], _ax, errors = dparity[:, power_enumerator[power], setting_enumerator[setting], point_index], colour_index = m, plottype = 'scatter')
        _ax.axhline(np.mean(parity[:, power_enumerator[power], setting_enumerator[setting], point_index]), color = pt.colours[m], label = setting)
        _ax.set_ylim((-0.75, 0.75))
        _ax.legend()
        _ax.set_xticks(range(groups))

ax[0].set_title('no signal')
ax[1].set_title(f'with signal {signals}')
ax[0].set_ylabel('Parity signal')
ax[0].set_xlabel('Measurement')
fig.savefig('plots/oxford_plot/oxfordplotexample2.png')
plt.show()