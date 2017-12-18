import numpy as np
import pylab as pl
import scipy.optimize

params = {'legend.fontsize' : 20,
          'axes.linewidth'  : 3.5,
          'axes.labelsize'  : 20,
          'xtick.major.pad' : 10,
          'xtick.major.width' : 4,
          'xtick.major.size'  : 8,
          'ytick.major.width' : 4,
          'ytick.major.size'  : 8,
          'xtick.minor.width' : 2,
          'xtick.minor.size'  : 5,
          'ytick.minor.width' : 2,
          'ytick.minor.size'  : 5,
          'xtick.labelsize'    : 20,
          'ytick.labelsize'    : 20,
          'text.usetex'        : True,
          'font.size'          : 20 }
pl.rcParams.update(params)

v,f,gm,gr = np.loadtxt("sw_sim.txt",unpack=True)

# convergence plot
fig = pl.figure()
ax = fig.add_subplot(111)
for vi in set(v):
    fmax = max(f[vi==v])
    ax.plot(gm[vi==v],f[vi==v]/fmax,label=r"$v={:.1f}$".format(vi),marker='o',lw=3)
ax.legend(frameon=False,shadow=False)
ax.set_xlabel(r"SW flow global initial mesh refinement")
ax.set_ylabel(r"convergence")
pl.tight_layout()
fig.savefig("convergence.pdf")

# force plot
fig = pl.figure(figsize=(10,4.8))
ax = fig.add_subplot(121)
# gm==gmmax filter: ~ converged values/most accurate values with finest global mesh (gm)
gmmax = max(gm)
vc = v[gm==gmmax] # vc, "v converged"
fc = f[gm==gmmax] # fc, "force converged"
fvfit = lambda v,a,b: a*v**2 + b*v
popt,pcov = scipy.optimize.curve_fit(fvfit,vc,fc,p0=[1,1])
ax.plot(vc,fc,marker='o',lw=0,c='deepskyblue')
vrange = np.linspace(0,1.1*max(vc),101)
ax.plot(vrange,fvfit(vrange,*popt),ls='dashed',lw=2,color='gray')
ax.set_xlabel(r"$v$ $[\frac{m}{s}]$")
ax.set_ylabel(r"$F$ $[N]$")

ax = fig.add_subplot(122)
Pc = fc*vc # Pc, "power converged"
ax.plot(vc,Pc,marker='o',lw=0,c='deepskyblue')
ax.plot(vrange,vrange*fvfit(vrange,*popt),ls='dashed',lw=2,color='gray')
ax.set_xlabel(r"$v$ $[\frac{m}{s}]$")
ax.set_ylabel(r"$P$ $[W]$")
pl.tight_layout()
fig.savefig("ForcePower.pdf")
pl.show()
