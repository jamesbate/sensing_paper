"""After seeing how great the lmfit package, I was inspired to create my own
object employing it. This acts as a fitting template. 
"""
##-------------------------------PREAMBLE-----------------------------------##
import numpy as np
from lmfit import minimize, Parameters, fit_report 
from stdlib_sensing import PlotTemplate

##-------------------------------CLASS DEFINITION-----------------------------------##

class FitTemplate(): 
    def __init__(self, fit_function):
        self.fit_function = fit_function 
        self.parameters = Parameters()
        self.fit_result = None
        self.fit_result_params = None
        self.fit_result_error_dict = {}
        
    def _residuals_wrapper(self, parameters, x, data,weights,**kwargs):
        #This is bad coding. Function fitting relies on residuals, whereas optimiser relies on the value of the objective function. 

        if x is None and data is None:
            return [self.fit_function(parameters.valuesdict(), **kwargs)]*len(parameters)
        else:
            model_values = self.fit_function(x, parameters.valuesdict(), **kwargs)
            #reshape data 
            data = data.reshape((data.size,1))
            model_values = model_values.reshape((model_values.size,1))
            if not isinstance(weights, int):
                weights = weights.reshape((weights.size, 1))
            return ((model_values - data)*weights)**2
        
    def do_minimisation(self, x, data, weights = 1,**kwargs):
        self.fit_result = minimize(self._residuals_wrapper, self.parameters, args = (x, data, weights), kws = kwargs, nan_policy = 'propagate')
        #self.fit_result = minimize(self._residuals_wrapper, self.parameters, args = (x, data, weights), kws = kwargs, nan_policy = 'propagate', method = 'nelder')#TEMPORARY CHANGE
        self.fit_result_params = self.get_opt_parameters()
        for name, param in self.fit_result.params.items():
            self.fit_result_error_dict.update({name: param.stderr})
        return self.fit_result

    def do_optimisation(self,**kwargs):
        """do_minimisation assumes you are fitting data. This method allows you to just optimise a function
        """
        self.fit_result = minimize(self._residuals_wrapper, self.parameters, args = (None, None, None), kws = kwargs, nan_policy = 'propagate', method = 'Powell', tol = 1e-12)
        #self.fit_result = minimize(self._residuals_wrapper, self.parameters, args = (None, None, None), kws = kwargs, nan_policy = 'propagate') 
        self.fit_result_params = self.get_opt_parameters()
        for name, param in self.fit_result.params.items():
            self.fit_result_error_dict.update({name: param.stderr})
        return self.fit_result

    def plot_fit_optcurve(self, x, parameters = None,points = None,xlabel = None, ylabel = None, title = None, label = None, ax = None, c = None, colour_index = None,**kwargs):
        """This function plots the curve of the optimum set of parameters. If parameters argument given, this overrides optimum parameters and 
        plots custom parameters. 
        """

        #Use plot template if no ax argument given
        plot_template = PlotTemplate((1,1))
        if ax is None:
            ax = plot_template.generate_figure() 

        #decide colour 
        if c is not None: 
            color = c 
        elif colour_index is not None: 
            color = plot_template.colours[colour_index]
        else: 
            color = plot_template.colours[0]

        #plot model
        if points is None:
            fitdomain = x
        else:
            fitdomain = np.linspace(x[0], x[-1], points)	
        if parameters is None:
            y = self.fit_function(fitdomain, self.fit_result.params.valuesdict(), **kwargs)
            ax.plot(fitdomain, y, c = color, label = label)
        else:
            y = self.fit_function(fitdomain, parameters, **kwargs)
            ax.plot(fitdomain, y, c = color, label = label)
        #set labels
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        return y


    def plot_fit(self, x, y, xlabel = None, ylabel = None, title = None, errorbars = None, label = None, ax = None, c = None, colour_index = None, **kwargs):
        """Full plotting function. 
        """
        #Use plot template if no ax argument given
        plot_template = PlotTemplate((1,1))
        if ax is None:
            ax = plot_template.generate_figure() 

        #decide colour 
        if c is not None: 
            color = c 
        elif colour_index is not None: 
            color = plot_template.colours[colour_index]
        else: 
            color = plot_template.colours[0]
        
        #if error plot not requested, go ahead with standard plot
        #scatter plot
        ax.scatter(x, y, color = color)
        #plot errors
        if errorbars is not None:
            ax.errorbar(x, y, errorbars, ls = 'none', c = color, capsize = 3)
        
        #plot model
        self.plot_fit_optcurve(x, ax = ax, c = color, label = label, xlabel = xlabel, ylabel = ylabel, title = title, **kwargs)

        return y

    def get_opt_parameters(self, errors = False):
        if self.fit_result is None: 
            raise ValueError("No fit result! Do a fit before asking for")
        if errors:
            return self.fit_result.params.valuesdict(), self.fit_result_error_dict
        return self.fit_result.params.valuesdict()

    def print_parameters(self):
        self.parameters.pretty_print() 
    
    def print_fit_result(self):
        print(fit_report(self.fit_result))






