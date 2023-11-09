##---------------PREAMBLE--------------##
import qutip as qt 
import numpy as np 
from stdlib_sensing import PlotTemplate, matrix_histogram, quantum_fischer_information
import matplotlib.pyplot as plt

#-------------------LOAD FILE----------------##

qubits = 3

#Read tomography for entangled sense state preparation
state = "product"
time_label = "constnoise80ms"
data_file = f'data/tomography_data/{state}sensestate{time_label}.dat'
rho = qt.Qobj(np.loadtxt(data_file).view(complex), dims = [[2]*qubits,[2]*qubits])

#Plot of density matrix
pt = PlotTemplate((1, 2))
ax, fig = pt.generate_figure(projection='3d', fig_ret=True)
fig, _ax = matrix_histogram(np.real(rho), limits = [-0.5, 0.5], ax = ax[0], colorbar = True, colorbarpad=0.5, fig = fig)
fig, _ax = matrix_histogram(np.imag(rho), limits = [-0.5, 0.5], ax = ax[1], colorbar = False, fig = fig)
_ax.set_title(f'QFI ∝ {quantum_fischer_information(rho, qt.tensor(qt.identity(2),qt.sigmaz(),qt.identity(2)))}')

fig.savefig(f'plots/tomography_plot/{state}sensestate{time_label}.png')
plt.show()