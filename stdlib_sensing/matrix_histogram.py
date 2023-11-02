import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
#from qutip.qobj import Qobj
import qutip as qt
import numpy as np

#From qutip!

def matrix_histogram(M, xlabels=None, ylabels=None, title=None, limits=None,
                     colorbar=True, fig=None, ax=None, colorbarpad = 0, cmap_name = 'jet'):#'jet'
    """
    Draw a histogram for the matrix M, with the given x and y labels and title.

    Parameters
    ----------
    M : Matrix of Qobj
        The matrix to visualize

    xlabels : list of strings
        list of x labels

    ylabels : list of strings
        list of y labels

    title : string
        title of the plot (optional)

    limits : list/array with two float numbers
        The z-axis limits [min, max] (optional)

    ax : a matplotlib axes instance
        The axes context in which the plot will be drawn.

    Returns
    -------
    fig, ax : tuple
        A tuple of the matplotlib figure and axes instances used to produce
        the figure.

    Raises
    ------
    ValueError
        Input argument is not valid.

    """

    if isinstance(M, qt.Qobj):
        # extract matrix data from Qobj
        M = M.full()

    n = np.size(M)
    xpos, ypos = np.meshgrid(range(M.shape[0]), range(M.shape[1]))
    xpos = xpos.T.flatten() - 0.5
    ypos = ypos.T.flatten() - 0.5
    zpos = np.zeros(n)
    dx = dy = 0.8 * np.ones(n)
    dz = np.real(M.flatten())

    if limits and type(limits) is list and len(limits) == 2:
        z_min = limits[0]
        z_max = limits[1]
    else:
        z_min = min(dz)
        z_max = max(dz)
        if z_min == z_max:
            z_min -= 0.1
            z_max += 0.1

    norm = mpl.colors.Normalize(z_min, z_max)
    cmap = cm.get_cmap(cmap_name)  # Spectral
    colors = cmap(norm(dz))

    if ax is None:
        fig = plt.figure()
        ax = Axes3D(fig, azim=-35, elev=35)

    im = ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colors)

    if title and fig:
        ax.set_title(title)

    # x axis
    ax.axes.w_xaxis.set_major_locator(plt.IndexLocator(1, -0.5))
    if xlabels is not None:
        ax.set_xticklabels(xlabels)
    ax.tick_params(axis='x', labelsize=14)

    # y axis
    ax.axes.w_yaxis.set_major_locator(plt.IndexLocator(1, -0.5))
    if ylabels is not None:
        ax.set_yticklabels(ylabels)
    ax.tick_params(axis='y', labelsize=14)

    # z axis
    ax.axes.w_zaxis.set_major_locator(plt.IndexLocator(1, 0.5))
    #ax.axes.w_zaxis.set_major_locator(plt.IndexLocator(1, 0.25))
    ax.set_zlim3d([min(z_min, 0), z_max])

    # color axis
    # if colorbar:
    #     # cax, kw = mpl.colorbar.make_axes(ax, shrink=.75, pad=colorbarpad)
    #     cax, kw = mpl.colorbar.make_axes(ax, shrink=0.5, pad=colorbarpad)
    #     mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm)

    if colorbar:
        # cax, kw = mpl.colorbar.make_axes(ax, shrink=.75, pad=colorbarpad, location = 'left', fraction = 0.01)
        # mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm)
        # cb_ax = fig.add_axes([.91,.124,.04,.754])
        cb_ax = fig.add_axes([.02,.224,.02,.554])
        mpl.colorbar.ColorbarBase(cb_ax, cmap=cmap, norm=norm)
        #fig.colorbar(im,orientation='vertical',cax=cb_ax)

    ax.view_init(25, -30, 0)

    if limits is not None:
        ax.set(zticks = [limits[0], limits[1]])
    else:
        ax.set(zticks = [-1, 1])

    return fig, ax