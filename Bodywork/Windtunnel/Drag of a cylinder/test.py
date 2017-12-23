import numpy as np
import matplotlib.pyplot as plt

params = {'legend.fontsize': 20,
          'axes.linewidth': 3.5,
          'axes.labelsize': 20,
          'xtick.major.pad': 10,
          'xtick.major.width': 4,
          'xtick.major.size': 8,
          'ytick.major.width': 4,
          'ytick.major.size': 8,
          'xtick.minor.width': 2,
          'xtick.minor.size': 5,
          'ytick.minor.width': 2,
          'ytick.minor.size': 5,
          'xtick.labelsize': 20,
          'ytick.labelsize': 20,
          'text.usetex': True,
          'font.size': 20}

plt.rcParams.update(params)

v = 15.11e-6    # Kinematic viscosity of air @ 20 degrees Celsius
d = 50e-3       # Characteristic length, diameter of the sphere in [m]

Re_wiki, Cd_wiki = np.loadtxt('drag_cylinder_ref.csv', skiprows=1,
                              delimiter=',', dtype=float, unpack=True)
u_sim, Cd_sim = np.loadtxt('simulated.csv', skiprows=1, delimiter=',',
                           dtype=float, unpack=True)

# Convert wind speed to Reynolds number Re = u*d/v, u is speed in [m/s]
Re_sim = u_sim*d/v

fig = plt.figure()
ax = plt.gca()
ax.plot(Re_wiki, Cd_wiki, ls='dashed', lw=2, color='gray', label=r'From wiki')
ax.scatter(Re_sim, Cd_sim, color='red', label=r'Flow sim results')
ax.legend(frameon=False, shadow=False)
ax.set_yscale('log')
ax.set_xscale('log')
ax.set_xlabel(r"\textbf{Re} $[-]$")
ax.set_ylabel(r"$\mathbf{C_d}$ $[-]$")
plt.tight_layout()
plt.savefig("Drag_of_a_cylinder.pdf")
plt.show()
