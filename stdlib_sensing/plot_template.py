"""Basic class to create plot templates because I got tired of constantly 
creating new figures
"""
##-------------------------------PREAMBLE-----------------------------------##
import matplotlib.pyplot as plt 
import numpy as np
import math
#packages

##-------------------------------CLASS DEFINITION-----------------------------------##

class PlotTemplate:

    def __init__(self, dim, large = False):
        self.property_params = {
            'font.size': 20,
            'legend.edgecolor': '0',
            'lines.markersize' : 5,
            'legend.borderaxespad': 1.5,
            'legend.fancybox': False,
            'legend.fontsize': 20.0,
            'legend.framealpha': 0.5,
            'legend.labelspacing': 0.3,
            'legend.markerscale': 1.0,
            'figure.figsize': (10, 8),
            'axes.labelsize': 20,
            'axes.titlesize': 20,
            'axes.linewidth': 3,
            'axes.xmargin': 0.03,
            'axes.ymargin': 0.03,
            'xtick.direction': 'in',
            'xtick.labelsize': 20,
            'xtick.major.pad': 10,
            'xtick.major.size': 10,
            'xtick.major.width': 3,
            'xtick.minor.pad': 10,
            'xtick.minor.size': 5,
            'xtick.minor.visible': True,
            'xtick.minor.width': 2,
            'xtick.top': True,
            'ytick.direction': 'in',
            'ytick.labelsize': 20,
            'ytick.major.pad': 10,
            'ytick.major.size': 10,
            'ytick.major.width': 3,
            'ytick.minor.pad': 10,
            'ytick.minor.size': 5,
            'ytick.minor.visible': True,
            'ytick.minor.width': 2,
            'ytick.right': True,
        }
        if large:
            self.property_params['axes.labelsize'] = 30
            self.property_params['legend.fontsize'] = 25
            self.property_params['xtick.labelsize'] = 30
            self.property_params['ytick.labelsize'] = 30
            self.property_params['axes.titlesize'] = 30
            self.property_params['font.size'] = 30
        # self.figsize =  (18,9)
        self.figsize =  (18,10)
        self.dim = dim
        self.colours = ['darkblue','darkmagenta','c','crimson','darkorange','tab:pink', 'mediumseagreen', 'cyan']*4
    
    def generate_figure(self, fig_ret = False, projection = None):
        plt.rcParams.update(self.property_params)#not sure this works?

        if projection == '3d':
            fig, axes = plt.subplots(self.dim[0], self.dim[1], constrained_layout=False, figsize=self.figsize, subplot_kw = {'projection': projection})
            #fig, axes = plt.subplots(self.dim[0], self.dim[1], constrained_layout=True, figsize=self.figsize, subplot_kw = {'projection': projection})
        else:
            # fig, axes = plt.subplots(self.dim[0], self.dim[1], constrained_layout=False, figsize=self.figsize)
            fig, axes = plt.subplots(self.dim[0], self.dim[1], constrained_layout=True, figsize=self.figsize)
        
        self.fig = fig
        #lazy implementation, can be improved
        if self.dim[0] == 1 and self.dim[1] == 1:
            axes.minorticks_on()
            axes.grid(True)
            axes.grid(which='minor', linestyle = '--', alpha = 0.6)            
        elif self.dim[0] == 1 or self.dim[1] == 1:
            for ax in axes:
                ax.minorticks_on()
                ax.grid(True)
                ax.grid(which='minor', linestyle = '--', alpha = 0.6)
        else:
            for axx in axes:
                for ax in axx:
                    ax.minorticks_on()
                    ax.grid(True)
                    ax.grid(which='minor', linestyle = '--', alpha = 0.6)
        if fig_ret:
            return axes, fig
        return axes
    
    # def index_double(self, index, dim1, dim2):
    #     if dim1 > dim2:
    #         return [index%self.dim[0], index//self.dim[0]]
    #     else:
    #         return [ index//self.dim[0], index%self.dim[0]]

    def index_double(self, index, dim1, dim2):
        return [index//self.dim[1], index%self.dim[1]]
        
    def dims_square(self, num):
        dim1 = int(math.ceil(np.sqrt(num)))
        dim2 = int(math.ceil(num/dim1))
        return (dim1, dim2)

    def plot(self, x, y, ax, errors = None, colour_index = 0, label = None, color = None, plottype = 'scatter',**kwargs):
        if color is None:
            color = self.colours[colour_index]
        if label is not None:
            ax.scatter(x, y, color = color, label = label, **kwargs)
            if 'line' in plottype:
                ax.plot(x, y, color = color, alpha = 0.6)
            if errors is not None:
                ax.errorbar(x, y, yerr = errors, ls = 'none', capsize = 3, color = color)
            ax.legend()

        else:
            ax.scatter(x, y, color = color, **kwargs)
            if 'line' in plottype:
                ax.plot(x, y, color = self.colours[colour_index], alpha = 0.6, label = label)
            if errors is not None:
                ax.errorbar(x, y, yerr = errors, ls = 'none', capsize = 3, color = color)

    def label_round_formatter(self, value, error, error_round = 0):
        #change error_round for different roudning of error

        error_pow = int(np.log10(error))
        value_pow = int(np.log10(np.abs(value)))


        if value_pow < 0:
            value_pow -= 1
        if error_pow <= 0:
            error_pow -= 1

        error_int = int(round(error, -1*(error_pow-error_round))*10**(-1*(error_pow-error_round)))
        value_sn = round(value*10**-value_pow, -1*((error_pow-error_round - value_pow)))

        if value_pow == 0:
            # return r'$' + '{1:0<{0}}({2})$'.format(value_pow + error_round - error_pow, value_sn , error_int)
            return r'$' + '{1:0<{0}}({2})$'.format(value_pow + error_round- error_pow + 2, value_sn , error_int) #hack, should change back
        return r'$' + '{1:0<{0}}({2})x10^'.format(value_pow + error_round - error_pow, value_sn, error_int)+ '{'+str(value_pow)+ '}$'
