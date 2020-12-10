import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import scipy.integrate 
from ipywidgets import Video
from numpy import *
import scipy.special

def animate_cir(f_state,g_state,r_0,prec,anilength):
	"""generate the animation for a wave on a circular membrane using given parameters from GUI"""

	def f(r,theta):
		"""initial height distribution"""
		x=r*np.cos(theta)
		y=r*np.sin(theta)
		return eval(f_state)

	def fi0(r,theta):
		"""modification to simplify the integration to compute Fourier-Bessel coefficients"""
		return r*f(r,theta)*scipy.special.jv(0,zeros[0,m-1]*r/r_0)/(np.pi*r_0**2*scipy.special.jv(1,zeros[0,m-1])**2)

	def ficos(r,theta):
		"""modification to simplify the integration to compute Fourier-Bessel coefficients"""
		return 2*r*f(r,theta)*scipy.special.jv(n,zeros[n,m-1]*r/r_0)*np.cos(n*theta)/(np.pi*r_0**2*scipy.special.jv(n+1,zeros[n,m-1])**2)

	def fisin(r,theta):
		"""modification to simplify the integration to compute Fourier-Bessel coefficients"""
		return 2*r*f(r,theta)*scipy.special.jv(n,zeros[n,m-1]*r/r_0)*np.sin(n*theta)/(np.pi*r_0**2*scipy.special.jv(n+1,zeros[n,m-1])**2)

	def g(r,theta):
		"""initial velocity distribution"""
		x=r*np.cos(theta)
		y=r*np.sin(theta)
		return eval(g_state)

	def gi0(r,theta):
		"""modification to simplify the integration to compute Fourier-Bessel coefficients"""
		return r*g(r,theta)*scipy.special.jv(0,zeros[0,m-1]*r/r_0)/(np.pi*r_0*c*zeros[n,m-1]*scipy.special.jv(1,zeros[0,m-1])**2)
  
	def gicos(r,theta):
		"""modification to simplify the integration to compute Fourier-Bessel coefficients"""
		return 2*r*g(r,theta)*scipy.special.jv(n,zeros[n,m-1]*r/r_0)*np.cos(n*theta)/(np.pi*r_0*c*zeros[n,m-1]*scipy.special.jv(n+1,zeros[n,m-1])**2)

	def gisin(r,theta):
		"""modification to simplify the integration to compute Fourier-Bessel coefficients"""
		return 2*r*g(r,theta)*scipy.special.jv(n,zeros[n,m-1]*r/r_0)*np.sin(n*theta)/(np.pi*r_0*c*zeros[n,m-1]*scipy.special.jv(n+1,zeros[n,m-1])**2)

	j=prec
	k=prec
	c=1
	tot_frames=int(25*anilength)

	zeros=[]
	for n in range(k+1):
		zeros.append(scipy.special.jn_zeros(n,j))
	zeros=np.array(zeros)

	A_0coeff=[]
	A_coeff=[]
	B_0coeff=[]
	B_coeff=[]
	C_coeff=[]
	D_coeff=[]

	for m in range(1,j+1):
		for n in range(k+1):
			if n == 0:
				A=scipy.integrate.dblquad(fi0,0,2*np.pi,0,r_0)
				A_0coeff.append(A[0])
				B=scipy.integrate.dblquad(gi0,0,2*np.pi,0,r_0)
				B_0coeff.append(B[0])
			else:
				A=scipy.integrate.dblquad(ficos,0,2*np.pi,0,r_0)
				A_coeff.append(A[0])
				B=scipy.integrate.dblquad(gicos,0,2*np.pi,0,r_0)
				B_coeff.append(B[0])
				C=scipy.integrate.dblquad(fisin,0,2*np.pi,0,r_0)
				C_coeff.append(C[0])
				D=scipy.integrate.dblquad(gisin,0,2*np.pi,0,r_0)
				D_coeff.append(B[0])

	A_0coeff=np.array(A_0coeff)
	A_0coeff=A_0coeff.reshape((j,1,1))
	A_coeff=np.array(A_coeff)
	A_coeff=A_coeff.reshape((j,k,1,1))
	B_0coeff=np.array(B_0coeff)
	B_0coeff=B_0coeff.reshape((j,1,1))
	B_coeff=np.array(B_coeff)
	B_coeff=B_coeff.reshape((j,k,1,1))
	C_coeff=np.array(C_coeff)
	C_coeff=C_coeff.reshape((j,k,1,1))
	D_coeff=np.array(D_coeff)
	D_coeff=D_coeff.reshape((j,k,1,1))

	r=np.linspace(0,r_0,250)
	theta=np.linspace(0,2*np.pi,250)

	R, Theta=np.meshgrid(r,theta)

	bessels=np.array([[scipy.special.jv(n,zeros[n,m-1]*R/r_0) for n in range(k+1)] for m in range(1,j+1)])
	sines=np.array([np.sin(n*Theta) for n in range(k+1)])
	cosines=np.array([np.cos(n*Theta) for n in range(k+1)])

	NTDA0=np.array([A_0coeff*bessels[:,0]])
	NTDB0=np.array([B_0coeff*bessels[:,0]])
	NTDA=A_coeff*bessels[:,1:]*cosines[1:]
	NTDB=B_coeff*bessels[:,1:]*cosines[1:]
	NTDA=np.append(NTDA0,NTDA,axis=0)
	NTDB=np.append(NTDB0,NTDB,axis=0)
	NTDC=C_coeff*bessels[:,1:]*sines[1:]
	NTDC=np.append(np.zeros((1,j,250,250)),NTDC,axis=0)
	NTDD=D_coeff*bessels[:,1:]*sines[1:]
	NTDD=np.append(np.zeros((1,j,250,250)),NTDD,axis=0)

	z=[]
	for t in range(tot_frames):
		zpst=[NTDA[n,m]*np.cos(c*zeros[n,m]*t/(r_0*25))+
			NTDB[n,m]*np.sin(c*zeros[n,m]*t/(r_0*25))+
			NTDC[n,m]*np.cos(c*zeros[n,m]*t/(r_0*25))+
			NTDD[n,m]*np.sin(c*zeros[n,m]*t/(r_0*25)) 
			for m in range(j) for n in range(k+1)]
		zpst=np.array(zpst)
		z.append(np.sum(zpst,axis=0))

	z=np.array(z)

	x,y=R*np.cos(Theta),R*np.sin(Theta)
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	def init():
		"""initialize animation"""
		ax.set_xlim(-1.1*r_0,1.1*r_0)
		ax.set_ylim(-1.1*r_0,1.1*r_0)
		ax.set_zlim(1.2*np.min(z),1.2*np.max(z))
		ax.set_xlabel("x",fontsize=18)
		ax.set_ylabel("y",fontsize=18)
		ax.set_zlabel("Height",fontsize=14)

	def update_plot(frame,z,plot):
		"""generate animation frames and update the frames"""
		plot[0].remove()
		plot[0]=ax.plot_surface(x,y,z[frame],cmap="viridis")

	plot=[ax.plot_surface(x,y,z[0],cmap="viridis")]
	ani1 = ani.FuncAnimation(fig, update_plot, frames=range(tot_frames),
							init_func=init, repeat=False, fargs=(z, plot), interval=40)

	return ani1