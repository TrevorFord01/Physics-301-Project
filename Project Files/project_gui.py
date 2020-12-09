from tkinter import *
from sympy.parsing.sympy_parser import parse_expr
from sympy import init_printing,latex
import matplotlib.pyplot as plt
from PIL import ImageTk,Image
from circle_gen import animate_cir
from rectangle_gen import animate_rect
import matplotlib.animation as ani
import moviepy.editor as mp

root=Tk()
root.title("Wave Animation Generator")

def changeshape0():
	global shape_1,l,w,r
	l=Entry(root)
	w=Entry(root)
	l.grid(row=4,column=0)
	w.grid(row=5,column=0)
	r=Entry(root,state=DISABLED)
	r.grid(row=7,column=0)
	shape_1=0

def changeshape1():
	global shape_1,l,w,r
	l=Entry(root,state=DISABLED)
	w=Entry(root,state=DISABLED)
	l.grid(row=4,column=0)
	w.grid(row=5,column=0)
	r=Entry(root)
	r.grid(row=7,column=0)
	shape_1=1

def generate_fpreview():
	a=f_r.get()
	b=f_p.get()
	if a:
		fprev=parse_expr(str(a))
	elif b:
		fprev=parse_expr(str(b))
	else:
		Label(root,text="No function available...").grid(row=12,column=0)
		return
	plt.plot(0,0)
	plt.box(False)
	plt.tick_params(top=False,bottom=False,left=False,right=False,
		labelleft=False,labelbottom=False)
	plt.figtext(0.1,0.5,r"$%s$" %(latex(fprev)),fontsize=12,color="black")
	plt.savefig("f_preview.png")
	plt.clf()
	top=Toplevel()
	top.title("Equation Preview")
	preview=Image.open('f_preview.png').crop((38,212,470,255))
	plotf=ImageTk.PhotoImage(preview)
	Label(top,image=plotf).pack()

def generate_gpreview():
	c=g_r.get()
	d=g_p.get()
	if c:
		gprev=parse_expr(str(c))
	elif d:
		gprev=parse_expr(str(d))
	else:
		Label(root,text="No function available...").grid(row=17,column=0)
		return
	plt.plot(0,0)
	plt.box(False)
	plt.tick_params(top=False,bottom=False,left=False,right=False,
		labelleft=False,labelbottom=False)
	plt.figtext(0.1,0.5,r"$%s$" %(latex(gprev)),fontsize=12,color="black")
	plt.savefig("g_preview.png")
	plt.clf()
	top=Toplevel()
	top.title("Equation Preview")
	preview=Image.open('g_preview.png').crop((38,212,470,255))
	plotg=ImageTk.PhotoImage(preview)
	Label(top,image=plotg).pack()

def generateanimation():

	space=Label(root,text="                                          "+
				"                                             ")
	space.grid(row=23,column=0)

	if shape_1 == 0:
		L=l.get()
		H=w.get()
		if L == "" or H == "":
			swarn=Label(root,text="       You must fill in the size parameters!         ")
			swarn.grid(row=23,column=0)
			flag=1
			return
		L=float(L)
		H=float(H)
	elif shape_1 == 1:
		r_0=r.get()
		if r_0 == "":
			swarn=Label(root,text="          You must fill in the size parameter!           ")
			swarn.grid(row=23,column=0)
			flag=1
			return
		r_0=float(r_0)
	else:
		mwarn=Label(root,text="You must select a membrane shape!")
		mwarn.grid(row=23,column=0)
		flag=0
		return

	if f_r.get():
		f=str(f_r.get())
		rectf=True
	elif f_p.get():
		f=str(f_p.get())
		rectf=False
	else:
		fwarn=Label(root,text="   No initial height distribution provided...   ")
		fwarn.grid(row=23,column=0)
		flag=2
		return
	if g_r.get():
		g=str(g_r.get())
		rectg=True
	elif g_p.get():
		g=str(g_p.get())
		rectg=False
	else:
		gwarn=Label(root,text="No initial velocity distribution provided...")
		gwarn.grid(row=23,column=0)
		flag=3
		return

	precision=prec.get()
	anil=anilength.get()

	if shape_1 == 0:
		ani1=animate_rect(f,g,L,H,precision,anil)
	elif shape_1 == 1:
		ani1=animate_cir(f,g,r_0,precision,anil)

	ani1.save("wave_ani.gif")

	gc=mp.VideoFileClip("wave_ani.gif")
	gc.write_videofile("wave_ani.mp4")

welcome_label=Label(root,text="This program will generate animations of waves on"
	" rectangular and circular membranes with fixed ends using user-specified parameters.")
welcome_label.grid(row=0,column=0,padx=20,pady=5)

shape_label=Label(root,text="Select the shape and size parameters of the desired membrane:")
shape_label.grid(row=1,column=0,sticky=W,padx=5,pady=3)

shape=IntVar()
shape.set(-1)

shape_1=-1

Radiobutton(root,text="Rectangle                                                   ",
	variable=shape,value=0,command=changeshape0).grid(row=3,column=0)
len_text=Label(root,text="Length:                                       "+
	"                     ").grid(row=4,column=0,pady=3)
wid_text=Label(root,text="Width:                                        "+
	"                   ").grid(row=5,column=0,pady=3)

Radiobutton(root,text="Circle                                              "+
	"            ",variable=shape,value=1,command=changeshape1).grid(row=6,column=0)
rad_text=Label(root,text="Radius:                                          "+
	"                  ").grid(row=7,column=0,pady=3)

l=Entry(root,state=DISABLED)
w=Entry(root,state=DISABLED)
l.grid(row=4,column=0)
w.grid(row=5,column=0)
r=Entry(root,text="Input Radius",state=DISABLED)
r.grid(row=7,column=0)

ihd_text=Label(root,text="Define the initial height distribution of the membrane as a"+
	" function of either rectangular or polar coordinates:")
ihd_text.grid(row=8,column=0,padx=5,pady=5,sticky=W)

f_rtext=Label(root,text="f(x,y):                                                        "+
	"    ").grid(row=9,column=0,pady=3)
f_ptext=Label(root,text="f(r,θ):                                                       "+
	"     ").grid(row=10,column=0,pady=3)
f_r=Entry(root)
f_r.grid(row=9,column=0)
f_p=Entry(root)
f_p.grid(row=10,column=0)

f_preview=Button(root,text="Equation Preview",command=generate_fpreview).grid(row=11,column=0)

ivd_text=Label(root,text="Define the initial velocity distribution of the membrane as a"+
	" function of either rectangular or polar coordinates:")
ivd_text.grid(row=13,column=0,padx=5,pady=5,sticky=W)

g_rtext=Label(root,text="g(x,y):                                                      "+
	"      ").grid(row=14,column=0,pady=3)
g_ptext=Label(root,text="g(r,θ):                                                     "+
	"       ").grid(row=15,column=0,pady=3)
g_r=Entry(root)
g_r.grid(row=14,column=0)
g_p=Entry(root)
g_p.grid(row=15,column=0)

g_preview=Button(root,text="Equation Preview",command=generate_gpreview).grid(row=16,column=0)

misc_text=Label(root,text="Miscellaneous Options:")
misc_text.grid(row=18,column=0,padx=5,pady=5,sticky=W)

al_text=Label(root,text="Animation Length (in s):                                               "+
	"                                             ")
al_text.grid(row=20,column=0)
anilength=IntVar()
anilength.set(10)
len_drop=OptionMenu(root,anilength,5,10,15,20,25,30)
len_drop.grid(row=20,column=0)

prec_text=Label(root,text="Precision:                                                       "+
	"            ")
prec_text.grid(row=21,column=0)
prec=IntVar()
prec.set(5)
prec_drop=OptionMenu(root,prec,3,5,10,20)
prec_drop.grid(row=21,column=0)

mwarn=""
swarn=""

gen_ani=Button(root,text="Generate Animation!",command=generateanimation)
gen_ani.grid(row=22,column=0,pady=10)

space=Label(root,text="")
space.grid(row=23,column=0)

root.mainloop()