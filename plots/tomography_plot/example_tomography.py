##---------------PREAMBLE--------------##
import qutip as qt 
import numpy as np 
from stdlib_sensing import PlotTemplate, matrix_histogram
import matplotlib.pyplot as plt

#-------------------LOAD FILE----------------##

qubits = 3

#Read tomography for entangled sense state preparation
data_file = 'data/tomography_data/entangledsensestatepreparation.dat'
rho = qt.Qobj(np.loadtxt(data_file).view(complex), dims = [[2]*qubits,[2]*qubits])

#Plot of density matrix
pt = PlotTemplate((1, 2))
ax, fig = pt.generate_figure(projection='3d', fig_ret=True)
fig, _ax = matrix_histogram(np.real(rho), limits = [-0.5, 0.5], ax = ax[0], colorbar = True, colorbarpad=0.5, fig = fig)
fig, _ax = matrix_histogram(np.imag(rho), limits = [-0.5, 0.5], ax = ax[1], colorbar = False, fig = fig)
fig.savefig('plots/tomography_plot/entangledsensestatepreparation.png')
plt.show()