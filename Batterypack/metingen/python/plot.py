import glob
import os
import matplotlib.pyplot as plt
import numpy as np

numcells = 1.
dirname = "test_auto_12cells"


def setplotparams():
    ''' Set a bunch of plot paramaters '''
    plt.rcParams.update(plt.rcParamsDefault)
    params = {  # 'legend.fontsize':        27,
                # 'axes.linewidth':         3.5,
                # 'axes.labelsize':         25,
                # 'xtick.minor.size':       6,
                # 'xtick.minor.width':      2,
                # 'xtick.major.pad':        10,
                # 'xtick.major.width':      4,
                # 'xtick.major.size':       12,
                # 'ytick.minor.size':       6,
                # 'ytick.minor.width':      2,
                # 'ytick.major.width':      4,
                # 'ytick.major.size':       12,
                # 'xtick.labelsize':        20,
                # 'ytick.labelsize':        20,
              'errorbar.capsize':       4,
              'text.usetex':            True,
              'text.latex.preamble':    "\\usepackage{amsmath} \
                                         \\usepackage{amssymb} \
                                         \\usepackage{amsfonts}",
              'font.size':              21,
              'font.family':            'serif',
              'font.serif':             'Computer Modern'
              }
    plt.rcParams.update(params)


def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


def getAllData(dir, suffix):
    '''Get the data from the .suffix files at path dir,
    returns the data from all .suffix files in dir.'''
    pwd = os.getcwd()
    os.chdir(dir)
    print(os.getcwd())
    time = [None]*10000
    voltage = [None]*10000
    current = [None]*10000
    count = 0
    files = glob.glob("*." + suffix)
    files.sort()
    for filename in files:
        print(filename)
        tempT, tempV, tempI = np.loadtxt(filename, skiprows=1, unpack=True,
                                         delimiter=',', usecols=(0, 1, 2),
                                         converters={0: lambda s: np.sum(
                                             [int(i)*y for i, y in zip(
                                                 s.decode().split(':'),
                                                 [3600, 60, 1])]
                                         )
                                                     })
        time[count:(count + len(tempV))] = tempT
        voltage[count:(count + len(tempV))] = tempV
        current[count:(count + len(tempV))] = tempI
        count += len(tempV)
    os.chdir(pwd)
    time[:count] = time[:count] - time[0]
    return time[:count], voltage[:count], current[:count]


def main():
    setplotparams()
    plt.clf()
    plt.cla()
    plt.close('all')
    fig, ax1 = plt.subplots()
    fig.subplots_adjust(left=0.15, right=0.85)
    secs, volts, amps = getAllData(dirname, "csv")
    ax1.scatter(secs, volts, color='navy', s=12., marker='^')
    #  ax1.errorbar(secs, volts, yerr=(80e-3), errorevery=100,
    #               ecolor='navy', fmt='none')
    ax1.set_xlabel(r"\textbf{Time [s]}")
    ax1.set_ylabel(r"\textbf{Voltage [V]}", color="navy")
    ax1.tick_params("y", colors="navy")
    ax1.set_xlim([secs[0]-1, secs[-1]+1])
    ax2 = ax1.twinx()
    ax2.scatter(secs, amps, color='firebrick', s=12., marker='v')
    #  ax2.errorbar(secs, amps, yerr=(2e-3*200), errorevery=100,
    #               ecolor='firebrick', fmt='none')
    ax2.set_ylim([np.min(amps)-.1, np.max(amps)+.1])
    ax2.set_ylabel(r"\textbf{Current [A]}", color="firebrick")
    ax2.tick_params('y', colors='firebrick')

    shifted = [0] + list(secs[:-1])
    secs_diff = secs - np.array(shifted)
    e = (np.array(volts)*np.array(amps)*secs_diff).cumsum()/3600.

    ax3 = ax1.twinx()
    # Offset the right spine of ax3.  The ticks and label have already been
    # placed on the right by twinx above.
    ax3.spines["left"].set_position(("axes", -0.2))
    # Having been created by twinx, ax3 has its frame off, so the line of its
    # detached spine is invisible.  First, activate the frame but make the patch
    # and spines invisible.
    ax3.yaxis.set_label_position('left')
    ax3.yaxis.set_ticks_position('left')
    make_patch_spines_invisible(ax3)
    # Second, show the right spine.
    ax3.spines["left"].set_visible(True)
    ax3.scatter(range(len(amps)), e/numcells, color='goldenrod')
    #  ax3.errorbar(range(len(amps)), e/numcells, yerr=[e_uerror/numcells,
    #                                                   e_lerror/numcells],
    #               color='goldenrod', fmt='none', errorevery=100, size=6.)
    ax3.set_ylabel(r"\textbf{Energy [Wh]}", color="goldenrod")
    ax3.tick_params("y", colors="goldenrod")

    ax4 = ax1.twinx()
    # Offset the right spine of ax3.  The ticks and label have already been
    # placed on the right by twinx above.
    ax4.spines["right"].set_position(("axes", 1.3))
    # Having been created by twinx, ax3 has its frame off, so the line of its
    # detached spine is invisible.  First, activate the frame but make the patch
    # and spines invisible.
    ax4.yaxis.set_label_position('right')
    ax4.yaxis.set_ticks_position('right')
    make_patch_spines_invisible(ax4)
    # Second, show the right spine.
    ax4.spines["right"].set_visible(True)
    amph = np.array(amps).cumsum()/(3600*numcells)
    ax4.scatter(secs, amph, color='coral')
    ax4.set_ylabel(r"\textbf{Amp hour [Ah]}", color="coral")
    ax4.tick_params("y", colors="coral")
    plt.savefig("test_auto_12cells.pdf", bbox_inches='tight')

    print("{:<30}{:>10.2f} Ah".format("Total amp hour: ", amph[-1]))
    print("{:<30}{:>10.2f} Wh".format("Total watt hour: ", e[-1]/numcells))


if __name__ == "__main__":
    main()
