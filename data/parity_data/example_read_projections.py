##-------------------PREAMBLE----------------##
import numpy as np
import scipy
#packages

##-----------------MAIN----------------##

#Specify the filename of the .mat file
matfile = 'data/parity_data/projections.mat'

#Read data
parity_data = scipy.io.loadmat(matfile)['out']

#parity_data shape (7, 3, 3, 60, 72) -> (AC stark power, 'experiment setting', ion, analysis phase, shot number). 
#The phase is scanned from 0 to 1.6 in 60 steps
phase = np.linspace(0, 1.6, 60)

#Here I define the index enumerations: 
power_enumerator = {
    'nosignal': 0,
    '-27.5db': 1,
    '-25.5db': 3,
    '-24.5db': 4,
    '-24db': 5,
    '-23.5db': 6,
    '-23db': 7,
}
setting_enumerator = {
    'entangledsensing': 0,
    'entangledsensingnonoise': 1,
    'productsensing': 2
}

#Example: get parity data for entangled sensing state experiment with no signal
parity_entanalged_nosignal = parity_data[power_enumerator['nosignal'], setting_enumerator['entangledsensing']]
print(f'Parity data for entangled sensing experiment with no signal:\n{parity_entanalged_nosignal}')
