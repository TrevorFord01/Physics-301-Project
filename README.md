"# Physics-301-Project"

This repository contains all of the work and notebooks I created to complete the project for Physics 301, Computational Physics,
offered in the Fall 2020 semester at West Virginia University. My goal is to have several notebooks explaining the background mathematics and physics in
detail, as well as code that produces animations for waves on circular and rectangular membranes with fixed edges.

Please start with the preliminary report folder and read the report that was created prior to any developments. Note that not all goals were acheived, namely 
that the triangular boundary case was not investigated due to mathematical and computational difficulties that exceeded my capabilities; I had made an 
overestimation of the extent to which numerical solutions to PDEs would be covered both in this class and in my PDEs class and therefore was unable to 
tackle the challenge associated with the method of finite difference in 2D spaces. To make up for this lack of ability, I focused more of my resources into
the development of a graphical user interface to help ease users into the execution of the program. The GUI can handle user-input functions, size, and shape 
parameters and pass them to the animation generator programs. One downfall of the GUI compared to using the programs themselves however is the lack of ability 
to give piecewise-defined functions to the GUI - a future development could be to expand the utility of the GUI and allow for these types of entries.

Once you have finished reading the preliminary report, feel free to proceed to the background work folder (though this is optional). This folder contains 
all of the mathematical developments and basic code that I created for the development of this project. The most important file to investigate in this section 
is the 2D Separation of Variables file, since it contains the most-relevant work to the project itself. Also included in this folder are mp4s of animations 
generated by the codes in these notebooks. The final development output are animations that are similar to those found in this directory.

To operate the project's main program, download the repo and open the file project_gui.py using the terminal/command prompt. Ensure that you have the following 
modules installed on your device: Matplotlib, NumPy, SciPy, SymPy, MoviePy, Pillow, TkInter, and iPywidgets, otherwise the program will not operate as intended. 
Upon opening the file in the terminal, the GUI should appear. Here you can select what shape and size of membrane you are interested in, as well as the initial 
height and velocity distributions, the precision, and the animation length. The function inputs require that multiplication is performed between variables and 
numbers using the * key and exponentiation is used via the ** keys operator. Certain trigonometric and exponential functions also work if used in the text box 
function inputs. For example, the GUI will correctly identify sin(x) and exp(x) and connect them with the appropriate functions, all without the use of an extra 
module call.

When you hit "Generate Animation!" in the GUI, it takes your current selections and generates an animation that is saved in the same file as the GUI file in both 
.gif and .mp4 format. The name of the video file will be wave_ani - to view the result of the program you will need to open this file on your device (opening either 
the .gif or .mp4 will work fine). Feel free to test and generate as many animations as you wish, just be sure to save the ones you want to keep under a different 
name in a different folder.

Support Contact: tdf0008@mix.wvu.edu
