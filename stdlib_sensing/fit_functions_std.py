import numpy as np

def fit_sinusoid(x, parameters_dict):
    """function: A*np.cos(B*x + C) + D
    default A: 1 
    default C: 0
    default D: 0
    """
    #necessary
    B = parameters_dict['B']

    #defaulted
    if 'A' in parameters_dict:
        A = parameters_dict['A']
    else: 
        A = 1
    if 'C' in parameters_dict:
        C = parameters_dict['C']
    else: 
        C = 0
    if 'D' in parameters_dict:
        D = parameters_dict['D']
    else: 
        D = 0

    #function
    return (A*np.cos(B*x + C) + D)[:,np.newaxis]