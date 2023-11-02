##---------------PREAMBLE--------------##
import qutip as qt 
import numpy as np 

#-------------------LOAD FILE----------------##

qubits = 3

#Read tomography for entangled sense state preparation
data_file = 'data/tomography_data/entangledsensestatepreparation.dat'
rho_ion_photon = qt.Qobj(np.loadtxt(data_file).view(complex), dims = [[2]*qubits,[2]*qubits])
print(rho_ion_photon)

