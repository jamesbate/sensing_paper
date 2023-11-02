#Note to self: previously called MetrologyAnalysis
##------------------PREAMBLE-------------------##
import numpy as np
import itertools
import qutip as qt

##--------------CLASSDEFINITION--------------##
class ProjectionAnalysis:

    def __init__(self, Q):
        """A class for analysing projection data

        Args:
            Q (numpy array (ion, shot_number) ): Array of projection outcomes
        """
        self.shots, self.ions = Q.shape
        self.Q = Q
        self.outcome_list = np.array(list(map(list, itertools.product([0, 1], repeat=self.ions))))

    def get_correlator(self, observable, error = False):
        """Returns the expectation value of a give DIAGONAL obervable. observable argument should be qutip object
        """
        x = np.sqrt(self.get_outcome_probabilities().T)
        parity = x.T.dot(observable).dot(x)
        if error:
            return parity, np.sqrt((1-parity**2)/self.shots)
        return parity

    def get_outcome_probabilities(self):
        """Return probability of each outcome from self.outcome_list. 
        """
        return np.array([self._get_outcome_numbers(i, self.Q) for i in self.outcome_list])/self.shots

    def _get_outcome_numbers(self, measurement_vector, Q):
        mask = np.ones(self.shots)
        for i,m in enumerate(measurement_vector):
            mask *= Q[:,i] == m 
        return np.sum(mask)
