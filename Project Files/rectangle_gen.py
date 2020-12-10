import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import scipy.integrate 
from ipywidgets import Video
from numpy import *

def animate_rect(f_state,g_state,L,H,prec,anilength):
	"""generate the animation for a wave on a rectangular membrane using given parameters from GUI"""

	def f(x,y):
		"""initial height distribution"""
		r=np.sqrt(x**2+y**2)
		if x > 0:
			if y > 0:
				theta=np.arctan(y/x)
			elif y < 0:
				theta=np.arctan(y/x)+2*np.pi
			else:
				theta=0
		if x < 0:
			if y != 0:
				theta=np.arctan(y/x)+np.pi
			else:
				theta=np.pi
		if x == 0:
			if y > 0:
				theta=np.pi/2
			elif y < 0:
				theta=3*np.pi/2
			else:
				theta=0
		return eval(f_state)

	def fi(x,y):
		"""modification to simplify the integration to compute Fourier coefficients"""
		return f(x,y)*np.sin(n*np.pi*x/L)*np.sin(m*np.pi*y/H)*4/(L*H)

	def g(x,y):
		"""initial velocity distribution"""
		r=np.sqrt(x**2+y**2)
		if x > 0:
			if y > 0:
				theta=np.arctan(y/x)
			elif y < 0:
				theta=np.arctan(y/x)+2*np.pi
			else:
				theta=0
		if x < 0:
			if y != 0:
				theta=np.arctan(y/x)+np.pi
			else:
				theta=np.pi
		if x == 0:
			if y > 0:
				theta=np.pi/2
			elif y < 0:
				theta=3*np.pi/2
			else:
				theta=0
		return eval(g_state)

	def gi(x,y):
		"""modification to simplify the integration to compute Fourier coefficients"""
		return g(x,y)*np.sin(n*np.pi*x/L)*np.sin(m*np.pi*y/H)*4/(np.pi*c*np.sqrt(m**2*L**2+n**2*H**2))

	j=prec
	k=prec
	c=1
	tot_frames=int(25*anilength)

	A_coeff=[]
	B_coeff=[]

	for n in range(1,k+1):
		for m in range(1,j+1):
			A_coeff.append(scipy.integrate.dblquad(fi,0,H,0,L)[0])
			B_coeff.append(scipy.integrate.dblquad(gi,0,H,0,L)[0])

	A_coeff=np.array(A_coeff)
	A_coeff=A_coeff.reshape((k,j,1,1))
	B_coeff=np.array(B_coeff)
	B_coeff=B_coeff.reshape((k,j,1,1))

	x=np.linspace(0,L,250)
	y=np.linspace(0,H,250)
	X,Y=np.meshgrid(x,y)

	sines=np.array([[np.sin(n*np.pi*X/L)*np.sin(m*np.pi*Y/H) for m in range(1,j+1)] 
    		        for n in range(1,k+1)])
	NTDA=A_coeff*sines
	NTDB=B_coeff*sines
	NTDA=NTDA.reshape((k,j,len(x),len(y)))
	NTDB=NTDB.reshape((k,j,len(x),len(y)))

	sq=np.array([[np.sqrt(m**2/H**2+n**2/L**2)*np.pi*c/25 for m in range(1,j+1)]
    	        for n in range(1,k+1)])

	z=np.array([np.sum([np.array(NTDA[n-1,m-1]*np.cos(sq[n-1,m-1]*t)+
    	                NTDB[n-1,m-1]*np.sin(sq[n-1,m-1]*t)) 
        	            for n in range(1,k+1) for m in range(1,j+1)],axis=0) 
  				for t in range(tot_frames)])

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	if L > H:
  		lim=L
	else:
  		lim=H

	def init():
		"""initialize animation"""
		ax.set_xlim(0,lim)
		ax.set_ylim(0,lim)
		ax.set_zlim(1.2*np.min(z),1.2*np.max(z))
		ax.set_xlabel("x",fontsize=18)
		ax.set_ylabel("y",fontsize=18)
		ax.set_zlabel("Height",fontsize=14)

	def update_plot(frame,z,plot):
		"""generate animation frames and update the frames"""
		plot[0].remove()
		plot[0]=ax.plot_surface(X,Y,z[frame],cmap="viridis")

	plot=[ax.plot_surface(X,Y,z[0],cmap="viridis")]
	ani1 = ani.FuncAnimation(fig, update_plot, frames=range(tot_frames),
    	                     init_func=init, repeat=False, fargs=(z, plot), interval=40)

	return ani1